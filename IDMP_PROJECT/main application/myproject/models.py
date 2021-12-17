from myproject import db,login_manager
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin

# We obtain access to a variety of built-in attributes by inheriting the UserMixin.
# which we will be able to call in our views!
# is_authenticated()
# is_active()
# is_anonymous()
# get_id()


# The user_loader decorator allows flask-login to load the current user and grab their id.
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

####################################################################
### Each of the class in this code represents the database tabels###
####################################################################

class User(db.Model, UserMixin):

    # Create a table in the db
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key = True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True, index=True)

    password = db.Column(db.String(128))
    admin_check = db.Column(db.String(128))
    booking = db.relationship('Booking',backref='users',lazy='dynamic')

    def __init__(self, email, username, password):
        self.email = email
        self.username = username

        self.password = password


    #Checks if the password entered while loggin in is the same as password while registering
    def check_password(self,password):
        return self.password==password


####################################################################
### actor_in_movie, director_in_movie are relational tables that
### are used to make relations between actor and movie table,
### director and movie table respectively
####################################################################

actor_in_movie = db.Table('actor_in_movie', db.Column('actor_id',db.Integer, db.ForeignKey('actor.actor_id')),
                            db.Column('movie_id',db.Integer, db.ForeignKey('movie.movie_id')))

director_in_movie = db.Table('director_in_movie', db.Column('director_id',db.Integer, db.ForeignKey('director.director_id')),
                            db.Column('movie_id',db.Integer, db.ForeignKey('movie.movie_id')))

class Movie(db.Model):

    __tablename__ = 'movie'
    movie_id = db.Column(db.Integer,primary_key = True)
    movie_name = db.Column(db.Text)
    movie_release_year = db.Column(db.Text)
    movie_rating = db.Column(db.Float)
    movie_status = db.Column(db.Text)
    movie_genre = db.Column(db.Text)
    actor = db.relationship('Actor',secondary=actor_in_movie, backref = db.backref('movie_act',lazy = 'dynamic'),lazy = 'dynamic')
    director = db.relationship('Director',secondary=director_in_movie, backref = db.backref('movie_dir',lazy = 'dynamic'),lazy = 'dynamic')
    schedule = db.relationship('Schedule',backref='movie',lazy='dynamic')
    booking = db.relationship('Booking',backref='movie1',lazy='dynamic')

class Schedule(db.Model):

    __tablename__ = 'schedule'
    schedule_id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.Date, nullable=False)
    time = db.Column(db.Time,nullable = False)
    seats = db.Column(db.Integer, default=100)

    movie_id = db.Column(db.Integer,db.ForeignKey('movie.movie_id'))
    book = db.relationship('Booking',backref='schedule',lazy='dynamic')


class Actor(db.Model):

    __tablename__ = 'actor'

    actor_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)



class Director(db.Model):

    __tablename__ = 'director'

    director_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.Text)

class Confirmation(db.Model):

    _tablename__ = 'confirmation'

    confirmation_id = db.Column(db.Integer, primary_key = True)
    user_id =  db.Column(db.Integer)
    confirmed = db.Column(db.Text)











class Booking(db.Model):

    __tablename__ = 'booking'
    booking_id = db.Column(db.Integer,primary_key = True)

    movie_id = db.Column(db.Integer,db.ForeignKey('movie.movie_id'))
    schedule_id = db.Column(db.Integer,db.ForeignKey('schedule.schedule_id'))
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))
