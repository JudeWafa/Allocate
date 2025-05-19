
import sys

import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Build.app import app

import pytest

@pytest.fixture

def client():
    with app.test_client() as client:
        yield client

def test_logIn_email_found_correct_password(client):
    response = client.get('/logIn')
    assert response.status_code == 200