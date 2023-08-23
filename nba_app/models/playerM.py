from app import db


class Player(db.Model):
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), unique=True, nullable=False)
    birth_date = db.Column(db.Date, nullable=False)
    position = db.Column(db.String(15), nullable=False)
    team_id = db.Column(db.Intiger, db.ForeignKey('teams.id'), nullable=False)
    team = db.relationship('Team', back_populates='player')

    def __repr__(self):
        return f'<{self.__class__.__name__}>: {self.team.first_name} {self.team.last_name}'
