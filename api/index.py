# Vercel serverless entry: import the Flask WSGI app from your package
# Vercel's Python builder will serve the WSGI `app` object.
from python_app.app import app

# Ensure the symbol used by Vercel is `app` (WSGI callable)
# No further code required here — Vercel will pick up this file as a serverless endpoint.
