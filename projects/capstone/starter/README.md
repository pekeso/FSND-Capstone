## Capstone Project API Documentation

The project is done to complete the capstone project for the Full Stack Nanodegree program.
This is the project documentation

### Project Description
The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. This is a Flask app served by Postgres database.

The project's root folder is: `FSND-Capstone/projects/capstone/starter`

### Prerequesites
When running locally, it's required to run the project in a virtual environment

For example, in Windows one can create a Python virtual environment with this command to be run in PowerShell:

`PS> python -m venv venv`

And in Linux/Unix:

`$ python3 -m venv venv`

You will need to activate the virtual environment `venv` with the following command in PowerShell:

`PS> venv\Scripts\activate`

`(venv) PS>`

and in Linux/Unix:

`$ source venv/bin/activate`

`(venv) $`

The next is to run the shell script with the following command:

`sh setup.sh` or

`chmod +x setup.sh && ./setup`

This will:

- Drop a `casting` database if it exists
- Create a `casting` database
- Initialize the database with some data
- Run the Flask application

### Roles
There are 3 roles: casting assistant, casting director and executive producer

1. The Casting Assistant can:
    - View actors and movies

2. The Casting Director:
    - All permissions a Casting Assistant has
    - Add or delete an actor from the database
    - Modify actors or movies

3. The Executive Producer:
    - All permissions a Casting Director has 
    - Add or delete a movie from the database

### Testing the app

To test the app, one must run the following commands:

- `pip install -r requirements.txt`
- `dropdb casting_test` if the databse `casting_test` exists
- `createdb casting_test`
- `python test_app.py`

Once the test application starts, it asks for the different roles' access tokens.

We paste the appropriate access tokens at each prompt and press enter to validate and execute the test app.


### API Documentation

`GET '/'`   

- This is the public base route
- Request Arguments: None
- Returns: An object with a two keys, `success` that contains a boolean `True` and `message`, that contains a string `Welcome to the Casting Agency API v1.0` .

`GET '/movies'`

- This is a public endpoint
- Fetches a dictionary of movies in which the keys are the movies and the value is the corresponding object of the movie
- Request Arguments: None
- Returns: an array of custom response status, an object with release_date and title

```json
{
  "success": true,
  "movies": [
        {
            "id": 1,
            "release_date": "Wed, 15 Sep 1999 00:00:00 GMT",
            "title": "Fight Club"
        }
    ]
}
```

`GET '/movies-detail'`

- Required permission: `view:movies` 
- Roles allowed: casting assistant, casting director and executive producer
- Fetches a dictionary of movies in which the keys are the movies and the value is the corresponding object of the movie
- Request Arguments: None
- Returns: an array custom response status, an object with 10 paginated questions, total questions, object including all categories, and current category string

```json
{
  "success": true,
  "movies": [
        {
            "id": 1,
            "release_date": "Wed, 15 Sep 1999 00:00:00 GMT",
            "title": "Fight Club",
            "genres": "Action"
        }
    ]
}
```

`POST '/movies'`

- Required permission: `add:movies`
- Roles allowed: executive producer
- Sends a post request in order to add a new movie
- Request Body:

```json
{
    "title": "True Lies",
    "release_date": "1990-04-10",
    "movie_genres": "Action"
}
```
- Returns: a custom response status and the inserted movie object

```json
{
  "success": true,
  "movies": movie
}
```

`PATCH '/movies/<id>'`

- Required permission: `edit:movies`
- Roles allowed: casting director, executive producer
- Request Arguments: `id` - integer 
- Sends a patch request in order to edit an existing movie
- Request Body:

```json
{
    "release_date": "1994-04-10"
}
```
- Returns: a custom response status and the updated movie object

```json
{
  "success": true,
  "movies": movie
}
```

`DELETE '/movies/<id>'`

- Required permission: `delete:movies`
- Roles allowed: executive producer
- Request Arguments: `id` - integer
- Deletes an existing movie record if it exists
- Returns: a custom response status and the deleted movie id

```json
{
  "success": true,
  "deleted": id
}
```

`GET '/actors'`

- This is a public endpoint
- Fetches a dictionary of actors in which the keys are the actors and the value is the corresponding object of the actor
- Request Arguments: None
- Returns: an array of custom response status, an object with id, age, gender, and name

```json
{
  "success": true,
  "actors": [
        {
            "id": 1,
            "age": 58,
            "gender": "Male",
            "name": "Brad Pitt"
        }
    ]
}
```

`GET '/actors-detail'`

- Required permission: `'view:actors'`
- Roles allowed: casting assistant, casting director, executive producer
- Fetches a dictionary of actors in which the keys are the actors and the value is the corresponding object of the actor
- Request Arguments: None
- Returns: an array of custom response status, an object with id, age, gender, name and nationality

```json
{
  "success": true,
  "actors": [
        {
            "id": 1,
            "age": 58,
            "gender": "Male",
            "name": "Brad Pitt",
            "nationality": "American"
        }
    ]
}
```

`POST '/actors'`

- Required permission: `'add:actors'`
- Roles allowed: casting director, executive producer
- Sends a post request in order to add a new actor
- Request Body:

```json
{
    "name": "Chuck Norris",
    "age": 69,
    "gender": "male",
    "nationality": "American"
}
```
- Returns: a custom response status and the inserted actor object

```json
{
  "success": true,
  "actors": actor
}
```

`PATCH '/actors/<id>'`

- Required permission: `edit:actors`
- Roles allowed: casting director, executive producer
- Request Arguments: `id` - integer 
- Sends a patch request in order to edit an existing actor
- Request Body:

```json
{
    "age": 82
}
```
- Returns: a custom response status and the updated actor object

```json
{
  "success": true,
  "actors": actor
}
```

`DELETE '/actors/<id>'`

- Required permission: `delete:actors`
- Roles allowed: casting director, executive producer
- Request Arguments: `id` - integer
- Deletes an existing actor record if it exists
- Returns: a custom response status and the deleted actor id

```json
{
  "success": true,
  "deleted": id
}


