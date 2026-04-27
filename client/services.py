"""HTTP helpers for the Personal Word Repository client."""
from __future__ import annotations

import os
from dataclasses import dataclass

import requests


class ClientServiceError(Exception):
    """Raised when a downstream API call fails."""

    def __init__(self, message, status_code=None):
        super().__init__(message)
        self.status_code = status_code


@dataclass
class ServiceConfig:
    """Resolved service endpoints for the client application."""

    api_base_url: str
    auxiliary_base_url: str


def get_config():
    """Return client configuration from environment variables."""
    return ServiceConfig(
        api_base_url=os.getenv("PWR_API_BASE_URL", "http://127.0.0.1:5000"),
        auxiliary_base_url=os.getenv(
            "PWR_AUXILIARY_BASE_URL",
            "http://127.0.0.1:5001"
        )
    )


def _join(base_url, path):
    """Join a base URL and API path safely."""
    return f"{base_url.rstrip('/')}/{path.lstrip('/')}"


def request_json(method, base_url, path, **kwargs):
    """Perform an HTTP request and return parsed JSON."""
    response = requests.request(method, _join(base_url, path), timeout=10, **kwargs)
    if response.ok:
        if response.content:
            return response.json()
        return None

    error_message = f"Request failed with status {response.status_code}"
    try:
        payload = response.json()
        error_message = payload.get("error", payload.get("message", error_message))
    except ValueError:
        if response.text:
            error_message = response.text
    raise ClientServiceError(error_message, status_code=response.status_code)


def register_user(email, password):
    """Create a user in the main API."""
    config = get_config()
    return request_json(
        "POST",
        config.api_base_url,
        "/users",
        json={"email": email, "password": password}
    )


def get_user(user_id):
    """Fetch a user from the main API."""
    config = get_config()
    return request_json("GET", config.api_base_url, f"/users/{user_id}")


def get_words(user_id, search="", language="", category_id=""):
    """Fetch words for the current user with optional filters."""
    config = get_config()
    params = {"user_id": user_id}
    if search:
        params["search"] = search
    if language:
        params["language"] = language
    if category_id:
        params["category_id"] = category_id
    return request_json("GET", config.api_base_url, "/words", params=params)


def create_word(payload):
    """Create a new word."""
    config = get_config()
    return request_json("POST", config.api_base_url, "/words", json=payload)


def get_word(word_id):
    """Fetch a single word."""
    config = get_config()
    return request_json("GET", config.api_base_url, f"/words/{word_id}")


def update_word(word_id, payload):
    """Update a word."""
    config = get_config()
    return request_json("PUT", config.api_base_url, f"/words/{word_id}", json=payload)


def delete_word(word_id):
    """Delete a word."""
    config = get_config()
    return request_json("DELETE", config.api_base_url, f"/words/{word_id}")


def get_categories(user_id):
    """Fetch categories for the current user."""
    config = get_config()
    return request_json(
        "GET",
        config.api_base_url,
        "/categories",
        params={"user_id": user_id}
    )


def create_category(payload):
    """Create a category."""
    config = get_config()
    return request_json("POST", config.api_base_url, "/categories", json=payload)


def delete_category(category_id):
    """Delete a category."""
    config = get_config()
    return request_json("DELETE", config.api_base_url, f"/categories/{category_id}")


def get_parts_of_speech():
    """Fetch all parts of speech."""
    config = get_config()
    return request_json("GET", config.api_base_url, "/parts-of-speech")


def get_translations(word_id):
    """Fetch all translations for a word."""
    config = get_config()
    return request_json("GET", config.api_base_url, f"/words/{word_id}/translations")


def create_translation(word_id, payload):
    """Create a translation for a word."""
    config = get_config()
    return request_json(
        "POST",
        config.api_base_url,
        f"/words/{word_id}/translations",
        json=payload
    )


def delete_translation(translation_id):
    """Delete a translation."""
    config = get_config()
    return request_json("DELETE", config.api_base_url, f"/translations/{translation_id}")


def create_quiz(payload):
    """Generate a quiz from the auxiliary service."""
    config = get_config()
    return request_json(
        "POST",
        config.auxiliary_base_url,
        "/api/quizzes",
        json=payload
    )


def check_quiz(quiz, answers):
    """Check quiz answers through the auxiliary service."""
    config = get_config()
    return request_json(
        "POST",
        config.auxiliary_base_url,
        "/api/quizzes/check",
        json={"quiz": quiz, "answers": answers}
    )
