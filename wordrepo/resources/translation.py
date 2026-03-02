import uuid
from flask import request
from flask_restful import Resource
from wordrepo.models import db, Translation, Word

def translation_to_dict(t):
  return {
    "id": t.id,
    "word_id": t.word_id,
    "text": t.text,
    "language": t.language,
    "note": t.note
  }

class TranslationListResource(Resource):
  """Handles GET, POST for translations."""
  def get(self, word_id):
    """Return all translations for a given word."""
    word = Word.query.get(word_id)
    if not word:
      return {"error": "word not found"}, 404
    translation = Translation.query.filter_by(word_id=word_id).all()
    return [translation_to_dict(t) for t in translation], 200
  def post(self, word_id):
    """Create a new translation for a given word."""
    word = Word.query.get(word_id)
    if not word:
      return {"error": "word not found"}, 404
    data = request.get_json()
    required = ["text", "language"]
    if not all(field in data for field in required):
      return {"error":"text and language are required"}, 400
    new_translation = Translation(
      id = str(uuid.uuid4()),
      word_id = word_id,
      text = data["text"],
      language = data["language"],
      note = data.get("note")
    )
    db.session.add(new_translation)
    db.session.commit()
    return translation_to_dict(new_translation), 201

class TranslationResource(Resource):
  """Handles GET, PUT, DELETE for translations."""
  def get(self, translation_id):
    """Retrieve a single translation"""
    t = Translation.query.get(translation_id)
    if not t:
      return {"error": "translation not found"}, 404
    return translation_to_dict(t), 200
  def put(self, translation_id):
    """Update a translation"""
    t = Translation.query.get(translation_id)
    if not t:
      return {"error": "translation not found"}, 404
    data = request.get_json()
    if "text" in data:
      t.text = data["text"]
    if "language" in data:
      t.language = data["language"]
    if "note" in data:
      t.note = data["note"]
    db.session.commit()
    return translation_to_dict(t), 200
  def delete(self, translation_id):
    """Delete a translation"""
    t = Translation.query.get(translation_id)
    if not t:
      return {"error": "translation not found"}, 404
    db.session.delete(t)
    db.session.commit()
    return {"message": "translation deletec"}, 200
