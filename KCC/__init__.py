from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask import Blueprint, render_template, request, flash, redirect, url_for
#from flask_ngrok import run_with_ngrok

db = SQLAlchemy()
DB_NAME = "kccdatabase.db"

def create_app():
    app = Flask(__name__, template_folder='template', static_url_path='/static')
    #run_with_ngrok(app)
    app.config['UPLOAD_FOLDER'] = 'uploads'
    app.config['ALLOWED_EXTENSIONS'] = {'pdf'}
    app.config['ACCEPTED_EXTENSIONS'] ={'mp3','wav', 'ogg'}
    app.config['SECRET_KEY'] = '12345678'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

    from .views import views

    from .auth import auth
    #from .function import function

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    #app.register_blueprint(function, url_prefix='/')

    from .datamodels import User, Admin, Uploadannouncement

    with app.app_context():
        create_database(app)

        admin_login_manager = LoginManager()
        admin_login_manager.init_app(app)

        user_login_manager = LoginManager()
        user_login_manager.init_app(app)

        @admin_login_manager.user_loader
        def load_admin(id):
            return Admin.query.get(int(id))

        @admin_login_manager.unauthorized_handler
        def admin_unauthorized():
            flash('You need to log in as an admin.', 'error')
            return redirect(url_for('views.adminlogin'))

        @user_login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))

        @user_login_manager.unauthorized_handler
        def user_unauthorized():
            flash('You need to log in as a user.', 'error')
            return redirect(url_for('views.userlogin'))

    return app


def create_database(app):
    db.init_app(app)
    
    if not path.exists('KCC/' + DB_NAME):
        db.create_all()
        print('Created Database')
