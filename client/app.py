"""Flask client application for Personal Word Repository."""
from __future__ import annotations

import os
from collections import Counter

from flask import Flask, flash, redirect, render_template, request, session, url_for

from client.services import (
    ClientServiceError,
    check_quiz,
    create_category,
    create_quiz,
    create_translation,
    create_word,
    delete_category,
    delete_translation,
    delete_word,
    get_categories,
    get_parts_of_speech,
    get_translations,
    get_user,
    get_word,
    get_words,
    register_user,
    update_word,
)


def create_app():
    """Create and configure the client application."""
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("PWR_CLIENT_SECRET", "pwr-client-secret")

    def current_user():
        """Return the currently selected user if available."""
        user_id = session.get("user_id")
        if not user_id:
            return None
        return {
            "id": user_id,
            "email": session.get("user_email", "Unknown user")
        }

    def require_user():
        """Redirect to home if no user is active."""
        user = current_user()
        if not user:
            flash("Choose or create a workspace profile first.", "warning")
            return None
        return user

    def decorate_words(words, categories_by_id):
        """Attach category names and translation counts to word items."""
        decorated = []
        for word in words:
            translations = get_translations(word["id"])
            category_names = [
                categories_by_id.get(category_id, {"name": "Unknown"})["name"]
                for category_id in word["categories"]
            ]
            decorated.append({
                **word,
                "translation_count": len(translations),
                "category_names": category_names
            })
        return decorated

    @app.errorhandler(ClientServiceError)
    def handle_service_error(error):
        """Render a friendly error page for downstream API problems."""
        return render_template(
            "service_error.html",
            user=current_user(),
            message=str(error),
            status_code=error.status_code
        ), 502

    @app.route("/")
    def home():
        """Render the start page."""
        if current_user():
            return redirect(url_for("dashboard"))
        return render_template("home.html")

    @app.post("/register")
    def register():
        """Create a workspace profile through the API."""
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "").strip()
        if not email or not password:
            flash("Email and password are required.", "error")
            return redirect(url_for("home"))

        try:
            user = register_user(email, password)
        except ClientServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("home"))

        session["user_id"] = user["id"]
        session["user_email"] = user["email"]
        flash("Workspace profile created successfully.", "success")
        return redirect(url_for("dashboard"))

    @app.post("/connect")
    def connect():
        """Connect the client to an existing user profile."""
        user_id = request.form.get("user_id", "").strip()
        if not user_id:
            flash("Enter a valid user id.", "error")
            return redirect(url_for("home"))

        try:
            user = get_user(user_id)
        except ClientServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("home"))

        session["user_id"] = user["id"]
        session["user_email"] = user["email"]
        flash("Connected to your existing workspace.", "success")
        return redirect(url_for("dashboard"))

    @app.post("/logout")
    def logout():
        """Clear the active user session."""
        session.clear()
        flash("Workspace disconnected.", "success")
        return redirect(url_for("home"))

    @app.route("/dashboard")
    def dashboard():
        """Render an overview dashboard for the active user."""
        user = require_user()
        if not user:
            return redirect(url_for("home"))

        categories = get_categories(user["id"])
        categories_by_id = {category["id"]: category for category in categories}
        words = decorate_words(get_words(user["id"]), categories_by_id)
        language_breakdown = Counter(word["language"] for word in words)
        missing_translation_count = sum(1 for word in words if word["translation_count"] == 0)

        return render_template(
            "dashboard.html",
            user=user,
            words=words[:5],
            total_words=len(words),
            total_categories=len(categories),
            missing_translation_count=missing_translation_count,
            language_breakdown=language_breakdown.most_common()
        )

    @app.route("/words")
    def words():
        """Show the word library view."""
        user = require_user()
        if not user:
            return redirect(url_for("home"))

        search = request.args.get("search", "").strip()
        language = request.args.get("language", "").strip()
        category_id = request.args.get("category_id", "").strip()

        categories = get_categories(user["id"])
        categories_by_id = {category["id"]: category for category in categories}
        words_data = decorate_words(
            get_words(user["id"], search=search, language=language, category_id=category_id),
            categories_by_id
        )
        parts_of_speech = get_parts_of_speech()
        languages = sorted({word["language"] for word in get_words(user["id"])})

        return render_template(
            "words.html",
            user=user,
            words=words_data,
            categories=categories,
            parts_of_speech=parts_of_speech,
            selected_category_id=category_id,
            selected_language=language,
            search=search,
            languages=languages
        )

    @app.post("/words")
    def create_word_action():
        """Create a word from form data."""
        user = require_user()
        if not user:
            return redirect(url_for("home"))

        category_ids = request.form.getlist("category_ids")
        payload = {
            "text": request.form.get("text", "").strip(),
            "language": request.form.get("language", "").strip(),
            "part_of_speech_id": int(request.form.get("part_of_speech_id", "0") or 0),
            "user_id": user["id"],
            "category_ids": category_ids
        }
        if not payload["text"] or not payload["language"] or not payload["part_of_speech_id"]:
            flash("Text, language and part of speech are required.", "error")
            return redirect(url_for("words"))

        try:
            create_word(payload)
        except ClientServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("words"))

        flash("Word created successfully.", "success")
        return redirect(url_for("words"))

    @app.route("/words/<word_id>")
    def word_detail(word_id):
        """Show a single word and its translations."""
        user = require_user()
        if not user:
            return redirect(url_for("home"))

        word = get_word(word_id)
        translations = get_translations(word_id)
        categories = get_categories(user["id"])
        categories_by_id = {category["id"]: category for category in categories}
        parts_of_speech = get_parts_of_speech()

        return render_template(
            "word_detail.html",
            user=user,
            word=word,
            translations=translations,
            categories=categories,
            category_names=[
                categories_by_id.get(category_id, {"name": "Unknown"})["name"]
                for category_id in word["categories"]
            ],
            parts_of_speech=parts_of_speech
        )

    @app.post("/words/<word_id>/update")
    def update_word_action(word_id):
        """Update a word from the detail screen."""
        payload = {
            "text": request.form.get("text", "").strip(),
            "language": request.form.get("language", "").strip(),
            "part_of_speech_id": int(request.form.get("part_of_speech_id", "0") or 0),
            "category_ids": request.form.getlist("category_ids")
        }
        try:
            update_word(word_id, payload)
        except ClientServiceError as error:
            flash(str(error), "error")
        else:
            flash("Word updated.", "success")
        return redirect(url_for("word_detail", word_id=word_id))

    @app.post("/words/<word_id>/delete")
    def delete_word_action(word_id):
        """Delete a word and return to the library view."""
        try:
            delete_word(word_id)
        except ClientServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("word_detail", word_id=word_id))
        flash("Word deleted.", "success")
        return redirect(url_for("words"))

    @app.post("/words/<word_id>/translations")
    def create_translation_action(word_id):
        """Create a translation from form data."""
        payload = {
            "text": request.form.get("text", "").strip(),
            "language": request.form.get("language", "").strip(),
            "note": request.form.get("note", "").strip() or None
        }
        try:
            create_translation(word_id, payload)
        except ClientServiceError as error:
            flash(str(error), "error")
        else:
            flash("Translation added.", "success")
        return redirect(url_for("word_detail", word_id=word_id))

    @app.post("/translations/<translation_id>/delete")
    def delete_translation_action(translation_id):
        """Delete a translation and return to the word detail page."""
        word_id = request.form.get("word_id", "").strip()
        try:
            delete_translation(translation_id)
        except ClientServiceError as error:
            flash(str(error), "error")
        else:
            flash("Translation deleted.", "success")
        return redirect(url_for("word_detail", word_id=word_id))

    @app.route("/categories")
    def categories():
        """Render the category management screen."""
        user = require_user()
        if not user:
            return redirect(url_for("home"))
        return render_template(
            "categories.html",
            user=user,
            categories=get_categories(user["id"])
        )

    @app.post("/categories")
    def create_category_action():
        """Create a category for the active user."""
        user = require_user()
        if not user:
            return redirect(url_for("home"))
        name = request.form.get("name", "").strip()
        if not name:
            flash("Category name is required.", "error")
            return redirect(url_for("categories"))
        try:
            create_category({"name": name, "user_id": user["id"]})
        except ClientServiceError as error:
            flash(str(error), "error")
        else:
            flash("Category created.", "success")
        return redirect(url_for("categories"))

    @app.post("/categories/<category_id>/delete")
    def delete_category_action(category_id):
        """Delete a category for the active user."""
        try:
            delete_category(category_id)
        except ClientServiceError as error:
            flash(str(error), "error")
        else:
            flash("Category deleted.", "success")
        return redirect(url_for("categories"))

    @app.route("/quiz", methods=["GET", "POST"])
    def quiz():
        """Render and generate vocabulary quizzes."""
        user = require_user()
        if not user:
            return redirect(url_for("home"))

        categories = get_categories(user["id"])
        parts_of_speech = get_parts_of_speech()
        quiz_payload = None
        target_language = "fi"
        limit = 5
        selected_category_id = ""
        selected_pos_code = ""
        selected_language = ""
        if request.method == "POST":
            target_language = request.form.get("target_language", "fi").strip() or "fi"
            limit = int(request.form.get("limit", "5") or 5)
            selected_category_id = request.form.get("category_id", "").strip()
            selected_pos_code = request.form.get("part_of_speech_code", "").strip()
            selected_language = request.form.get("language", "").strip()
            try:
                quiz_payload = create_quiz({
                    "user_id": user["id"],
                    "target_language": target_language,
                    "count": limit,
                    "category_id": selected_category_id,
                    "part_of_speech_code": selected_pos_code,
                    "language": selected_language
                })
            except ClientServiceError as error:
                flash(str(error), "error")
            else:
                session["active_quiz"] = quiz_payload

        return render_template(
            "quiz.html",
            user=user,
            categories=categories,
            parts_of_speech=parts_of_speech,
            quiz_payload=quiz_payload,
            target_language=target_language,
            limit=limit,
            selected_category_id=selected_category_id,
            selected_pos_code=selected_pos_code,
            selected_language=selected_language
        )

    @app.post("/quiz/check")
    def quiz_check():
        """Submit a generated quiz for checking."""
        user = require_user()
        if not user:
            return redirect(url_for("home"))
        quiz_payload = session.get("active_quiz")
        if not quiz_payload:
            flash("Generate a quiz before checking answers.", "warning")
            return redirect(url_for("quiz"))

        answers = {}
        for question in quiz_payload.get("questions", []):
            answers[question["word_id"]] = request.form.get(
                f"answer_{question['word_id']}",
                ""
            ).strip()
        try:
            results = check_quiz(quiz_payload, answers)
        except ClientServiceError as error:
            flash(str(error), "error")
            return redirect(url_for("quiz"))
        return render_template(
            "quiz_results.html",
            user=user,
            results=results
        )

    return app


if __name__ == "__main__":
    create_app().run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5050")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
