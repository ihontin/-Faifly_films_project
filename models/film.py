"""Table Film"""

from models.db import db


class Film(db.Model):
    """ Model Film. plan - film groups watch, watched, dropped.
    set - movies list from the seme denomination"""
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    fk_genre_id = db.relationship('Genre', secondary='filmgenre',
                                  back_populates="fk_filmgen_id")
    fk_filmgroup_id = db.Column(db.Integer, db.ForeignKey("filmgroup.id"))
    plan = db.relationship("Plan", backref='film', lazy=True)
    comment = db.relationship("Comment", backref='film', lazy=True)
    rating = db.relationship("Rating", backref='film', lazy=True)
    mean_rating = db.Column(db.Integer, nullable=False)

    def __init__(self, title, fk_filmgroup_id, mean_rating):
        self.title = title
        self.fk_filmgroup_id = fk_filmgroup_id
        self.mean_rating = mean_rating
