from flask import Blueprint

blp = Blueprint('players', __name__)

from nba_app.players import players