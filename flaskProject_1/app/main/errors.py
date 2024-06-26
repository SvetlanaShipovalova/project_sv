from flask import render_template
from . import main


@main.errorhandler(404)
def page_not_found():
    return render_template("404.html"), 404


@main.errorhandler(400)
def error_request():
    return render_template("400.html"), 400
