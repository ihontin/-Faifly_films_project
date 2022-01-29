"""Creating and seeding models"""

import json

from models.app import db
from models.user import User
from models.film import Film
from models.genre import Genre
from models.film_genre import Filmgenre


def create_db():
    """Create tables in postgres db"""
    from models.user import User
    from models.film import Film
    from models.genre import Genre
    from models.film_genre import Filmgenre
    from models.plan import Plan
    from models.comment import Comment
    from models.rating import Rating
    db.create_all()


def seeding_db():
    """Seeding tables in postgres db"""
    result = db.session.query(User).all()
    if len(result) == 0:
        genre_list, film_list = [], []

        # Fill USER Table
        # with open("./data/user.json"...  # for running without docker
        with open("./models/data/user.json", 'r', encoding='utf-8') as user_file:
            json_user = json.load(user_file)

        for row in json_user:
            fill_user = User(login=row['login'],
                             password=row['password'], user_mail=row['user_mail'], admin=row['admin'], vanish=1)
            db.session.add(fill_user)

        # Fill FILM Table
        # with open("./data/film.json"...  # for running without docker
        with open("./models/data/film.json", 'r', encoding='utf-8') as film_file:
            json_film = json.load(film_file)

        for row in json_film:
            fill_film = Film(title=row['title'], sets=row['set'], mean_rating=0)
            film_list.append(fill_film)
            db.session.add(fill_film)

        # Fill GENRE Table
        # with open("./data/genre.json"...  # for running without docker
        with open("./models/data/genre.json", 'r', encoding='utf-8') as gen_file:
            json_genre = json.load(gen_file)

        for row in json_genre:
            fill_genre = Genre(title=row['title'])
            genre_list.append(fill_genre)
            db.session.add(fill_genre)

        # Fill Filmgenre Table
        filmgenre_seeds = [(11, 0), (0, 0), (5, 1), (0, 1), (11, 2), (11, 3), (11, 4), (11, 5), (11, 6), (11, 7),
                           (0, 8), (1, 8), (11, 8), (0, 9), (5, 9), (0, 10), (5, 10), (0, 11), (5, 11), (0, 12),
                           (5, 12), (0, 13), (5, 13), (0, 14), (5, 14), (0, 15), (5, 15), (0, 16), (5, 16), (0, 17),
                           (1, 17), (2, 18), (3, 18), (4, 19), (5, 19), (6, 20), (7, 20), (8, 21), (9, 21), (10, 22),
                           (11, 22), (12, 23), (0, 23), (1, 24), (2, 24), (3, 25), (4, 25), (5, 26), (6, 26), (7, 27),
                           (8, 27), (9, 28), (10, 28), (11, 29), (12, 29), (11, 30), (2, 30), (10, 31), (3, 31),
                           (9, 32), (4, 32), (8, 33), (5, 33), (7, 34), (6, 34), (0, 35), (2, 35), (1, 36), (3, 36),
                           (2, 37), (4, 37), (3, 38), (5, 38), (4, 39), (6, 39), (7, 40), (5, 40), (8, 41), (6, 41),
                           (7, 42), (9, 42), (8, 42), (10, 42), (9, 43), (11, 43), (10, 44), (12, 44), (0, 45), (5, 45),
                           (1, 46), (6, 46), (7, 47), (2, 47), (8, 48), (3, 48), (4, 49), (9, 49)]
        for seed in filmgenre_seeds:
            genre_list[seed[0]].fk_filmgen_id.append(film_list[seed[1]])

        db.session.commit()
    else:
        print("The database is seeded")
        db.session.commit()


# create_db()
# seeding_db()
