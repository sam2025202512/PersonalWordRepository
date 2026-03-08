"""Resource module for managing words."""
import uuid
from flask import request
from flask_restful import Resource
from wordrepo.models import db, Word, User, PartOfSpeech, Category

def word_to_dict(word):
    """Creates a dictionary for words."""
    return {
        "id": word.id,
        "user_id": word.user_id,
        "text": word.text,
        "language": word.language,
        "part_of_speech_id": word.part_of_speech_id,
        "categories": [c.id for c in word.categories]
    }

class WordListResource(Resource):
    """Handles POST for words."""
    def post(self):
        """Create a new word."""
        data = request.get_json() or {}
        required = ["text", "language", "user_id", "part_of_speech_id"]
        #Check that everything required is given in the data
        if not all(field in data for field in required):
            return {"error": "text, language, user_id and part_of_speech_id are required"}, 400
        #validate user
        if not User.query.get(data["user_id"]):
            return {"error": "user not found"}, 404
        #validate the part of speech
        if not PartOfSpeech.query.get(data["part_of_speech_id"]):
            return {"error": "part_of_speech not found"}, 404
        new_word = Word(
           id=str(uuid.uuid4()),
           user_id = data["user_id"],
           text = data["text"],
           language = data["language"],
           part_of_speech_id = data["part_of_speech_id"]
           )
        #If category has been assigned
        if "category_ids" in data:
            for cid in data["category_ids"]:
                category = Category.query.get(cid)
                if category:
                    new_word.categories.append(category)

        db.session.add(new_word)
        db.session.commit()
        return word_to_dict(new_word), 201

class WordResource(Resource):
    """Handles GET, PUT, DELETE for words."""
    def get(self, word_id):
        """Retrieve a single word."""
        word = Word.query.get(word_id)
        if not word:
            return {"error": "word not found"}, 404
        return word_to_dict(word), 200
    def put(self, word_id):
        """Update a word."""
        word = Word.query.get(word_id)
        if not word:
            return {"error": "word not found"}, 404
        data = request.get_json()
        # check what is changed
        if "text" in data:
            word.text = data["text"]
        if "language" in data:
            word.language = data["language"]
        if "part_of_speech_id" in data:
            if not PartOfSpeech.query.get(data["part_of_speech_id"]):
                return {"error": "part_of_speech not found"}, 404
        word.part_of_speech_id = data["part_of_speech_id"]
        if "category_ids" in data:
            word.categories.clear()
        for cid in data["category_ids"]:
            category = Category.query.get(cid)
            if category:
                word.categories.append(category)
        db.session.commit()
        return word_to_dict(word), 200
    def delete(self, word_id):
        """Delete a word."""
        word = Word.query.get(word_id)
        if not word:
            return {"error": "word not found"}, 404
        db.session.delete(word)
        db.session.commit()
        return{"message": "word deleted"}, 200
