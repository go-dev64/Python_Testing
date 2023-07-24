from .conftest import client
from app.server import showSummary


def test_should_status_code_ok(client):
    response = client.get("/")
    assert response.status_code == 200


# verifie si type email non ok => retrun msg error
# verifie si email dans db => retrun ok
# verifie si email absent db => return msg error


def test_email_is_valid_type():
    # check if email is a valid email.
    pass
