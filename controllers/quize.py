from flask import render_template

from models.models import Category, Quiz


def allquizes():
    quizzes = Quiz.query.all()  # Fetch all quizzes
    categories = Category.query.all()  # Assuming you have a Category model
    return render_template('all_quizes.html', quizzes=quizzes, categories=categories)