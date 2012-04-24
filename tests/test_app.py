from flask import Flask
from blog import app


def test_app_exists():
    assert app


def test_app_is_a_flask_app():
    assert isinstance(app, Flask)
