import uuid
from datetime import datetime
from wordrepo.api import db

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
