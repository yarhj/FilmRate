from flask import Flask, render_template, redirect, url_for
from forms.login_form import LoginForm
from forms.register_form import RegisterForm
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from data.users import User
from dotenv import load_dotenv
from data import db_session
import getpass
import os

app = Flask(__name__)
db_session.global_init("db/database.db")

load_dotenv()
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

login_manager = LoginManager()
login_manager.init_app(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')


@app.route('/registration', methods=['GET', 'POST'])
def reqistration():
    form = RegisterForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        if (db_sess.query(User)
           .filter((User.email == form.email.data) | (User.username == form.username.data))
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
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(
            User.email == form.email.data,
            User.username == form.username.data
            ).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/")
        return render_template('login.html',
                               message="Неправильный логин или пароль",
                               form=form)
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    pass


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


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect("/")


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.get(User, user_id)


if __name__ == '__main__':
    app.run()
