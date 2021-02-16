from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

db = SQLAlchemy()

bcrypt = Bcrypt()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)


class Feedback(db.Model):
    __tablename__ = "feedbacks"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
    )
    title = db.Column(
        db.Text,
        primary_key=True,
        nullable=False
    )
    content = db.Column(
        db.Text,
        nullable=False
    )
    user = db.relationship(
        'User',
        backref="feedbacks"
    )
    user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
    )


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True,
        unique=True,
    )
    username = db.Column(
        db.Text,
        unique=True,
        nullable=False,
    )
    password = db.Column(
        db.Text,
        nullable=False
    )
    email = db.Column(
        db.String(50),
        nullable=False,
        unique=True,
    )
    first_name = db.Column(
        db.String(30),
        nullable=False,
    )
    last_name = db.Column(
        db.String(30),
        nullable=False,
    )

    @classmethod
    def register(cls, username, password, email, first_name, last_name):
        """Register user w/hashed password & return user."""

        hashed = bcrypt.generate_password_hash(password)
        hashed_utf8 = hashed.decode("utf8")

        return cls(
            username=username,
            password=hashed_utf8,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = User.query.filter_by(username=username).first()

        if user and bcrypt.check_password_hash(user.password, password):
            return user
        else:
            return False

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}'
