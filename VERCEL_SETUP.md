Vercel Setup for To-Do App

1) Framework Settings
- Framework Preset: Other

2) Build & Deployment fields (copy these into Vercel UI)
- Install Command (Override):
  pip install -r requirements.txt
- Build Command (Override):
  (leave empty)
- Output Directory (Override):
  (leave empty)
- Development Command (Override):
  python run.py

3) Environment Variables (add these in Vercel > Settings > Environment Variables)
- MONGODB_URI = mongodb+srv://<user>:<password>@cluster0.mongodb.net/tododb
- MONGODB_DB = tododb
- SECRET_KEY = <a-strong-random-secret>

Notes & Troubleshooting
- Do NOT use your local mongodb://localhost:27017/ on Vercel—use Atlas or another hosted MongoDB instance.
- Ensure `api/index.py` exists at repository root (it should import `app` from `python_app.app`).
- `vercel.json` is present and instructs Vercel to use Python 3.11 for functions.
- If Vercel fails to detect the function, verify file path `api/index.py` and that `app` WSGI callable is exported.
- If you prefer a container approach, I can add a Dockerfile instead.

Quick local test commands
```bash
# from repo root
pip install -r requirements.txt
python run.py
# then open http://127.0.0.1:5000
```

If you'd like, I can also:
A) Update `app.py` to use a module-level lazy MongoDB client to reduce cold-start overhead on Vercel.
B) Add a simple `README.md` Vercel section with screenshots and exact UI copy-paste values.
C) Create a Dockerfile for alternative deployment on Render/Heroku.
