I'm Here!
=========

About
--------

**I'm Here!** is a vitual sign-in sheet designed originally for public offices.  It's essentially a digital equivalent of a sign-in clipboard like you'd see at a doctor's office, for example.

I'm Here! is primarily the work of Alan D Moore <me AT alandmoore DOT com>

Features
--------

- Web-based, accessible by multiple clients simultaneously
- Touch-compatible for use with touch-screen kiosks or tablets
- Can be configured to use appointments, or handle walk-in only.

Design
------

I'm Here! is built on these technologies:

- Backend:
  - Flask
  - Sqlite
  - Jinja2
  - Python

- Frontend:
  - HTML5
  - JQuery
  - JQuery-UI

It's designed to run on a Linux server.


Configuration
-------------

I'm Here! has the following configuration options:

- DB_LOCATION:  Full path to the sqlite database file.  Since this is throwaway data, speed is preferred.  I recommend /dev/shm/.  I'm Here! will create the database automatically, so this file can be simply deleted if the database is corrupt.

- CLAIM_LIMIT: This is the length of time after a signin is claimed that it will be deleted.  For silly implementation reasons, it's expressed as a negative value, e.g. "-20 minutes".

- UNCLAIM_LIMIT: This is the length of time after a signin is submitted that it will be deleted, if it is never claimed.  This is in case people get lazy and never claim anything.

- RECIPIENTS: A list of emails which will be contacted when someone signs in.

- ORGANIZATION: This is the name of your business / organization

- SIGNIN_PAGE: This is a list of items to configure the text on the sign-in page.  It includes your office name and various instructions for the user.

- NOTIFICATIONS: This is some configuration for your email notifications, including subject, reply-to email, and templates for the actual email.

Usage
-----

Here's a typical setup for an office:

Let's assume the application has been set up on a webserver called Pokey under the subdirectory "signin".

- A web browser kiosk would be set up pointing to http://pokey/signin.
- Visitors will use the kiosk to sign their name and indicate if they have an appointment or not, and if so what time.
- When visitors sign in, an email is sent to the recipients that a visitor has signed in, and direct them to http://pokey/signin/view to see the status.
- If their name is not stored in the browser's localStorage, the employees will be able to enter names to identify themselves.
- If they are able to help the visitor, employees will *claim* the visitor by clicking the "claim" button.
- Other employees can see that the visitor has been helped, and who is helping them.
- After the configured time limits, the visitor entries are deleted from the database.


Current Limitations
-------------------

- Currently there is **NO SECURITY** whatsoever.  It's assumed your web app is running on a private LAN, the URL is hidden from the public, and that you trust your employees to do the right things.

  - Eventually, LDAP or other login support could be added, if there is a demand.

- The application is effectively married to **English**.  Localizing it may require you to edit HTML and JS files extensively.

  - Ultimately, all textual components should be moved to the config file so you can customize them to any language or verbiage you desire.

- The application is not designed for **High Concurrency**.  You should be fine using it with < 10 kiosks and < 10 staff, maybe more.  It probably won't scale to an operation serving hundreds, due to the SQLite backend.

- The data is considered to be disposable.  You *can* download it for your records, but it's intended to be temporary, much like you might throw away a sign-in sheet at the end of a day.

- I'm Here! is not really a full appointment-scheduling application; it's strictly a digital sign-in form.  Eventually it may grow.


Bugs, Features, Help
--------------------

Please submit issues to the github project.

If you would like to see a new feature, please understand you have 3 chances to see it happen:

- Code the feature yourself and submit a pull request
- Pay someone (like the author) to code the feature
- Pray that someone else does one of the other two things

If you need assistance installing and configuring this application, you may contact the author for help, but please be willing to offer some reasonable compensation for his time.  "The code is free; my time is not."

License
-------

This project is licensed under the terms of the GNU GPL v3.  Please see the COPYING file for details.
