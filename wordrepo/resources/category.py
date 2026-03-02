from flask import request
from flask_restful import Resource
from wordrepo.models import db, Category, User 
import uuid

def category_to_dict(category):
  return {
    "id": category.id,
    "user_id": category.user_id,
    "name": category.name,
    "words": [w.id for w in category.words]
  }

class CategoryListResource(Resource):
  def post(self):
    """Create a new category."""
    data = request.get_json()
    if not data or "name" not in data or "user_id" not in data:
      return {"error": "name and user_id are required"}, 400
    #validate the user
    user = User.query.get(data["user_id"])
    if not user:
      return {"error": "user not found"}, 404
    new_category = Category(
      id=str(uuid.uuid4()),
      user_id=data["user_id"],
      name=data["name"]
    )
    db.session.add(new_category)
    db.session.commit()
    return category_to_dict(new_category), 201

class CategoryResource(Resource):
  def get(self, category_id):
    """Retrieve a single category"""
    category = Category.query.get(category_id)
    if not category:
      return {"error": "category not found"}, 404
    return category_to_dict(category), 200
  def put(self, category_id):
    """Update a category"""
    category = Category.query.get(category_id)
    if not category:
      return {"error": "category not found"}, 404
    data = request.get_json()
    if "name" in data:
      category.name = data["name"]
    db.session.commit()
    return category_to_dict(category), 200
  def delete(self, category_id):
    """Delete a category."""
    category = Category.query.get(category_id)
    if not category:
      return {"error": "category not found"}, 404
    db.session.delete(category)
    db.session.commit()
    return {"message": "category deleted"}, 200
