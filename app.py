from flask import Flask, jsonify, redirect, render_template , url_for
from controllers import user, quize
from flask_sqlalchemy import SQLAlchemy
from controllers.Trivia_API import fetch_questions
from models.models import db , User
from flask_migrate import Migrate
from flask_login import LoginManager, current_user ,login_required
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mimirima123@127.0.0.1:3306/quizapp'  
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view= 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/userhome')
@login_required
def userhome():
    if current_user.is_authenticated:
        username = current_user.username 
        return render_template('home.html', username=username) 
    else:
        return redirect(url_for('login'))  

@app.route('/login' ,methods=['GET','POST'])
def login():
    return render_template('auth/login.html')

@app.route('/register' ,methods=['GET','POST'])
def register():
    return render_template('auth/register.html')

@app.route('/register-user' ,methods=['GET','POST'])
def UserRegister():
    return user.register()


@app.route('/login-user' ,methods=['GET','POST'])
def UserLogin():
    return user.login()

@app.route('/logout')
def logout():
    return user.logout()

@app.route('/allquizes')
def allquizes():
    return quize.allquizes()


with app.app_context():
  db.create_all()
  api_url = 'https://opentdb.com/api.php?amount=18'
  fetch_questions(api_url, "General Knowledge")

if __name__ == "__main__":
    app.run(debug=True)