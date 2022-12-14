from models import db
from models import Movie, Actor
from app import app

with app.app_context():
    db.create_all()

    if Movie.query.count() == 0:
        movies = [
            Movie(title='Fight Club', release_date='1999-09-15', genres='Action'),
            Movie(title='The Matrix', release_date='1999-03-31', genres='Action'),
            Movie(title='Donnie Darko', release_date='2001-01-19', genres='Drama'),
            Movie(title='Inception', release_date='2010-07-16', genres='Action'),
        ]

        for movie in movies:
            db.session.add(movie)

        db.session.commit()

    if Actor.query.count() == 0:
        actors = [
            Actor(name='Brad Pitt', age='58', gender='Male', nationality='American'),
            Actor(name='Keanu Reeves', age='58', gender='Male', nationality='American'),
            Actor(name='Jake Gyllenhaal', age='41', gender='Male', nationality='American'),
            Actor(name='Leonardo DiCaprio', age='48', gender='Male', nationality='American'),
        ]

        for actor in actors:
            db.session.add(actor)

        db.session.commit()