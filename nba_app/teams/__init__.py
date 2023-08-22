from flask_smorest import Blueprint

blp = Blueprint('teams', __name__)

from nba_app.teams import teams
