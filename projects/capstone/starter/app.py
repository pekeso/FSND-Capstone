import os
from flask import Flask, request, abort, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
from flask_cors import CORS
from models import setup_db, Movie, Actor
from auth import AuthError, requires_auth


def create_app(test_config=None):
    app = Flask(__name__)
    with app.app_context():
        setup_db(app)


    CORS(app, resources={r"/*": {"origins": "*"}})

    

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        response.headers.add(
            "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
        )
        response.headers.add(
            "Access-Control-Allow-Methods", "GET,PUT,POST,DELETE,OPTIONS"
        )
        return response

    # Routes
    @app.route('/')
    def health():
        return jsonify({
            "success": True,
            "message": "Welcome to the Casting Agency API v1.0"
        })

    # -----------------------------------------------------------------------
    #                                 Movies                                |
    # -----------------------------------------------------------------------
    '''
        GET /movies
            it's a public endpoint
        returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies')
    def get_movies():
        movies = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in movies]

        if len(movies) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "movies": movies
        })

    '''
        GET /movies-detail
            requires the 'get:movies-detail' permission
        returns status code 200 and json {"success": True, "movies": movies} where movies is the list of movies
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies-detail')
    @requires_auth('view:movies')
    def get_movies_detail(jwt):
        movies = Movie.query.order_by(Movie.id).all()
        movies = [movie.detail() for movie in movies]

        if len(movies) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "movies": movies
        })

    '''
        POST /movies
            creates a new row in the movies table
            requires the 'add:movies' permission
        returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the newly created movie
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies', methods=['POST'])
    @requires_auth('add:movies')
    def create_movie(jwt):
        body = request.get_json()

        new_title = body.get('title', None)
        new_release_date = body.get('release_date', None)
        new_genres = body.get('genres', None)
        
        try:
            movie = Movie(title=new_title, release_date=new_release_date, genres=new_genres)
            
            movie.insert()
            movie = [movie.detail()]

            return jsonify({
                'success': True,
                'movies': movie
            })
        except:
            abort(422)

    '''
        PATCH /movies/<id>
            where <id> is the existing model id
            responds with a 404 error if <id> is not found
            updates the corresponding row for <id>
            requires the 'edit:movies' permission
            it contains the movie.format() data representation
        returns status code 200 and json {"success": True, "movies": movie} where movie an array containing only the updated movie
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<id>', methods=['PATCH'])
    @requires_auth('edit:movies')
    def edit_movie(jwt, id):

        body = request.get_json()

        try:
            movie = Movie.query.filter(Movie.id==int(id)).one_or_none()

            if movie is None:
                abort(404)

            if 'title' in body:
                movie.title = str(body.get('title'))
            if 'release_date' in body:
                movie.release_date = str(body.get('release_date'))
            
            movie.update()
            movie = [movie.detail()]

            return jsonify({
                'success': True,
                'movies': movie
            })

        except:
            abort(422)

    '''
        DELETE /movies/<id>
            where <id> is the existing model id
            responds with a 404 error if <id> is not found
            deletes the corresponding row for <id>
            requires the 'delete:movies' permission
        returns status code 200 and json {"success": True, "deleted": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/movies/<id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, id):

        try:
            movie = Movie.query.filter(Movie.id==int(id)).one_or_none()

            if movie is None:
                abort(404)

            movie.delete()

            return jsonify({
                'success': True,
                'deleted': int(id)
            })
        except:
            abort(422)

    # -----------------------------------------------------------------------
    #                                 Actors                                |
    # -----------------------------------------------------------------------
    '''
        GET /actors
            it's a public endpoint
        returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors')
    def get_actors():
        actors = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in actors]

        if len(actors) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "actors": actors
        })

    '''
        GET /actors-detail
            requires the 'get:actors-detail' permission
        returns status code 200 and json {"success": True, "actors": actors} where actors is the list of actors
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors-detail')
    @requires_auth('view:actors')
    def get_actors_detail(jwt):
        actors = Actor.query.order_by(Actor.id).all()
        actors = [actor.detail() for actor in actors]

        if len(actors) == 0:
            abort(404)

        return jsonify({
            "success": True,
            "actors": actors
        })

    '''
        POST /actors
            creates a new row in the actors table
            requires the 'add:actors' permission
        returns status code 200 and json {"success": True, "actors": actors} where actor an array containing only the newly created actor
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors', methods=['POST'])
    @requires_auth('add:actors')
    def create_actor(jwt):
        body = request.get_json()

        new_name = body.get('name', None)
        new_age = body.get('age', None)
        new_gender = body.get('gender', None)
        new_nationality = body.get('nationality', None)

        try:
            actor = Actor(name=new_name, age=new_age, gender=new_gender, nationality=new_nationality)

            actor.insert()  
            actor = [actor.detail()]

            return jsonify({
                'success': True,
                'actors': actor
            })

        except:
            abort(422)

    '''
        PATCH /actors/<id>
            where <id> is the existing model id
            responds with a 404 error if <id> is not found
            updates the corresponding row for <id>
            requires the 'edit:actors' permission
            it contains the actor.format() data representation
        returns status code 200 and json {"success": True, "actors": actor} where actor an array containing only the updated actor
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<id>', methods=['PATCH'])
    @requires_auth('edit:actors')
    def edit_actor(jwt, id):
        body = request.get_json()

        try:
            actor = Actor.query.filter(Actor.id == int(id)).one_or_none()

            if actor is None:
                abort(404)

            if 'name' in body:
                actor.name = str(body.get('name'))
            if 'age' in body:
                actor.age = int(body.get('age'))
            if 'gender' in body:
                actor.gender = str(body.get('gender'))

            actor.update()
            actor = [actor.format()]

            return jsonify({
                'success': True,
                'actors': actor
            })

        except:
            abort(422)


    '''
        DELETE /actors/<id>
            where <id> is the existing model id
            responds with a 404 error if <id> is not found
            deletes the corresponding row for <id>
            requires the 'delete:actors' permission
        returns status code 200 and json {"success": True, "deleted": id} where id is the id of the deleted record
            or appropriate status code indicating reason for failure
    '''
    @app.route('/actors/<id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, id):
        try:
            actor = Actor.query.filter(Actor.id == int(id)).one_or_none()

            if actor is None:
                abort(404)

            actor.delete()

            return ({
                'success': True,
                'deleted': int(id)
            })

        except:
            abort(422)

    # Error handling

    @app.errorhandler(401)
    def unauthorized_error(error):
        return jsonify({
            "success": False,
            "error": 401,
            "message": "Oops! Access denied! Please make sure you login first"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "success": False,
            "error": 403,
            "message": "Unfortunately, you do not have permission to complete this task!"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    return app

app = create_app()


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
    