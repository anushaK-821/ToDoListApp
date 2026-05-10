# Python + MongoDB ToDo App

This is the migrated version of your Java app in Python using Flask and MongoDB.

## Stack

- Flask
- PyMongo
- MongoDB (`mongodb://localhost:27017/`)

## Run Steps

1. Open terminal in this folder:
   - `cd d:\ToDoListApp\python_app`
2. Create virtual environment:
   - `python -m venv .venv`
3. Activate it (PowerShell):
   - `.\.venv\Scripts\Activate.ps1`
4. Install dependencies:
   - `pip install -r requirements.txt`
5. Optional: copy env file:
   - `Copy-Item .env.example .env`
6. Seed a login user:
   - `python seed_user.py`
7. Start app:
   - `python app.py`
8. Open in browser:
   - `http://localhost:5000/login`

## One Command Start (Windows)

From this folder, run:

- `python run.py`

Alternative commands:

- `.\start.cmd`

Or run PowerShell script directly:

- `.\start.ps1`

This command will:

- create `.venv` if missing
- install dependencies
- create `.env` from `.env.example` if missing
- seed default user
- run the Flask app

## Default Seed User

- username: `admin`
- password: `admin123`

## MongoDB Collections

- `users`:
  - `username` (string)
  - `password` (string)
- `tasks`:
  - `_id` (ObjectId)
  - `title` (string)
  - `description` (string)
  - `owner` (string)

## Notes

- This migration keeps behavior similar to your existing Java app.
- Credentials are plain text for parity with old app. For production, hash passwords.
