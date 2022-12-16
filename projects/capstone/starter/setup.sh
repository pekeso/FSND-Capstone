#!/bin/sh

# delete database
dropdb casting

# create database
createdb casting 

# initialize database with data
python init_db.py

# run the flask app
python app.py
