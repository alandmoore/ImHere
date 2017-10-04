#############################################
# Configuration file for signin application #
#############################################


# The secret key
SECRET_KEY = "Set me to a random string of characters"

# Path to the sqlite db file
DB_LOCATION = "/tmp/signin.db"

DEBUG = True

# The name of your business/government/etc.
ORGANIZATION = "Our organization"

# CLAIM_LIMIT and UNCLAIM_LIMIT are the time periods after which records are deleted.
# CLAIM_LIMIT is expressed as a time period from the time the person was claimed.
# UNCLAIM_LIMIT is expressed as a time period from the time the person signed in.
# Defaults:
#   - CLAIM_LIMIT: '30 minutes'
#   - UNCLAIM_LIMIT: '8 hours'

CLAIM_LIMIT = '10 minutes'
UNCLAIM_LIMIT = '8 hours'

RECIPIENTS = ["admin@example.com"]

# IF this is None or empty, users will not be prompted for an appointment time
# and everyone will be treated as a walk-in.
# Otherwise, it's a list of valid appointment times.
APPOINTMENT_TIMES = [
    "", "8:15 AM", "8:30 AM", "9:15 AM", "9:30 AM", "10:15 AM", "10:30 AM",
    "1:15 PM", "1:30 PM", "2:15 PM", "2:30 PM", "3:15 PM", "3:30 PM"
]


# NOTIFICATIONS are the settings for the email notifications.
# The template will plugin the following values:
# - {name} = The name of the person signing in
# - {appointment_details} = A phrase indicating if the person had an appointment, and what time.
# - {signin_time} = The time a person signed in
# - {url} = The url for the staff interface

NOTIFICATIONS = {
    "template": (
        "{name} signed in at {signin_time} {appointment_details}."
        "\n\n"
        "To see if {name} is still waiting, visit {url} in your browser."
    ),
    "appointment_template": (
        "for a {appointment_time} appointment"
    ),
    "walk_in_template": (
        "as a walk-in"
    ),
    "reply_to": "noreply@example.com",
    "subject": "[I'm Here!] Someone just signed in..."
}

SIGNIN_PAGE = {
    "office_name": "Our Office",
    "info_note": '',
    "name_instructions": "Please Enter your name and click &quot;Accept&quot;",
    "appointment instructions": "Select your appointment time from the list."
}
