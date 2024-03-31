import pytest
from src.main import app
from flask import url_for


def test_all_routes():
    """testing whether the redirection of routes as expected"""

    # add potential future routes as well in the future
    routes_pages_map = {'/redirect_gender_analysis': 'gender_breakdown_analysis',
                        '/route_trend_analysis': 'trend_analysis'}

    with app.test_client() as client:
        for route, page in routes_pages_map.items():
            response = client.get(route)
            assert response.status_code == 302
            assert response.location == url_for(page)


def test_index_page():
    pass
