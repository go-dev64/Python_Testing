import pytest
from app import server
from tests.test_utils import captured_templates, MockReponse
import app.server


class TestEmail(MockReponse):
    bad_email = "bademail"
    email = "admin@irontemple.com"

    def test_email_is_db(self, client, monkeypatch):
        # Mock clubs data json .
        monkeypatch.setattr(app.server, "clubs", self.get_clubs())

        # Check if email is in clubs email.
        response = client.post("/showSummary", data={"email": self.email})
        # print(app.server.clubs)
        assert response.status_code == 200

    def test_email_is_not_in_db(self, client, monkeypatch):
        # Mock clubs data json .
        monkeypatch.setattr(app.server, "clubs", self.get_clubs())

        # Check if email is not in clubs email and retrun error msg.
        response = client.post("/showSummary", data={"email": self.bad_email})
        # print(app.server.clubs)

        assert b"error" in response.data
        assert response.status_code == 400
