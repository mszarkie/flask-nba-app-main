from flask import Blueprint

blp = Blueprint('errors', __name__)

from nba_app.errors import errors