import pytest
from app import server
from tests.test_utils import captured_templates
import app.server


class MockReponse:
    @staticmethod
    def get_clubs():
        # Return clubs lists.
        return [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
        ]

    @staticmethod
    def get_competitions():
        # Retrun cpmpetitons lists.
        return [
            {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
            {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
        ]


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
