from flask import redirect
from flask_cors import CORS
import os

from factory import app
from errors.errors import load_error_page

# CORS
# In Ihrer Flask/Python API
CORS(app, origins=["https://localhost:3000"])  # Add-In Domain erlauben

# ROUTES
# register blueprints
from blueprints import register_blueprints
register_blueprints(app)

# Start
@app.route('/')
def start():
    return redirect(os.environ.get('START_LINK'))

# 500 Error-Handler (internal server error)
@app.errorhandler(500)
def internal_server_error(error):
    return load_error_page('Internal Server Error', 500)

# 503 Error-Handler (internal server error)
@app.errorhandler(503)
def privilege_error(error):
    return load_error_page('Service Unavailable Error', 503)

# 404 Error-Handler (internal server error)
@app.errorhandler(404)
def file_not_found_error(error):
    return load_error_page('Not Found Error', 404)

# 403 Error-Handler (internal server error)
@app.errorhandler(403)
def other_error(error):
    return load_error_page('Forbidden Error', 403)

if __name__ == '__main__':
    app.run(debug=True)
    # app.run(host='127.0.0.1', port=5000, ssl_context='adhoc')