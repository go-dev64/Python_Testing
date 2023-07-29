import pytest
from app import server
from tests.test_utils import MockReponse


class TestEmail(MockReponse):
    bad_email = "bademail"
    email = "admin@irontemple.com"

    def test_email_is_db(self, client, monkeypatch, captured_templates):
        # Mock clubs data json .
        monkeypatch.setattr(server, "clubs", self.get_clubs())
        # print("Mocked clubs:", server.clubs)

        # Check if email is in clubs email.
        rv = client.post("/showSummary", data={"email": self.email})
        template, context = captured_templates[0]
        assert rv.status_code == 200
        assert template.name == "welcome.html"
        # print("rv", rv.data.decode())
        # print("templates:", template, context)

    def test_email_is_not_in_db(self, client, monkeypatch, captured_templates):
        # Mock clubs data json .
        monkeypatch.setattr(self.app.server, "clubs", self.get_clubs())

        # Check if email is not in clubs email and retrun error msg.
        rv = client.post("/showSummary", data={"email": self.bad_email})
        template, context = captured_templates[0]
        assert rv.status_code == 400
        assert b"error" in rv.data
