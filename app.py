from flask import Flask, redirect, render_template, request, flash, session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from forms import UserForm, UserLoginForm, FeedbackForm
from models import User, db, connect_db, Feedback

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = (
    "postgresql://localhost:5433/flask_feedback_db"
)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "1234-5678"

connect_db(app)
db.drop_all()
db.create_all()


@app.route('/')
def landing_page():
    if 'user_id' in session:
        user_id = session['user_id']
        user = User.query.filter_by(id=user_id).one()
        return redirect(f'/users/{user.username}')

    return render_template('index.html')


@app.route('/register', methods=["GET", "POST"])
def register():
    form = UserForm()
    if form.validate_on_submit():

        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        username = form.username.data
        password = form.password.data

        new_user = User.register(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )

        db.session.add(new_user)

        try:
            db.session.commit()
        except IntegrityError:
            form.email.errors.append('This email alredy exists')
            return render_template('register.html', form=form)

        db.session.commit()
        session['user_id'] = new_user.id

        return redirect(f'/users/{new_user.username}')

    return render_template('register.html', form=form)


@app.route('/users/<username>')
def secret(username):
    if 'user_id' not in session:
        flash("Please login first!", "danger")
        return redirect('/login')

    user = User.query.filter_by(username=username).one()
    form = UserForm(obj=user)

    return render_template('user.html', user=user, form=form)


@app.route('/login', methods=["POST", "GET"])
def login():
    form = UserLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        try:
            User.query.filter_by(username=username).one()
        except NoResultFound:
            flash(f'No user found', 'danger')
            return render_template('login.html', form=form)

        user = User.authenticate(username, password)

        if user:
            session['user_id'] = user.id
            return redirect(f'/users/{username}')
        else:
            form.username.errors = ['Invalid username/password.']

    return render_template('login.html', form=form)


@app.route('/logout')
def logout_user():
    session.pop('user_id')
    return redirect('/')


@app.route('/feedbacks/<username>', methods=["GET", "POST"])
def feedback_create(username):
    form = FeedbackForm()
    user = User.query.filter_by(username=username).one()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        user_id = user.id

        feedback = Feedback(
            title=title,
            content=content,
            user_id=user_id,
        )
        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/users/{username}')

    return render_template(
        'feedback_create.html',
        form=form,
        username=username,
    )


@app.route('/feedbacks/<int:feedback_id>/detail', methods=["GET", "POST"])
def feedback_detail(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).one()

    return render_template(
        'feedback_detail.html',
        feedback=feedback,
        username=feedback.user.username,
    )


@app.route('/feedbacks/<int:feedback_id>/edit', methods=["POST", "GET"])
def feedback_edit(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).one()
    form = FeedbackForm(obj=feedback)
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        feedback.user_id = feedback.user_id

        db.session.add(feedback)
        db.session.commit()

        return redirect(f'/feedbacks/{feedback_id}/detail')
    else:
        return render_template(
            'feedback_edit.html',
            feedback=feedback,
            form=form,
        )


@app.route('/feedbacks/<int:feedback_id>/delete')
def feedback_delete(feedback_id):
    feedback = Feedback.query.filter_by(id=feedback_id).one()
    username = feedback.user.username
    Feedback.query.filter_by(id=feedback_id).delete()
    db.session.commit()

    return redirect(f'/users/{username}')
