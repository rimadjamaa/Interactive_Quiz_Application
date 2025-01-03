from flask import render_template, request, redirect, url_for, flash , session
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import User, db
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        

        # Basic validation
        if not all([email, username, password]):
            flash('All fields are required!', 'danger')
            return render_template('auth/register.html')

        if not "@" in email:
            flash('Email is not valid !', 'danger')
            return render_template('auth/register.html')
        # Check if the user already exists with the same username or email
        existing_user_username = User.query.filter_by(username=username).first()
        existing_user_email = User.query.filter_by(email=email).first()
        if existing_user_username:
            flash("This username already exist !", 'danger')
            return render_template('auth/register.html')
        if existing_user_email:
            flash('This email already exist!', 'danger')
            return render_template('auth/register.html')

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create a new user
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. Please log in.', 'success')
        return redirect(url_for('login'))  # Redirect to login page

    return render_template('auth/register.html')

def login():
  if request.method == 'POST':
    username = request.form.get('username')
    password = request.form.get('password')

    if not username or not password:
      flash('Username and password are required', 'danger')
      return render_template('auth/login.html')

    user = User.query.filter_by(username=username).first()

    if user and check_password_hash(user.password, password):
      session['user_id'] = user.id
      flash('Login successful!', 'success')
      return redirect(url_for('home'))  # Redirect to protected area
    else:
      flash('Login failed. Please check your username and password.', 'danger')
      return render_template('auth/login.html')
  return render_template('auth/login.html')