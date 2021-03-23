from flask import Flask, redirect, render_template, flash, request,session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db,db,User, Feedback
from forms import RegisterUser, LoginForm


app = Flask(__name__)
app.debug = True
connect_db(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=False
app.config['SECRET_KEY'] = '<replace with a secret key>'

toolbar = DebugToolbarExtension(app)
db.create_all()

@app.route('/')
def render_homepage():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_user():
    form = RegisterUser()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name = last_name)
        db.session.add(new_user)
        db.session.commit()
        session['curr_user'] = new_user.username
        flash('Account created!')
        return redirect(f'/users/{new_user.username}')
    return render_template('register.html', form = form)

@app.route('/login', methods =['GET','POST'])
def login_user():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password = form.password.data)
        session['curr_user'] = user.username
        flash('Logged in successfully!')
        return redirect(f'/users/{user.username}')
    return render_template('login.html',form = form)

@app.route('/logout')
def logout_user():
    session.pop('curr_user')
    flash('Successfully logged out.')
    return redirect('/')

@app.route('/users/<username>')
def show_user_details(username):
    if username != session.get('curr_user'):
        flash(f"Login as {username} to access that page")
        return redirect('/')
    else:
        user = User.query.get(username)
        return render_template('user.html', user = user)

# Feedback routes ****************************************************************


@app.route('/feedback/<int:id>/delete',methods='POST')
def delete_feedback(id):
    Feedback.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Feedback deleted successfully')
    return redirect(f'/users/{session["curr_user].username')
    
    