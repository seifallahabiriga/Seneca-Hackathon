import os

from flask_sqlalchemy import SQLAlchemy
db=SQLAlchemy()
class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') 
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres:postgres@localhost/match_analysis'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
