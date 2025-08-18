#!/usr/bin/python3
"""
imports Flask instance for gunicorn configurations
gunicorn --bind 127.0.0.1:8003 wsgi.wsgi_airbnb:app.app
"""

app = __import__('main_app.app', globals(), locals(), ['*'])

if __name__ == "__main__":
    """runs the main flask app"""
    app.app.run()
