from flask import render_template

# load error page
def load_error_page(type, code):
    return render_template('errors/error.html', code=code)