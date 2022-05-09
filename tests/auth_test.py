from app.auth.forms import *
from app.db.models import User
from flask import session
import pytest


def test_request_login(client):
    response = client.get("/login")
    assert response.status_code == 200
    assert b'<h2>Login</h2>' in response.data


def test_request_register(client):
    response = client.get("/register")
    assert response.status_code == 200
    assert b'<h2>Register</h2' in response.data


def test_register(client):
    assert client.get("/register").status_code == 200
    response = client.post("/register", data={"email": "admin2@mail.com", "password": "Test123", "confirm": "Test123"})
    with client.application.app_context():
        user_id = User.query.filter_by(email="admin2@mail.com").first().get_id()
    # check if the user is redirected properly
    assert "/login" == response.headers["Location"]
    # check if the user is in the database
    assert user_id is not None


def test_login(client):
    with client:
        assert client.get("/login").status_code == 200
        response = client.post("/login", data={"email": "admin2@mail.com", "password": "Test123"})
        assert "/about" == response.headers["Location"]
        with client.application.app_context():
            user_id = User.query.filter_by(email="admin2@mail.com").first().get_id()
        assert session['_user_id'] == user_id


@pytest.mark.parametrize(
    ("password", "confirm"),
    (
            # password too short
            ("a", "a"),
            # password has no lowercase
            ("TEST123", "TEST123"),
            # password has no uppercase
            ("test123", "test123"),
            # password has no numbers
            ("testtest", "testtest"),
            # password too long
            ("test123test123test123test123test123test123", "test123test123test123test123test123test123")
    )
)
def test_bad_register(client, password, confirm):
    with client:
        # attempt to register a password that a custom validator would invalidate
        response = client.post("/register",
                               data={"email": "bad@mail.com", "password": password, "confirm": confirm})
        with client.application.app_context():
            # a new entry should not have been created
            assert User.query.filter_by(email="bad@mail.com").first() is None


def test_register_matching_passwords(client):
    # Test that mismatching passwords are correctly handled
    response = client.post("/register", data={"email": "bad@mail.com", "password": "Test123", "confirm": ""})
    assert b'Passwords must match' in response.data
    # Test that mismatching passwords are correctly handled even if the field is not empty
    response = client.post("/register", data={"email": "bad@mail.com", "password": "Test123", "confirm": "Test456"})
    assert b'Passwords must match' in response.data


def test_already_registered(client):
    with client:
        assert client.get("/register").status_code == 200
        response = client.post("/register", data={"email": "admin@mail.com", "password": "Test123", "confirm": "Test123"})
        # The user should now be redirected back to the registration
        assert "/login" == response.headers["Location"]