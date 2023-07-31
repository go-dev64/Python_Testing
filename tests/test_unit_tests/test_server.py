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
        # Check template returned.
        assert template.name == "welcome.html"

    def test_email_is_not_in_db(self, client, monkeypatch, captured_templates):
        # Mock clubs data json .
        monkeypatch.setattr(server, "clubs", self.get_clubs())

        # Check if email is not in clubs email and retrun error msg.
        rv = client.post("/showSummary", data={"email": self.bad_email})
        template, context = captured_templates[0]
        assert rv.status_code == 400
        assert b"error" in rv.data
        assert template.name == "index.html"

    def test_data_returned(self, client, monkeypatch, captured_templates):
        # Check whether the context returned is that of the e-mail supplied.
        monkeypatch.setattr(server, "clubs", self.get_clubs())
        rv = client.post("/showSummary", data={"email": self.email})
        template, context = captured_templates[0]
        assert context["club"]["email"] == self.email
        assert context["list_of_club"] == server.clubs
        assert len(context["list_of_club"]) > 0
