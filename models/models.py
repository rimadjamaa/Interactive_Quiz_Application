from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# User Table
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="user")  # 'user' or 'admin'
    profile = db.relationship('Profile', backref='user', uselist=False, lazy=True)
    scores = db.relationship('UserScore', backref='user', lazy=True)
    submitted = db.relationship('QuizSubmit', backref='user', lazy=True)


# Profile Table
class Profile(db.Model):
    __tablename__ = 'profile'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, unique=True)
    email_address = db.Column(db.String(100))
    bio = db.Column(db.Text)
    profile_img = db.Column(db.String(200))
    location = db.Column(db.String(100))
    gender = db.Column(db.String(10))

# Quiz Table
class Quiz(db.Model):
    __tablename__ = 'quiz'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    file = db.Column(db.String(200))  # For quiz resources
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)
    questions = db.relationship('Question', backref='quiz', lazy=True)
    scores = db.relationship('UserScore', backref='quiz', lazy=True)
    submitted = db.relationship('QuizSubmit', backref='quiz', lazy=True)
    tags = db.relationship('Tag', backref='quiz', lazy=True)

# Question Table
class Question(db.Model):
    __tablename__= 'question'
    qid = db.Column(db.String(36), primary_key=True)  # UUID for questions
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    choice1 = db.Column(db.Text)
    choice2 = db.Column(db.Text)
    choice3 = db.Column(db.Text)
    choice4 = db.Column(db.Text)
    answer = db.Column(db.Text)

# UserScore Table
class UserScore(db.Model):
    __tablename__ = 'user_score'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
    max_marks = db.Column(db.Integer)
    marks_got = db.Column(db.Integer)
    total_time = db.Column(db.Integer)  # in seconds
    time_taken = db.Column(db.Integer)  # in seconds

# QuizSubmit Table
class QuizSubmit(db.Model):
    __tablename__ = 'quiz_submit'
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), primary_key=True)
    marks = db.Column(db.Integer)
    taken_time = db.Column(db.Integer)  # in seconds
    submitted_at = db.Column(db.DateTime)

# Tag Table
class Tag(db.Model):
    __tablename__ = 'tag'
    name = db.Column(db.String(50), primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quiz.id'), nullable=False)