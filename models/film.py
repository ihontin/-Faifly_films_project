"""Table Film"""

from models.app import db


class Film(db.Model):
    """ Model User. plan - film groups watch, watched, dropped.
    set - movies list from the seme denomination"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    set = db.Column(db.String(45), nullable=False)
    fk_genre_id = db.relationship('Genre', secondary='filmgenre',
                                  back_populates="fk_filmgen_id")
    plan = db.relationship("Plan", backref='film', lazy=True)
    comment = db.relationship("Comment", backref='film', lazy=True)
    rating = db.relationship("Rating", backref='film', lazy=True)

    def __init__(self, title, sets):
        self.title = title
        self.set = sets
