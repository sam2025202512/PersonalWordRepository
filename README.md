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

## Running the project

Run all commands from the project root directory, where `README.md`, `init_db.py`, and the `wordrepo/` folder are located.

### Windows (PowerShell)

1. Create a virtual environment:

```powershell
python -m venv venv
```

2. Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

3. Install dependencies:

```powershell
pip install -r requirements.txt
```

4. Initialize the database:

```powershell
python init_db.py
```

5. Start the Flask API:

```powershell
cd PersonalWordRepository
```

```powershell
python -m flask --app wordrepo.api:create_app run
```

### Linux / macOS (Bash)

1. Create a virtual environment:

```bash
python3 -m venv venv
```

2. Activate the virtual environment:

```bash
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Initialize the database:

```bash
python init_db.py
```

5. Start the Flask API:


```bash
cd PersonalWordrepository
```

```bash
python -m flask --app wordrepo.api:create_app run
```

### Without activating the virtual environment

Windows:

```powershell
python -m venv venv
.\venv\Scripts\python.exe -m pip install -r requirements.txt
.\venv\Scripts\python.exe init_db.py
.\venv\Scripts\python.exe -m flask --app wordrepo.api:create_app run
```

Linux / macOS:

```bash
python3 -m venv venv
venv/bin/pip install -r requirements.txt
venv/bin/python init_db.py
venv/bin/python -m flask --app wordrepo.api:create_app run
```

## API entry point

After starting the server, the API is available at:

```text
http://127.0.0.1:5000/
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
