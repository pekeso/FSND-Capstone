import os
import DateTime as dt
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from flask_migrate import Migrate


load_dotenv()

environment = os.environ['DEV']

# is_aws = True if os.environ.get("AWS_DEFAULT_REGION") else False

if envrionment is not 'Local':
    database_path = 'postgresql://{username}:{password}@{host}:{port}/{database}'.format(
            username=os.environ['POSTGRES_USERNAME'],
            password=os.environ['POSTGRES_PASSWORD'],
            host=os.environ['POSTGRES_HOST'],
            port=os.environ['POSTGRES_PORT'],
            database=os.environ['POSTGRES_DATABASE'],
        )
    print('aws')
else:
    database_path = "postgresql://{host}/{database}".format(host=os.environ['DATABASE_HOST'], database=os.environ['DATABASE_NAME'])
    print('local')

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()


class Movie(db.Model):
    __tablename__ = 'movies'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    release_date = db.Column(db.DateTime)
    genres = db.Column(db.String(120))

    def __init__(self, title, release_date, genres):
        self.title = title
        self.release_date = release_date
        self.genres = genres

    '''
    insert()
        inserts a new model into a database
        the model must have a title
        the model must have a release date
        the model can have a genres
        EXAMPLE
            movie = Movie(title=req_title, release_date=req_release_date, genres=genres)
            movie.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model from a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            movie.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a model into a database
        the model must exist in the database
        EXAMPLE
            movie = Movie.query.filter(Movie.id == id).one_or_none()
            Movie.title = 'Avengers: End Game'
            movie.update()
    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }

    def detail(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'genres': self.genres
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(30), nullable=False)
    nationality = db.Column(db.String(120))

    def __init__(self, name, age, gender, nationality):
        self.name = name
        self.age = age
        self.gender = gender
        self.nationality = nationality

    '''
    insert()
        inserts a new model into a database
        the model must have a name
        the model must have an age
        the model must have a gender
        the model can have a nationality
        EXAMPLE
            actor = Actor(name=req_name, age=req_age, gender=req_gender, nationality=nationality)
            actor.insert()
    '''

    def insert(self):
        db.session.add(self)
        db.session.commit()

    '''
    delete()
        deletes a model from a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            actor.delete()
    '''

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    '''
    update()
        updates a model into a database
        the model must exist in the database
        EXAMPLE
            actor = Actor.query.filter(Actor.id == id).one_or_none()
            Actor.name = 'Tommy Lee Jones'
            actor.update()
    '''

    def update(self):
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }

    def detail(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'nationality': self.nationality
        }