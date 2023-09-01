from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from config import Config


db = SQLAlchemy()
migrate = Migrate()


def create_app(config_class=Config):

    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    from nba_app.commands import blp as CommandBluePrint
    from nba_app.errors import blp as ErrorsBluePrint
    from nba_app.teams import blp as TeamsBluePrint
    from nba_app.players import blp as PlayersBluePrint
    from nba_app.auth import blp as AuthBluePrint

    app.register_blueprint(CommandBluePrint)
    app.register_blueprint(ErrorsBluePrint)
    app.register_blueprint(TeamsBluePrint, url_prefix='/v1')
    app.register_blueprint(PlayersBluePrint, url_prefix='/v1')
    app.register_blueprint(AuthBluePrint, url_prefix='/v1/auth')

    return app
