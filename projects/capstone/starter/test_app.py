import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from flask import Flask
from flask_cors import CORS
from auth import AuthError, requires_auth

from models import setup_db, Movie, Actor
from app import create_app

print("Please enter the casting assistant authentication token:")
casting_assistant_token = 'Bearer ' + input()
casting_assistant_headers = {'Authorization': casting_assistant_token}

print("Please enter the casting director authentication token:")
casting_director_token = 'Bearer ' + input()
casting_director_headers = {'Authorization': casting_director_token}

print("Please enter the executive producer authentication token:")
producer_token = 'Bearer ' + input()
producer_headers = {'Authorization': producer_token}

class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.app.debug = True
        self.client = self.app.test_client
        self.database_name = "casting_test"
        self.database_path = "postgresql://{}/{}".format('localhost:5432', self.database_name)
        
        with self.app.app_context():
            setup_db(self.app, self.database_path)
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

        self.new_movie = {
            'title': 'Madagascar',
            'release_date': '2005-06-23',
            'genres': 'Animé'
        }

        self.updated_movie = {
            'title': 'The Penguins of Madagascar',
            'release_date': '2006-06-02',
        }

        self.bad_movie = {
            'title': 'Casablanca',
            'release_date': 1949
        }

        self.new_actor = {
            'name': 'Chuck Norris',
            'age': 69,
            'gender': 'male',
            'nationality': 'American'
        }

        self.updated_actor = {
            'name': 'Ryan Reynolds',
            'age': 40,
            'gender': 'male'
        }

        self.bad_actor = {
            'name': 'Chuck Norris',
            'age': 69
        }

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    Test for unsuccessful unauthenticated retrieve of movies
    """
    def test000_404_get_movies_public(self):
        res = self.client().get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")

    """
    Test for unsuccessful authenticated retrieve of movies by casting assistant
    """
    def test001_404_get_movies_authenticated(self):
        res = self.client().get("/movies-detail", headers=casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")

    """
    Test to add new movie by producer
    """
    def test002_create_new_movie(self):
        res = self.client().post("/movies", json=self.new_movie, headers=producer_headers)
        data = json.loads(res.data)
        pass

    """
    Test for successful authenticated retrieve of actors by casting assistant
    """
    def test003_get_movies_authenticated(self):
        res = self.client().get("/movies-detail", headers=casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    """
    Test to update new movie by producer
    """
    def test004_update_new_movie(self):
        res = self.client().patch("/movies/1", json=self.updated_movie, headers=casting_director_headers)
        data = json.loads(res.data)
        pass

    """
    Test for successful resource deletion
    """
    def test005_delete_movie(self):
        res = self.client().delete('/movies/1', headers=producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    """
    Test for deletion of non existing resource
    """
    def test006_404_if_movie_does_not_exist(self):
        res = self.client().delete("/movies/10", headers=producer_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    """
    Test to add new movie by casting director: unsuccessful
    """
    def test007_422_create_new_movie(self):
        res = self.client().post("/movies", json=self.bad_movie, headers=producer_headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "unprocessable")

    # --------------------------------------------------
    """
    Test for unsuccessful unauthenticated retrieve of actors
    """
    def test008_404_get_actors_public(self):
        res = self.client().get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")

    """
    Test for unsuccessful authenticated retrieve of movies by casting assistant
    """
    def test009_404_get_actors_authenticated(self):
        res = self.client().get("/actors-detail", headers=casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "resource not found")

    """
    Test to add new actor by casting director
    """
    def test010_create_new_actor(self):
        res = self.client().post("/actors", json=self.new_actor, headers=casting_director_headers)
        data = json.loads(res.data)
        pass

    """
    Test for successful authenticated retrieve of actors by casting assistant
    """
    def test011_get_actors_authenticated(self):
        res = self.client().get("/actors-detail", headers=casting_assistant_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    """
    Test to update new actor by producer
    """
    def test012_update_new_actor(self):
        res = self.client().patch("/actors/1", json=self.updated_actor, headers=casting_director_headers)
        data = json.loads(res.data)
        pass

    """
    Test for successful resource deletion
    """
    def test013_delete_actor(self):
        res = self.client().delete('/actors/1', headers=casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['deleted'], 1)

    """
    Test for deletion of non existing resource
    """
    def test014_404_if_actor_does_not_exist(self):
        res = self.client().delete("/actors/10", headers=casting_director_headers)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    """
    Test to add new actor by casting director: unsuccessful
    """
    def test015_422_create_new_actor(self):
        res = self.client().post("/actors", json=self.bad_actor, headers=casting_director_headers)
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "unprocessable")
    

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
