"""Table Rating"""

from models.app import db


class Rating(db.Model):
    """Each film is rated by the user on a 5-point scale"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fk_userrate_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    grade = db.Column(db.Integer, nullable=False)
    fk_filmrate_id = db.Column(db.Integer, db.ForeignKey("film.id"))

    def __init__(self, fk_userrate_id, fk_filmrate_id, grade):
        self.fk_userrate_id = fk_userrate_id
        self.grade = grade
        self.fk_filmrate_id = fk_filmrate_id
