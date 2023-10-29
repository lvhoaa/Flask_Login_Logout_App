from flask import Flask 
from flask_sqlalchemy import SQLAlchemy
from os import path 
from flask_login import LoginManager

db= SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY']='fljk;sdajfl' # store session token/ cookie
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}' # declare where sqlalchemy is located
    db.init_app(app)
    
    from .views import views #import Blueprint from module 
    from .auth import auth 
    
    app.register_blueprint(views,url_prefix='/') 
    app.register_blueprint(auth,url_prefix='/')
    #url prefix could be changed to '/views/' or '/auth/'
    
    
    
        
    from .models import User,Note
    
    with app.app_context():
        db.create_all()
    
    #create_database(app)
    
    
    login_manager = LoginManager() # config flask log in 
    login_manager.login_view = 'auth.login' # where to go if not LOGGED IN 
    login_manager.init_app(app)
    
    @login_manager.user_loader 
    def load_user(id):
        return User.query.get(int(id))
    
    return app 

def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
    