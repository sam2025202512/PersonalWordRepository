from flask import Flask, json
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime

# ----------------------
# Flask + DB setup
# ----------------------
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///words.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

# ----------------------
# Models
# ----------------------
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    words = db.relationship("Word", back_populates="user", cascade="all, delete-orphan")
    categories = db.relationship("Category", back_populates="user", cascade="all, delete-orphan")

class PartOfSpeech(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(20), unique=True, nullable=False)

    words = db.relationship("Word", back_populates="part_of_speech")

class Category(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)

    user = db.relationship("User", back_populates="categories")
    words = db.relationship("Word", secondary="word_category", back_populates="categories")

class Word(db.Model):
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    text = db.Column(db.String(100), nullable=False)
    language = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    part_of_speech_id = db.Column(db.String(36), db.ForeignKey("part_of_speech.id", ondelete="RESTRICT"), nullable=False)

    user = db.relationship("User", back_populates="words")
    part_of_speech = db.relationship("PartOfSpeech", back_populates="words")
    categories = db.relationship("Category", secondary="word_category", back_populates="words")

# ----------------------
# Join table
# ----------------------
class WordCategory(db.Model):
    __tablename__ = "word_category"
    word_id = db.Column(db.String(36), db.ForeignKey("word.id"), primary_key=True)
    category_id = db.Column(db.String(36), db.ForeignKey("category.id"), primary_key=True)

# ----------------------
# Populate DB if empty
# ----------------------
with app.app_context():
    db.create_all()

    if not User.query.first():
        # Sample user
        user = User(email="test@example.com", password_hash="hashed_password")
        db.session.add(user)
        db.session.commit()

        # Part of Speech
        noun = PartOfSpeech(name="noun")
        verb = PartOfSpeech(name="verb")
        adjective = PartOfSpeech(name="adjective")
        db.session.add_all([noun, verb, adjective])
        db.session.commit()

        # Categories
        animals = Category(name="animals", user_id=user.id)
        colors = Category(name="colors", user_id=user.id)
        db.session.add_all([animals, colors])
        db.session.commit()

        # Words
        word_run = Word(text="run", language="en", user_id=user.id, part_of_speech_id=verb.id)
        word_cat = Word(text="cat", language="en", user_id=user.id, part_of_speech_id=noun.id)
        word_red = Word(text="red", language="en", user_id=user.id, part_of_speech_id=adjective.id)
        db.session.add_all([word_run, word_cat, word_red])
        db.session.commit()

        # Assign categories
        word_run.categories.append(animals)
        word_cat.categories.append(animals)
        word_red.categories.append(colors)
        db.session.commit()
