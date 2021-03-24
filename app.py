from flask import Flask, redirect, render_template, flash, request,session
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db,db,User, Feedback
from forms import RegisterUser, LoginForm, FeedbackForm


app = Flask(__name__)
app.debug = False
connect_db(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///feedback'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['SQLALCHEMY_ECHO']=False
app.config['SECRET_KEY'] = '<replace with a secret ke1y>'

toolbar = DebugToolbarExtension(app)
db.create_all()

@app.route('/')
def render_homepage():
    return redirect('/register')

@app.route('/register', methods=['GET','POST'])
def register_user():
    if 'curr_user' in session:
        return redirect(f'/users/{session["curr_user"]}')
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
    if 'curr_user' in session:
        return redirect(f'/users/{session["curr_user"]}')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.authenticate(username=form.username.data, password = form.password.data)
        if user:
            session['curr_user'] = user.username
            flash('Logged in successfully!')
            return redirect(f'/users/{user.username}')
        else:
            form.username.errors.append('invalid username or password')
            
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

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    if username == session.get('curr_user'):
        User.query.filter_by(username=username).delete()
        session.pop('curr_user')
        db.session.commit()
        flash('Account deleted successfully')

    else:
        flash('You do not have permission to do that')
    return redirect('/')
# Feedback routes ****************************************************************

@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    if username == session.get('curr_user'):
        form = FeedbackForm()
        if form.validate_on_submit():
            title = form.title.data
            content = form.content.data
            user = session['curr_user']
            feedback = Feedback(title=title,content=content,username=user)
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{user}')
        else:
            return render_template('feedback/add_feedback.html', form=form, title='Add Feedback', btn = 'Add feedback')
    else:
        flash('You do not have permission to do that')
        return redirect('/')

@app.route('/feedback/<int:id>/edit', methods=['POST','GET'])
def edit_feedback(id):
    feedback = Feedback.query.get_or_404(id)
    user = User.query.get_or_404(session.get('curr_user'))
    if feedback in user.feedback:
        form = FeedbackForm(obj = feedback)
        if form.validate_on_submit():
            feedback.title = form.title.data
            feedback.content = form.content.data
            db.session.add(feedback)
            db.session.commit()
            return redirect(f'/users/{session["curr_user"]}')
        return render_template('feedback/add_feedback.html', form=form, title='Edit Feedback', btn = 'Save')
    else:
        return 'beans'


@app.route('/feedback/<int:id>/delete',methods=['POST'])
def delete_feedback(id):
    Feedback.query.filter_by(id=id).delete()
    db.session.commit()
    flash('Feedback deleted successfully')
    return redirect(f'/users/{session["curr_user"]}')
    
    