"""Core orchestration for the auxiliary quiz service."""
from __future__ import annotations

import os
import random

import requests


class AuxiliaryServiceError(Exception):
    """Raised when the auxiliary service cannot complete a request."""


def api_base_url():
    """Return the configured main API base URL."""
    return os.getenv("PWR_API_BASE_URL", "http://127.0.0.1:5000")


def _join(path):
    """Join the main API base URL and path."""
    return f"{api_base_url().rstrip('/')}/{path.lstrip('/')}"


def api_get(path, params=None):
    """Issue a GET request to the main API."""
    response = requests.get(_join(path), params=params, timeout=10)
    if response.ok:
        return response.json()
    raise AuxiliaryServiceError(f"Main API request failed: {response.text}")


def get_filtered_words(user_id, language="", category_id=""):
    """Fetch words from the main API with basic filters."""
    params = {"user_id": user_id}
    if language:
        params["language"] = language
    if category_id:
        params["category_id"] = category_id
    return api_get("/words", params=params)


def get_parts_of_speech_map():
    """Fetch parts of speech and return them as maps."""
    parts = api_get("/parts-of-speech")
    by_id = {part["id"]: part for part in parts}
    by_code = {part["code"].lower(): part for part in parts}
    return by_id, by_code


def build_quiz_questions(words, target_language):
    """Create quiz questions from main API words."""
    questions = []
    for word in words:
        translations = api_get(f"/words/{word['id']}/translations")
        target_translations = [
            translation for translation in translations
            if translation["language"].strip().lower() == target_language.lower()
        ]
        if not target_translations:
            continue

        acceptable_answers = [translation["text"].strip().lower() for translation in target_translations]
        questions.append({
            "word_id": word["id"],
            "prompt": word["text"],
            "source_language": word["language"],
            "target_language": target_language,
            "acceptable_answers": acceptable_answers,
            "display_answers": [translation["text"] for translation in target_translations],
            "translation_count": len(target_translations)
        })
    return questions


def generate_quiz(user_id, target_language, count, category_id="", part_of_speech_code="", language=""):
    """Generate a quiz from the user's stored words."""
    words = get_filtered_words(user_id, language=language, category_id=category_id)
    if part_of_speech_code:
        by_id, by_code = get_parts_of_speech_map()
        part = by_code.get(part_of_speech_code.lower())
        if not part:
            raise AuxiliaryServiceError("Requested part of speech code does not exist.")
        words = [word for word in words if word["part_of_speech_id"] == part["id"]]
    else:
        by_id, _ = get_parts_of_speech_map()

    questions = build_quiz_questions(words, target_language)
    if not questions:
        return {
            "summary": "No matching quiz questions could be created. Make sure the selected words have translations in the chosen target language.",
            "filters": {
                "user_id": user_id,
                "target_language": target_language,
                "count": count,
                "category_id": category_id,
                "part_of_speech_code": part_of_speech_code,
                "language": language
            },
            "questions": []
        }

    random.shuffle(questions)
    selected = questions[:count]
    for index, question in enumerate(selected, start=1):
        part = by_id.get(next(word["part_of_speech_id"] for word in words if word["id"] == question["word_id"]))
        question["number"] = index
        question["part_of_speech"] = part["code"] if part else "unknown"

    return {
        "summary": f"Generated {len(selected)} quiz question(s) for target language '{target_language}'.",
        "filters": {
            "user_id": user_id,
            "target_language": target_language,
            "count": count,
            "category_id": category_id,
            "part_of_speech_code": part_of_speech_code,
            "language": language
        },
        "questions": selected
    }


def check_quiz(quiz, answers):
    """Check quiz answers and return scored results."""
    questions = quiz.get("questions", [])
    results = []
    score = 0
    for question in questions:
        submitted = answers.get(question["word_id"], "").strip().lower()
        is_correct = submitted in question["acceptable_answers"]
        if is_correct:
            score += 1
        results.append({
            "word_id": question["word_id"],
            "prompt": question["prompt"],
            "submitted_answer": answers.get(question["word_id"], "").strip(),
            "correct_answers": question["display_answers"],
            "is_correct": is_correct,
            "part_of_speech": question.get("part_of_speech", "unknown")
        })

    total = len(questions)
    return {
        "score": score,
        "total": total,
        "percentage": round((score / total) * 100, 1) if total else 0,
        "results": results
    }
