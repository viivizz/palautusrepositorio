# Copilot instructions for this repository

## Project overview

This repository is a small Flask web application for user registration and login. The main app entry is `src/index.py`, which starts the Flask server from `src/app.py`.

The code is organized by responsibility:

- `src/app.py`: Flask routes and request handling; routes are thin by design and delegate work to services.
- `src/services/user_service.py`: validation and business rules for login/registration.
- `src/repositories/user_repository.py`: in-memory user storage used for tests and application state.
- `src/entities/user.py`: the domain model for a user.
- `src/templates/`: server-rendered HTML templates for the UI.
- `src/tests/`: Robot Framework acceptance tests and shared browser setup in `resource.robot`.

This is intentionally a lightweight app with no database, ORM, or frontend build pipeline. The repository state is kept in memory and reset via the `/tests/reset` endpoint during automated browser tests.

## Build, test, and validation commands

This project uses Python 3.14 (`.python-version`) and `uv` for dependency management.

- Install dependencies:
  `uv sync --group dev`
- Start the app locally:
  `uv run python src/index.py`
  The Flask application runs at 'http://localhost:5001'.
- Run the full test suite:
  `uv run robot src/tests`
  The application must be running in a separate terminal for the Robot tests to execute successfully.
- Run a single Robot test file:
  `uv run robot src/tests/login.robot`
- Run a single test case by name:
  `uv run robot -t "Login With Correct Credentials" src/tests/login.robot`

The Robot tests use the `Browser` library and the shared setup in `src/tests/resource.robot`. The `HEADLESS` variable controls whether the browser runs headlessly or visibly; change it there if you need to observe the browser while debugging.

There is no project-specific lint command or `pytest` configuration in this repository. The primary validation path is the Robot test suite.

## Architecture notes

The important architecture to preserve is the separation between layers:

- `app.py` should stay focused on HTTP concerns: reading form data, delegating to a service, and redirecting/flash messaging.
- `UserService` owns validation rules such as username length, password length, password composition, matching confirmation, and duplicate-user checks. Username and password validation is implemented in 'src/services/user_service.py' in the 'UserService.validate' method.
- `UserRepository` is the only persistence abstraction in the project. It stores users in a Python list, not a database.
- Browser tests exercise the real web app through `AppLibrary.py` and reset the repository state before each scenario to keep tests isolated.

When changing behavior, keep the same flow: read request data in routes, validate in the service layer, persist via the repository, then render or redirect in the route.

## Key repository conventions

- Prefer the existing layered structure over introducing new helpers in route handlers.
- Keep tests in `src/tests` and use the shared Robot keywords in `resource.robot` instead of duplicating browser setup.
- The app resets its in-memory data through `POST /tests/reset`; do not change the repository to a persistent store unless the task explicitly requires it.
- The project is intentionally simple and does not include a frontend build step or API layer; changes should remain consistent with that structure.
- Use `uv` and the managed environment instead of ad hoc virtualenv setup so dependency versions stay aligned with `pyproject.toml` and `uv.lock`.

## Editing guidance

- Add or update route behavior in `src/app.py` only when the change is directly about request handling.
- Put validation and business logic in `src/services/user_service.py` rather than hidden in templates or routes.
- If you need stateful behavior for tests, use the same in-memory repository pattern and reset endpoints rather than introducing a database.

This repo is small and convention-driven; the quickest way to understand it is to read the route flow in `src/app.py`, then the matching service and repository implementation that handles the request.
