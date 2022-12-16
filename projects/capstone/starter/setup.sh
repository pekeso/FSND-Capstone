#!/bin/sh

# Install dependencies
pip install -r requirements.txt

# delete database
dropdb casting

# create database
createdb casting 

# initialize database with data
python init_db.py

# run the flask app
python app.py
