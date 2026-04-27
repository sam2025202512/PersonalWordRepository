# PWP SPRING 2026
# PERSONAL WORD REPOSITORY
# Group information
* Student 1. Sami Häkkilä - sami.hakkila@student.oulu.fi
* Student 2. Saara Laasonen - Saara.Laasonen@student.oulu.fi
* Student 3. Syed Mahim - Syed.Mahim@student.oulu.fi


This project implements a RESTful API for storing, categorizing and translating personal vocabulary. The repository includes full documentation on setup, database initialization, running the API, and code quality verification.

The repository also includes:

- a Flask-based GUI client in `client/`
- an auxiliary learning service in `auxiliary_service/`
- ecosystem documentation in `docs/final_deadline_overview.md`

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

Development and test dependencies are listed in `requirements-dev.txt`.
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
python -m flask --app wordrepo.api:create_app run
```

## Option: Running the full ecosystem with Docker Compose

The repository includes Docker support for:

- the main API
- the auxiliary service
- the GUI client

Build and start the whole ecosystem with one command:

```bash
docker compose up --build
```

This command starts all three services together, so you do not need to run the main API, the auxiliary service, and the client separately when using Docker Compose.

After startup:

```text
Main API: http://127.0.0.1:5000/
Auxiliary service: http://127.0.0.1:5001/
Client: http://127.0.0.1:5050/
```

The SQLite database is stored in the local `instance/` folder and mounted into the container, so data persists between restarts.

Stop the service with:

```bash
docker compose down
```


## API entry point

After starting the server, the API is available at:

```text
http://127.0.0.1:5000/
```

## API documentation

The repository includes an OpenAPI 3.0 specification at `docs/openapi.yaml`.

When the server is running, the documentation is available live at:

```text
http://127.0.0.1:5000/docs
```

The raw OpenAPI file is available at:

```text
http://127.0.0.1:5000/openapi.yaml
```

## Final deliverable components

- Main API: `wordrepo/`
- Client application: `client/`
- Auxiliary service: `auxiliary_service/`

Component-specific documentation:

- `client/README.md`
- `auxiliary_service/README.md`
- `docs/final_deadline_overview.md`

## Testing

Run the automated tests with:

```bash
pytest -q
```

Run the tests with coverage:

```bash
pytest --cov=wordrepo --cov-report=term-missing
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
