# PWP SPRING 2026
# PERSONAL WORD REPOSITORY
# Group information
* Student 1. Sami Häkkilä - sami.hakkila@student.oulu.fi
* Student 2. Saara Laasonen - Saara.Laasonen@student.oulu.fi
* Student 3. Syed Mahim - Syed.Mahim@student.oulu.fi


This project implements a RESTful API for storing, categorizing and translating personal vocabulary. The repository includes full documentation on setup, database initialization, running the API, and code quality verification.

---

## Technologies

- Python 3
- Flask
- Flask-SQLAlchemy
- Flask-RESTful
- SQLite (default database)
- PyLint (code quality)

---

## Dependencies

Project dependencies are listed in `requirements.txt`.

Main dependencies:
- Flask
- Flask-SQLAlchemy
- Flask-RESTful

Install dependencies with:

```bash
pip install -r requirements.txt

```
## Setting up the framework:

Step 1: Create a virtual environment
```bash
python -m venv venv

```

Step 2: Activate the environment
For Windows:
```bash
venv\Scripts\activate

```

For macOS/Linux:
```bash
source venv/bin/activate

```


## Populate the test database:

```bash
python populate.py

