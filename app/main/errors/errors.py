from flask import render_template
from .. import main


@main.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@main.errorhandler(500)
def page_error(e):
    return render_template('500.html', e=e)
