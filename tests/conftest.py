import pytest
from wordrepo.api import create_app, db

@pytest.fixture
def app():
  app = create_app()
  app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
  app.config["TESTING"] = True
  with app.app_context():
    db.create_all()
    yield app
    db.drop_all()

@pytest.fixture
def client(app):
  return app.test_client()

@pytest.fixture
def db_session(app):
  with app.app_context():
    yield db.session
