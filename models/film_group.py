"""Table Film group"""

from models.db import db


class FilmGroup(db.Model):
    """ Model FilmGroup
    films that have sequels or several parts have a common group
    """
    __tablename__ = 'filmgroup'
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    title = db.Column(db.String(45), nullable=False)
    group = db.relationship("Film", backref='filmgroup', lazy=True)

    def __init__(self, title):
        self.title = title
        