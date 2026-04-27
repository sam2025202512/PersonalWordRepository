"""Auxiliary Flask service for Personal Word Repository."""
from __future__ import annotations

import os

from flask import Flask, jsonify, request

from auxiliary_service.service import AuxiliaryServiceError, check_quiz, generate_quiz


def create_app():
    """Create the auxiliary service application."""
    app = Flask(__name__)

    @app.after_request
    def set_headers(response):
        """Allow simple cross-service browser integration during demos."""
        response.headers["Access-Control-Allow-Origin"] = "*"
        response.headers["Access-Control-Allow-Headers"] = "Content-Type"
        response.headers["Access-Control-Allow-Methods"] = "GET,POST,OPTIONS"
        return response

    @app.get("/health")
    def health():
        """Return a basic health response."""
        return jsonify({"status": "ok"}), 200

    @app.post("/api/quizzes")
    def quizzes():
        """Generate a quiz from the stored vocabulary."""
        data = request.get_json() or {}
        user_id = data.get("user_id", "").strip()
        target_language = data.get("target_language", "").strip()
        count = int(data.get("count", 5) or 5)
        category_id = data.get("category_id", "").strip()
        part_of_speech_code = data.get("part_of_speech_code", "").strip()
        language = data.get("language", "").strip()
        if not user_id or not target_language:
            return jsonify({"error": "user_id and target_language are required"}), 400

        try:
            payload = generate_quiz(
                user_id=user_id,
                target_language=target_language,
                count=count,
                category_id=category_id,
                part_of_speech_code=part_of_speech_code,
                language=language
            )
        except AuxiliaryServiceError as error:
            return jsonify({"error": str(error)}), 502
        return jsonify(payload), 200

    @app.post("/api/quizzes/check")
    def quizzes_check():
        """Check a completed quiz."""
        data = request.get_json() or {}
        quiz = data.get("quiz")
        answers = data.get("answers")
        if not quiz or answers is None:
            return jsonify({"error": "quiz and answers are required"}), 400

        try:
            payload = check_quiz(quiz, answers)
        except AuxiliaryServiceError as error:
            return jsonify({"error": str(error)}), 502
        return jsonify(payload), 200

    return app


if __name__ == "__main__":
    create_app().run(
        host="0.0.0.0",
        port=int(os.getenv("PORT", "5001")),
        debug=os.getenv("FLASK_DEBUG", "false").lower() == "true"
    )
