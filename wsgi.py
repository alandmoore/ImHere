import sys
import os.path
import os

path = os.path.realpath(os.path.dirname(__file__))
virtualenv_path = os.path.join(path, "env")

# activate virtualenv if it exists
activate_this = os.path.join(virtualenv_path, "bin/activate_this.py")

if os.path.exists(activate_this):
    with open(activate_this, 'r') as fh:
        exec(fh.read(), dict(__file__=activate_this))
        print("Using virtualenv at {}.".format(virtualenv_path))
else:
    print("Using system python environment.")

sys.path.insert(0, path)

if os.environ.get('IMHERE_DEBUG'):
    # Activate Debugging
    print("I'm Here! debugging ON")
    from werkzeug.debug import DebuggedApplication
    from main import app
    application = DebuggedApplication(app, True)
else:
    from main import app as application
