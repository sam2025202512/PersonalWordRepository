"""Initialize database and insert test data."""

import uuid

from wordrepo.api import create_app, db
from wordrepo.models import User, PartOfSpeech

app = create_app()

with app.app_context():

    # Create all tables
    db.create_all()

    print("Database tables created")

    # Add test user if database empty
    if not User.query.first():

        test_user = User(
            id=str(uuid.uuid4()),
            email="test@example.com",
            password_hash="test123"
        )

        db.session.add(test_user)

        # Default parts of speech
        noun = PartOfSpeech(code="noun", name="Noun")
        verb = PartOfSpeech(code="verb", name="Verb")
        adjective = PartOfSpeech(code="adjective", name="Adjective")

        db.session.add_all([noun, verb, adjective])

        db.session.commit()

        print("Test user and parts of speech added")
        print("User ID:", test_user.id)

    else:
        print("Database already contains data")