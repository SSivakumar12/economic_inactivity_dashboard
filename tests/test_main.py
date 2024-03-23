##
# PLACEHOLDER - TEST WHETHER ROUTING IS CORRECT

import pytest
from src.main import app
from flask import url_for


def test_redirect_gender_analysis():
    # testing whether the redirection of
    with app.test_client() as client:
        response = client.get('/redirect_gender_analysis')
        response.status_code == 302
        response.location == url_for('gender_breakdown_analysis')
