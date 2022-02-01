"""All routes index, login, logout, registration, film, profile"""

from datetime import datetime
from flask import render_template, request, flash, url_for, redirect
from werkzeug.security import check_password_hash, generate_password_hash
from flask_login import login_user, current_user, logout_user, login_required

from models.app import app, db, login_manager
from models.user import User
from models.film import Film
from models.genre import Genre
from models.plan import Plan
from models.comment import Comment
from models.rating import Rating
from models.film_genre import Filmgenre

menu_active = [{"name": "Main page", "url": "/"},
               {"name": "Profile", "url": "profile"},
               {"name": "Logout", "url": "logout"}]

menu_anonym = [{"name": "Main page", "url": "/"},
               {"name": "Profile", "url": "profile"},
               {"name": "Login", "url": "login"}]

film_glob = {}


def find_film_group(user_db, film_db):
    """ Find film group by user id and film id """
    result = db.session.query(Plan).filter(Plan.fk_userplan_id == user_db, Plan.fk_filmplan_id == film_db).first()
    return result


def user_film_list(user_id):
    """ Find film list in Plan model by user id """
    result = db.session.query(Plan).filter(Plan.fk_userplan_id == user_id).order_by(Plan.title).all()
    return result


def find_user(user_name):
    """ Find user by nickname"""
    result = db.session.query(User).filter(User.login == user_name).first()
    return result


def check_user():
    """ Return menu for authenticated or anonymous user """
    if current_user.is_active:
        return menu_active
    else:
        return menu_anonym


def profile_film_list():
    """Return all films from Plan model by user.id"""
    return Film.query.join(Film.plan).filter(Plan.fk_userplan_id == current_user.id).order_by(Plan.title).all()


@login_manager.user_loader
def load_user(user_id):
    """ User in session """
    return db.session.query(User).get(user_id)


@app.route("/")
@app.route("/index")
def index():
    """ Main page shows all movies. Pagination - 5 movies in page, user can choose a genre """
    page = request.args.get('page', 1, type=int)
    genre_search = request.args.get('genre_search', None, type=int)
    sort_by = request.args.get('sort_by', None, type=int)
    title = request.args.get('title', 'Films', type=str)
    film_glob['film'] = title
    if genre_search:
        if sort_by:
            list_of_films = Film.query.join(Film.fk_genre_id).filter(Genre.id == genre_search).\
                order_by(db.desc(Film.mean_rating)).paginate(page=page, per_page=5)
        else:
            list_of_films = Film.query.join(Film.fk_genre_id).filter(Genre.id == genre_search).\
                paginate(page=page, per_page=5)
    else:
        if sort_by:
            list_of_films = db.session.query(Film).order_by(db.desc(Film.mean_rating)).paginate(page=page, per_page=5)
        else:
            list_of_films = db.session.query(Film).paginate(page=page, per_page=5)
    genres = db.session.query(Genre).all()
    menu = check_user()
    return render_template('index.html', title=title, menu=menu, li_of_films=list_of_films, genres=genres,
                           genre_search=genre_search, sort_by=sort_by)


@app.route("/login", methods=["POST", "GET"])
def login():
    """ Login page """
    menu = check_user()
    if request.method == 'POST':
        if current_user.is_active:
            flash('User already logged in', category='error')
            return render_template('login.html', title='Authorization', menu=menu)
        user_log = find_user(request.form['username'])
        if user_log:
            user_pass = check_password_hash(user_log.password, str(request.form['password']))
            if user_pass:
                login_user(user_log)
                menu = menu_active
                return redirect(url_for('index', menu=menu))
            else:
                flash('Wrong name or password', category='error')
        else:
            flash('Wrong name or password', category='error')
    return render_template('login.html', title='Authorization', menu=menu)


@app.route("/logout", methods=["POST", "GET"])
def logout():
    """ Logout page """
    if current_user.is_active:
        menu = menu_active
    else:
        menu = menu_anonym
        return redirect(url_for('login', title='Authorization', menu=menu))
    if request.method == 'POST':
        logout_user()
        flash('Successful logout', category='success')
        return redirect(url_for('login', title='Authorization', menu=menu))
    return render_template('logout.html', title='Logout', menu=menu)


@app.route("/registration", methods=["POST", "GET"])
def registration():
    """ New user registration """
    if current_user.is_active:
        menu = menu_active
        flash('Logout first', category='error')
        return redirect(url_for('logout', title='Logout', menu=menu))
    menu = menu_anonym
    if request.method == 'POST':
        exist_nick = find_user(request.form['username'])
        if exist_nick:
            flash(f'User with nickname {request.form["username"]} already exists.  Login should be unique',
                  category='error')
            return render_template('registration.html', title='Registration', menu=menu)
        if len(request.form['username']) < 5 and len(request.form['user_email']) < 5 \
                and len(request.form['password']) < 5:
            flash('Passwords and nick should be at least five characters long', category='error')
            return render_template('registration.html', title='Registration', menu=menu)
        if request.form['password'] != request.form['verify_password']:
            flash('Password mismatch', category='error')
            return render_template('registration.html', title='Registration', menu=menu)
        pass_hash = generate_password_hash(request.form['password'])
        add_user = User(login=request.form['username'], password=pass_hash,
                        user_mail=request.form['user_email'], admin=0, vanish=1)
        try:
            db.session.add(add_user)
            db.session.commit()
        except Exception as ex:
            return f"Registration error - {ex}"
        flash('New account created successfully. Login to continue.', category='new_account')
        return redirect(url_for('login', title='Authorization', menu=menu))
    return render_template('registration.html', title='Registration', menu=menu)


@app.route('/film/<int:film_id>/<int:set_number>/add', methods=["POST", "GET"])
@login_required
def film_add_plan(film_id, set_number):
    """ Add or change group of film """
    menu = menu_active
    if current_user.is_anonymous:
        menu = menu_anonym
        return redirect(url_for('login', title='Authorization', menu=menu))
    film_title = db.session.query(Film).filter(Film.id == film_id).first()
    sets = find_film_group(current_user.id, film_id)
    film_groups_list = ['watch', 'watched', 'dropped']
    if sets:
        if sets.sets == film_groups_list[set_number]:
            flash(f'Film "{film_title.title}" was added to "{film_groups_list[set_number]}" list on '
                  f'{sets.adding_time.date()}', category='new_account')
            return redirect(url_for('film', title=sets.title, menu=menu))
        sets.sets = film_groups_list[set_number]
        try:
            db.session.commit()
            flash(f'{film_title.title} added to "{film_groups_list[set_number]}" list', category='success')
            return redirect(url_for('film', title=film_title.title, menu=menu))
        except Exception as ex:
            return f"Adding movie error - {ex}"
    else:
        try:
            fill_plan = Plan(fk_userplan_id=current_user.id, fk_filmplan_id=film_id, title=film_title.title,
                             sets=film_groups_list[set_number], adding_time=datetime.now())
            db.session.add(fill_plan)
            db.session.commit()
            flash(f'{film_title.title} added', category='success')
            return redirect(url_for('film', title=film_title.title, menu=menu))
        except Exception as ex:
            return f"Adding movie error - {ex}"


@app.route('/film/<int:comment_id>/del')
@login_required
def film_comment_del(comment_id):
    """Delete comment from film page"""
    menu = check_user()
    del_film = db.session.query(Comment).filter(Comment.id == comment_id).first()
    try:
        db.session.delete(del_film)
        db.session.commit()
        return redirect(url_for('film', title=film_glob['film'], menu=menu, cur_user=current_user))
    except Exception as ex:
        return f"Deleting movie error - {ex}"


@app.route('/film/<int:rating_num>/<int:film_id>/<int:user_id>/rating')
@login_required
def film_rating_add(rating_num, film_id, user_id):
    """Delete comment from film page"""
    menu = check_user()
    find_rating = db.session.query(Rating).filter(Rating.fk_filmrate_id == film_id,
                                                  Rating.fk_userrate_id == user_id).first()
    if find_rating:
        find_rating.grade = rating_num
        try:
            db.session.commit()
            return redirect(url_for('film', title=film_glob['film'], menu=menu, cur_user=current_user))
        except Exception as ex:
            return f"Change film rating error - {ex}"
    try:
        new_rating = Rating(fk_userrate_id=user_id, grade=rating_num, fk_filmrate_id=film_id)
        db.session.add(new_rating)
        db.session.commit()
        return redirect(url_for('film', title=film_glob['film'], menu=menu))
    except Exception as ex:
        return f"Add new film rating error - {ex}"


@app.route("/film", methods=["POST", "GET"])
def film():
    """ 'Film page' show selected movie, and user can add it to watch list, genres, comments,
     films from the same denomination. User can add and delete his comments"""
    menu, film_rating = menu_active, None
    title_film = request.args.get('title', None, type=str)
    if title_film:
        film_glob['film'] = title_film
    film_select = db.session.query(Film).filter(Film.title == film_glob['film']).first()
    genres = Genre.query.join(Genre.fk_filmgen_id).filter(Film.title == film_glob['film']).all()
    # film_sets - find films from the same film group
    film_sets = db.session.query(Film).filter(Film.set == film_select.set).all()
    film_comments = db.session.query(Comment).join(Film).filter(Film.id == film_select.id).all()
    find_rating = db.session.query(Rating).filter(Rating.fk_filmrate_id == film_select.id).all()
    if find_rating:
        film_rating = (sum(f_rat.grade for f_rat in find_rating)) // len(find_rating)
        film_select.mean_rating = film_rating
        try:
            db.session.commit()
        except Exception as ex:
            return f"Change film mean rating error - {ex}"
    if current_user.is_anonymous:
        menu = menu_anonym
        return render_template('film.html', title=film_glob['film'], menu=menu, genres=genres, cur_user=current_user,
                               film_select=film_select, film_sets=film_sets, film_comments=film_comments,
                               film_rating=film_rating)
    if request.method == 'POST':
        new_comment = request.form['comment']
        user_comment = Comment(fk_usercom_id=current_user.id, nick=current_user.login, fk_filmcom_id=film_select.id,
                               adding_time=datetime.now(), my_comment=new_comment)
        try:
            db.session.add(user_comment)
            db.session.commit()
            return redirect(url_for('film', title=film_glob['film'], menu=menu))
        except Exception as ex:
            return f"Add new user comment error - {ex}"
    return render_template('film.html', title=film_glob['film'], menu=menu, genres=genres, film_sets=film_sets,
                           film_select=film_select, film_comments=film_comments, cur_user=current_user,
                           film_rating=film_rating)


@app.route('/profile/hide')
@login_required
def profile_hide():
    """Delete movie from active user film list"""
    menu = check_user()
    if current_user.vanish:
        current_user.vanish = 0
    else:
        current_user.vanish = 1
    try:
        db.session.commit()
        return redirect(url_for('profile', title="Profile", menu=menu))
    except Exception as ex:
        return f"Deleting movie error - {ex}"


@app.route('/profile/<int:film_id>/<int:set_num>/sets')
@login_required
def profile_plan_watched(film_id, set_num):
    """Change movie group in active user film list"""
    sets_number = ['watch', 'watched', 'dropped']
    menu = check_user()
    sets = find_film_group(current_user.id, film_id)
    sets.sets = sets_number[set_num]
    try:
        db.session.commit()
        return redirect(url_for('profile', title="Profile", menu=menu))
    except Exception as ex:
        return f"Deleting movie error - {ex}"


@app.route('/profile/<int:film_id>/del')
@login_required
def profile_plan_del(film_id):
    """Delete film from plan list"""
    menu = check_user()
    del_film = find_film_group(current_user.id, film_id)
    try:
        db.session.delete(del_film)
        db.session.commit()
        return redirect(url_for('profile', title="Profile", menu=menu))
    except Exception as ex:
        return f"Deleting movie error - {ex}"


@app.route("/profile")
@login_required
def profile():
    """Profile page show active user film list"""
    if current_user.is_active:
        menu = menu_active
        sets_plan = user_film_list(current_user.id)
    else:
        menu = menu_anonym
        return redirect(url_for('index', title="Films", menu=menu))
    return render_template('profile.html', title="Profile", menu=menu, sets_plan=sets_plan, user=current_user)


@app.route("/users")
@login_required
def users():
    """logged user can find another user by nickname to watch his films list"""
    menu = check_user()
    user_films_list, user_id = None, None
    list_of_users = db.session.query(User).all()
    username = request.args.get('username', 'Users', type=str)
    user_log = find_user(username)
    plan_sets = ['watch', 'watched', 'dropped']
    if user_log:
        if user_log.vanish or user_log.id == current_user.id:
            user_id = request.args.get('user_id', None, type=int)
        else:
            flash(f'User "{username}" has restricted access to own list', category='error')
    if user_id:
        plan_sets = []
        user_films_list = db.session.query(Plan).filter(Plan.fk_userplan_id == user_id).\
            order_by(Plan.sets, Plan.title).all()
        for one_film in user_films_list:
            if one_film.sets not in plan_sets:
                plan_sets.append(one_film.sets)
    return render_template('users.html', title='Users', menu=menu, user_id=user_id, username=username,
                           list_of_users=list_of_users, user_films_list=user_films_list, plan_sets=plan_sets)


@app.errorhandler(404)
def page_not_found():
    """New page for 404 error
    user can return to main page"""
    menu = check_user()
    return render_template("page404.html", title="Page not found", menu=menu), 404  # return 404 code
