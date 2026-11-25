"""
WSGI Production Entry Point for Smart Parking System
Used by Gunicorn, Waitress, uWSGI, or cloud hosting environments.
"""
from app import create_app

app = create_app()

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    # In production on Windows, Waitress can be used:
    # from waitress import serve
    # serve(app, host="0.0.0.0", port=port)
    app.run(host="0.0.0.0", port=port)
