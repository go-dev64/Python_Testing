import pytest
import app
from app import server
from tests.test_utils import captured_templates, MockReponse


class TestEmail(MockReponse):
    bad_email = "bademail"
    email = "admin@irontemple.com"

    def test_email_is_db(self, client, monkeypatch):
        # Mock clubs data json .
        monkeypatch.setattr(server, "clubs", self.get_clubs())
        print("Mocked clubs:", server.clubs)

        # Check if email is in clubs email.
        """response = client.post("/showSummary", data={"email": self.email})
        # print(app.server.clubs)
        assert response.status_code == 200"""

        with captured_templates(app=server) as templates:
            rv = client.post("/showSummary", data={"email": self.email})
            assert rv.status_code == 200

            print("rv", rv.data.decode())

            print("templates:", templates)

            # template, context = templates[0]

    """def test_email_is_not_in_db(self, client, monkeypatch):
        # Mock clubs data json .
        monkeypatch.setattr(self.app.server, "clubs", self.get_clubs())

        # Check if email is not in clubs email and retrun error msg.
        templates = []
        with captured_templates(self.app, templates):
            rv = client.post("/showSummary", data={"email": self.bad_email})
            assert rv.status_code == 400
            assert b"error" in rv.data
            print(templates)

        response = client.post("/showSummary", data={"email": self.bad_email})
        # print(app.server.clubs)

        assert b"error" in response.data
        assert response.status_code == 400"""
