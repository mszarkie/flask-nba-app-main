from flask import Blueprint

blp = Blueprint('auth', __name__)

from nba_app.auth import auth