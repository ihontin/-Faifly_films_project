"""Table Plan"""

from models.app import db


class Plan(db.Model):
    """ User can add film to his list.
    Groups in the list: watch, watched, dropped."""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fk_userplan_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    fk_filmplan_id = db.Column(db.Integer, db.ForeignKey("film.id"))
    title = db.Column(db.String(255), nullable=True)
    sets = db.Column(db.String(255), nullable=True)
    adding_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, fk_userplan_id, fk_filmplan_id, sets, adding_time, title):
        self.fk_userplan_id = fk_userplan_id
        self.fk_filmplan_id = fk_filmplan_id
        self.sets = sets
        self.adding_time = adding_time
        self.title = title
