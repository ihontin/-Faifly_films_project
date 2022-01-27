"""Table Film"""

from models.app import db


class Comment(db.Model):
    """ User comments about films """
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    fk_usercom_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    nick = db.Column(db.String(100), nullable=True)
    fk_filmcom_id = db.Column(db.Integer, db.ForeignKey("film.id"))
    adding_time = db.Column(db.DateTime, nullable=False)
    my_comment = db.Column(db.String(500), nullable=True)

    def __init__(self, fk_usercom_id, fk_filmcom_id, adding_time, my_comment, nick):
        self.fk_usercom_id = fk_usercom_id
        self.nick = nick
        self.fk_filmcom_id = fk_filmcom_id
        self.adding_time = adding_time
        self.my_comment = my_comment
