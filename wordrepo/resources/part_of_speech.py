"""Resource module for managing parts of speech."""
import uuid
from flask import request
from flask_restful import Resource
from wordrepo.models import db, PartOfSpeech

def pos_to_dict(pos):
    """Creates a dictionary for part of speech."""
    return {
      "id": pos.id,
      "name": pos.name,
      "words": [w.id for w in pos.words]
    }

class PartOfSpeechListResource(Resource):
    """Handles GET, POST for pos."""
    def get(self):
        """Return all parts of speech"""
        parts = PartOfSpeech.query.all()
        return [pos_to_dict(p) for p in parts], 200
    def post(self):
        """Create a new part of speech."""
        data = request.get_json()
        # check for requirements
        if not data or "name" not in data:
            return {"error": "name is required"}, 400
        #check if name already exists
        if PartOfSpeech.query.filter_by(name=data["name"]).first():
            return {"error": "part of speech already exists"}, 409
        new_pos = PartOfSpeech(
            id=str(uuid.uuid4()),
            name=data["name"]
        )
        db.session.add(new_pos)
        db.session.commit()
        return pos_to_dict(new_pos), 201

class PartOfSpeechResource(Resource):
    """Handles PUT, DELETE for pos."""
    def put(self, pos_id):
        """Update a part of speech."""
        pos = PartOfSpeech.query.get(pos_id)
        if not pos:
            return {"error": "part of speech not found"}, 404
        data = request.get_json()
        if "name" in data:
            pos.name = data["name"]
        db.session.commit()
        return pos_to_dict(pos), 200
    def delete(self, pos_id):
        """Delete a part of speech."""
        pos = PartOfSpeech.query.get(pos_id)
        if not pos:
            return {"error": "part of speech not found"}, 404
        db.session.delete(pos)
        db.session.commit()
        return {"message": "part of speech deleted"}, 200
