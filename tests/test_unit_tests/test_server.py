import pytest
from app import server
from tests.test_utils import MockReponse


class TestEmail(MockReponse):
    def setup_method(self):
        self.bad_email = "bademail"
        self.email = "admin@irontemple.com"

    def test_email_is_db(self, client, monkeypatch, captured_templates):
        # Mock clubs data json .
        monkeypatch.setattr(server, "clubs", self.get_clubs())

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
        assert context["list_of_clubs"] == server.clubs
        assert len(context["list_of_clubs"]) > 0


class TestBooking(MockReponse):
    def setup_method(self):
        self.data = {"club": "Simply Lift", "competition": "Spring Festival", "places": 2}

    def test_soubstract_point_club(self, client, monkeypatch, captured_templates):
        """
        We are testing if ,after registering  for acompetition,
        the number of entries is deducted from club's points.
        """
        monkeypatch.setattr(server, "clubs", self.get_clubs())
        monkeypatch.setattr(server, "competitions", self.get_competitions())
        # We get club point before request.
        club = [c for c in server.clubs if c["name"] == self.data["club"]][0]
        nombre_point = int(club["points"])
        rv = client.post("/purchasePlaces", data=self.data)
        assert rv.status_code == 200
        template, context = captured_templates[0]
        # Checking of deduction of points and  the context returned are those of the requested club.
        assert context["club"]["name"] == self.data["club"]
        assert int(context["club"]["points"]) == nombre_point - self.data["places"]

    def test_input_is_positive_number(self, client):
        rv = client.post("/purchasePlaces", data=self.data)
        assert rv.status_code == 200

    def test_input_is_negative_number(self, client):
        rv = client.post(
            "/purchasePlaces",
            data={"club": "Simply Lift", "competition": "Spring Festival", "places": -2},
        )
        assert rv.status_code == 400
        assert b"error" in rv.data
