#errors/error_handler.py
from flask import Blueprint, render_template

errors_page = Blueprint('errors', __name__)

@errors_page.app_errorhandler(404)
def page_not_found(error):
    '''
    Error for page not found
    '''
    return render_template('errors/404.html'), 404

@errors_page.app_errorhandler(403)
def forbidden(error):
    '''
    The HTTP 403 Forbidden client error status response code indicates 
    that the server understands the request but refuses to authorize it.
    '''
    return render_template('errors/403.html'), 403