from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restful import Api

db = SQLAlchemy()

def create_app():
  app = Flask(__name__)
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///words.db"
  app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

  db.init_app(app)
  api = Api(app)

  #import resources
  from wordrepo.resources.user import UserListResource, UserResource
  from wordrepo.resources.word import WordListResource, WordResource
  from wordrepo.resources.translation import TranslationListResource, TranslationResource
  from wordrepo.resources.category import CategoryListResource, CategoryResource
  from wordrepo.resources.part_of_speech import PartOfSpeechListResource
  from wordrepo.resources.quiz import QuizListResource, QuizResource

  #User endpoints
  api.add_resource(UserListResource, "/users")
  api.add_resource(UserResource, "/users/<string:user_id>")
  #Word endpoints
  api.add_resource(WordListResource, "/words")
  api.add_resource(WordResource, "/words/<string:word_id>")
  #Translation endpoints
  api.add_resource(TranslationListResource, "/words/<string:word_id>/translations")
  api.app_resource(TranslationResource, "/translations/<string:translation_id>")
  return app
