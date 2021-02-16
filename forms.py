from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField
from wtforms.validators import InputRequired, Length


class UserForm(FlaskForm):
    first_name = StringField(
        "First name",
        validators=[
            InputRequired(message="Last name can't be blank"),
            Length(max=30),
        ]
    )
    last_name = StringField(
        "Last name",
        validators=[
            InputRequired(message="Last name can't be blank"),
            Length(max=30)
        ]
    )
    email = StringField(
        "Email",
        validators=[
            InputRequired(message="Email can't be blank"),
        ]
    )
    username = StringField(
        "Username",
        validators=[
            InputRequired(message="Username can't be blank"),
            Length(min=1, max=20),
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Password can't be blank"),
            Length(min=6, max=55),
        ]
    )


class UserLoginForm(FlaskForm):
    username = StringField(
        "Username",
        validators=[
            InputRequired(message="Username can't be blank"),
            Length(min=1, max=20),
        ]
    )
    password = PasswordField(
        "Password",
        validators=[
            InputRequired(message="Password can't be blank"),
            Length(min=6, max=55),
        ]
    )


class FeedbackForm(FlaskForm):
    title = StringField(
        "Title",
        validators=[
            InputRequired(message="title can't be blank"),
        ]
    )
    content = TextAreaField(
        "Content",
        validators=[
            InputRequired(message="content can't be blank"),
        ]
    )