from application.config import db

class Tweet(db.Model):
    __tablename__ = 'tweets_match' 
    id = db.Column(db.Integer, primary_key=True)
    minute_int = db.Column(db.Integer, nullable=False)
    timestamp = db.Column(db.String(10))
    text = db.Column(db.Text, nullable=False)
