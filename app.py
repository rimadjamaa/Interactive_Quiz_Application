from flask import Flask, render_template , url_for
from controllers import user
from flask_sqlalchemy import SQLAlchemy
from models.models import db
from flask_migrate import Migrate
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mimirima123@127.0.0.1:3306/quizapp'  # Change to your DB
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
migrate = Migrate(app, db)

@app.route('/')
def home():
    return render_template('home.html')

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

with app.app_context():
  db.create_all()


if __name__ == "__main__":
    app.run(debug=True)