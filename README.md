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
--- 

## Install dependencies without virtual environment

Step 1: install requirements

```bash
pip install -r requirements.txt

```
---
## With virtual environment:

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

Step 3: Install dependencies
```bash
pip install -r requirements.txt

```

---

## Populate the test database:

```bash
python populate.py

```

## API entry point

Entry point:
```bash
http://localhost:5000/

```

## Code Quality

Code quality was evaluated using PyLint, as required by the assignment.

Command used:

```bash
pylint wordrepo --disable=no-member,import-outside-toplevel,no-self-use

```

Final Pylint Score: 9.48/10

Remaining warnings and justifications:
- Trailing whitespace (C0303) > minor cosmetic issue; does not affect functionality
- Too few public methods (R0903) > Normal for SQLAlchemy models (primarily define fields and relationships)
- Trailing newlines (C0305) > extra blank line at the end of the code is harmless
- Cyclic imports (R0401) > expected in Flask applications using an application factory pattern (occur inside create_app(), so no runtime issues occur)
