from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    notes = db.relationship('Note')
    quiz_results = db.relationship('QuizResult', backref='user', lazy=True)
    total_score_it = db.Column(db.Integer, default=0)
    total_score_de = db.Column(db.Integer, default=0)
    total_score_fr = db.Column(db.Integer, default=0)
    total_score_en = db.Column(db.Integer, default=0)
    total_score_es = db.Column(db.Integer, default=0)

class QuizResult(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    date = db.Column(db.DateTime(timezone=True), default=func.now())


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_text = db.Column(db.String(500))
    option_a = db.Column(db.String(200))
    option_b = db.Column(db.String(200))
    option_c = db.Column(db.String(200))
    correct_option = db.Column(db.String(2))  # Correct option among 'a', 'b', 'c'
    language = db.Column(db.String(50))  # To distinguish between languages
    qtype = db.Column(db.String(50))  # subject of question
    difficulty = db.Column(db.Integer)  # diffi 1-3

class Answered(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    correct = db.Column(db.Integer)  # 1 for correct, 0 for incorrect
    qlang = db.Column(db.String(20))  # question language
    date = db.Column(db.DateTime(timezone=True), default=func.now())

class Answeredagg(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    icount = db.Column(db.Integer)  # 1 for correct, 0 for incorrect
    icountcorrect = db.Column(db.Integer)  # 1 for correct, 0 for incorrect
    correctpct = db.Column(db.Integer)  # 1 for correct, 0 for incorrect
    qlang = db.Column(db.String(20))  # question language
    qtype = db.Column(db.String(20))  # question language
    difficulty = db.Column(db.String(20))  # question language
    date = db.Column(db.DateTime(timezone=True), default=func.now())

