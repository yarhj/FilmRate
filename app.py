from flask import Flask, render_template, redirect, url_for, abort
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
import uuid
import requests
from flask.cli import AppGroup
from data.users import User
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
from forms.add_film import FilmForm
from data.film import Films
from data import db_session
import getpass
import os

app = Flask(__name__)
db_session.global_init("db/database.db")

load_dotenv()

app.config['SECRET_KEY'] = os.getenv("SECRET_KEY")
app.config['UPLOAD_FOLDER'] = 'static/uploads'
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

cli = AppGroup('tmdb')
app.cli.add_command(cli)

login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = 'login'


@cli.command('import_popular')
def import_popular():
    db_sess = db_session.create_session()
    for page in range(1, 6):
        url = f"https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&language=ru&page={page}"
        response = requests.get(url)
        data = response.json()

        for movie in data['results']:
            existing_film = db_sess.query(Films).filter(Films.title == movie['title']).first()
            if existing_film:
                print(f"Фильм '{movie['title']}' уже есть в БД, пропускаем...")
                continue

            details_url = f"https://api.themoviedb.org/3/movie/{movie['id']}?api_key={TMDB_API_KEY}&language=ru"
            details_data = requests.get(details_url).json()
            credits_url = f"https://api.themoviedb.org/3/movie/{movie['id']}/credits?api_key={TMDB_API_KEY}"
            credits_data = requests.get(credits_url).json()
            director = next(
                (person['name'] for person in credits_data['crew'] if person['job'] == 'Director'),
                "Неизвестно"
            )
            screenwriter = next(
                (person['name'] for person in credits_data['crew'] if person['job'] == 'Writer'),
                "Неизвестно"
            )
            film = Films(
                title=movie['title'],
                description=movie.get('overview', 'Нет описания'),
                director=director,
                screenwriter=screenwriter,
                duration=details_data.get('runtime', 0),
                average_rating=movie.get('vote_average', 0),
                premiere=movie.get('release_date', '')[:4],
                poster_path=f"https://image.tmdb.org/t/p/w500{movie['poster_path']}" if movie.get('poster_path') else None,
                user_id=1
            )
            db_sess.add(film)
            print(f"Добавлен фильм: {movie['title']}")

        db_sess.commit()
        print('Импорт завершен')


app.cli.add_command(cli)


@app.route('/', methods=['GET', 'POST'])
def index():
    db_sess = db_session.create_session()
    films = db_sess.query(Films).all()

    return render_template('index.html', films=films)


@app.route('/film/<int:film_id>')
def film_detail(film_id):
    db_sess = db_session.create_session()
    film = db_sess.query(Films).get(film_id)
    if not film:
        return abort(404)
    return render_template("film_detail.html", film=film)


@app.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if (db_sess.query(User)
           .filter(
               (User.email == form.email.data) | (
                   User.username == form.username.data)
               )
           .first()):
            return render_template('registration.html',
                                   form=form,
                                   message="Пользователь с таким email или логином уже существует")
        user = User(
            username=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()
        return redirect('/login')
    return render_template('registration.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.username == form.username.data
            ).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.cli.command("create-admin")
def create_admin():
    db_sess = db_session.create_session()

    username = input("Введите имя администратора: ")
    email = input("Введите вашу почту: ")
    password = getpass.getpass("Введите пароль: ")
    confirm = getpass.getpass("Подтвердите пароль: ")

    if password != confirm:
        print("Пароли не совпадают!")
        return

    admin = User(
        username=username,
        email=email,
        is_admin=True
    )
    admin.set_password(password)

    db_sess.add(admin)
    db_sess.commit()
    print(f"Администратор {username} успешно создан!")


@app.route('/my_films')
def my_films(): 
    db_sess = db_session.create_session()
    user_films = db_sess.query(Films).filter(Films.user_id == current_user.id).all()
    return render_template("my_films.html", films=user_films)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


@app.route('/add_film', methods=['GET', 'POST'])
@login_required
def add_film():
    new_film = FilmForm()
    if new_film.validate_on_submit():
        db_sess = db_session.create_session()
        poster_file = new_film.poster.data
        if poster_file:
            filename = secure_filename(poster_file.filename)
            unique_filename = str(uuid.uuid4()) + '_' + filename
            poster_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            poster_file.save(poster_path)

            poster_db_path = os.path.join('uploads', unique_filename)
        else:
            poster_db_path = None

        films = Films(
            title=new_film.title.data,
            description=new_film.description.data,
            director=new_film.director.data,
            screenwriter=new_film.screenwriter.data,
            duration=new_film.duration.data,
            average_rating=new_film.rating.data,
            premiere=new_film.premiere.data,
            poster_path=poster_db_path,
            user_id=current_user.id
        )
        db_sess.add(films)
        db_sess.commit()
        return redirect('/')
    return render_template('add_film.html',
                           title='Добавление фильма',
                           form=new_film)


if __name__ == '__main__':
    app.run()
