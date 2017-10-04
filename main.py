"""
I'm Here!
By Alan D Moore

This application is intended as a sort of digitized "sign-in sheet",
such as you might sign at a doctor's office.

See README.md for more information.
"""

from flask import Flask, render_template, g, request, abort, json, url_for
from includes.model import Model
from includes.email_utils import send_email
from includes.downloads import data_dump_csv
from functools import partial
from datetime import datetime

app = Flask(__name__, instance_relative_config=True)
app.config.from_object("config")
app.config.from_pyfile("config.py", silent=True)


@app.before_request
def before_request():
    """Initialize the environment"""
    g.db = Model(app.config["DB_LOCATION"])
    g.db.clear_old_customers(
        app.config["CLAIM_LIMIT"],
        app.config["UNCLAIM_LIMIT"]
    )
    g.notification_config = app.config["NOTIFICATIONS"]

@app.route("/")
def index():
    """Present the default landing page

    Users will use this page to sign in to the waiting list.
    """
    return render_template("main.jinja2", use_osk=request.args.get("osk"))


def submit_customer(**kwargs):
    """Handle the logic when a customer signs in."""

    # Enter the customer in the database
    g.db.submit_customer(**kwargs)

    # Email the recipients about it
    if (
            app.config["APPOINTMENT_TIMES"] and
            kwargs.get("has_appointment") == [1]
    ):
        appointment_details = (
            g.notification_config.get('appointment_template').format(
                appointment_time=kwargs.get(
                    "appointment_time", ['unspecified']
                )[0]
            )
        )
    elif app.config["APPOINTMENT_TIMES"]:
        appointment_details = g.notification_config.get('walk_in_template')
    else:
        appointment_details = ''

    message = g.notification_config.get("template").format(
        name=kwargs.get("name", ["Unknown"])[0],
        signin_time=datetime.now().strftime("%-I:%M %p"),
        url=url_for("view", _external=True),
        appointment_details=appointment_details
    )
    for recipient in app.config["RECIPIENTS"]:
        send_email(
            to=recipient,
            sender=g.notification_config.get('reply_to'),
            subject=g.notification_config.get('subject'),
            message=message
        )
    return True


@app.route("/post/<callback>", methods=["POST"])
def post(callback):
    """Receive posted data and respond appropriately
    """
    callbacks = {
        "sign_in": partial(submit_customer, **request.form),
        "list": g.db.list_customers,
        "claim_customer": partial(g.db.claim_customer, **request.form),
        "unclaim_customer": partial(g.db.unclaim_customer, **request.form)
    }

    try:
        return json.dumps(callbacks[callback]())
    except KeyError:
        print("bad callback: {}".format(callback))
        abort(400)


@app.route("/view")
def view():
    """View the current waiting list and unqueue waiters.
    """
    return render_template("view.jinja2")


@app.route("/download/<callback>")
def download(callback):
    """Request a download file
    """
    callbacks = {
        "data_dump_csv": partial(data_dump_csv, g.db)
    }

    if callback not in callbacks.keys():
        print("bad callback: {}".format(callback))
        abort(400)

    data, headers, mimetype = callbacks[callback]()

    return Response(
        data,
        mimetype=mimetype,
        headers=headers
    )


if __name__ == "__main__":
    app.run(debug=True)
