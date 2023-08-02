import pytest
from app import server
from app.server import book
from tests.test_utils import MockReponse
from datetime import datetime, date


class TestEmail(MockReponse):
    def setup_method(self):
        self.bad_email = "bademail"
        self.email = "admin@irontemple.com"

    def test_email_is_db(self, client, monkeypatch, captured_templates):
        # Mock clubs data json .
        self._mock_club_and_competition(monkeypatch)

        # Check if email is in clubs email.
        rv = client.post("/showSummary", data={"email": self.email})
        template, context = captured_templates[0]
        assert rv.status_code == 200
        # Check template returned.
        assert template.name == "welcome.html"

    def test_email_is_not_in_db(self, client, monkeypatch, captured_templates):
        # Mock clubs data json .
        self._mock_club_and_competition(monkeypatch)

        # Check if email is not in clubs email and retrun error msg.
        rv = client.post("/showSummary", data={"email": self.bad_email})
        template, context = captured_templates[0]
        assert rv.status_code == 400
        assert b"error" in rv.data
        assert template.name == "index.html"

    def test_data_returned(self, client, monkeypatch, captured_templates):
        # Check whether the context returned is that of the e-mail supplied.
        self._mock_club_and_competition(monkeypatch)

        rv = client.post("/showSummary", data={"email": self.email})
        template, context = captured_templates[0]
        assert context["club"]["email"] == self.email
        assert context["list_of_clubs"] == server.clubs
        assert len(context["list_of_clubs"]) > 0


class TestBooking(MockReponse):
    def setup_method(self):
        self.data = {"club": "toto", "competition": "Spring Festival", "places": 2}
        self.future_competition = {"club": "toto", "competition": "next competition", "places": 2}

    def test_soubstract_point_club(self, client, monkeypatch, captured_templates):
        """
        We are testing if ,after registering  for acompetition,
        the number of entries is deducted from club's points.
        """
        self._mock_club_and_competition(monkeypatch)
        # We get club point before request.
        club = [c for c in server.clubs if c["name"] == self.data["club"]][0]
        nombre_point = int(club["points"])
        rv = client.post("/purchasePlaces", data=self.data)
        assert rv.status_code == 200
        template, context = captured_templates[0]
        # Checking of deduction of points and  the context returned are those of the requested club.
        assert context["club"]["name"] == self.data["club"]
        assert int(context["club"]["points"]) == nombre_point - self.data["places"]

    def test_input_is_positive_number(self, client, monkeypatch, captured_templates):
        self._mock_club_and_competition(monkeypatch)
        rv = client.post("/purchasePlaces", data=self.data)
        template, context = captured_templates[0]

        # Should return a status_code 200 with input > 0.
        assert rv.status_code == 200
        assert template.name == "welcome.html"

    def test_input_is_negative_number(self, client, monkeypatch, captured_templates):
        self._mock_club_and_competition(monkeypatch)
        rv = client.post(
            "/purchasePlaces",
            data={"club": "Simply Lift", "competition": "Spring Festival", "places": -2},
        )
        template, context = captured_templates[0]

        # Should return a status_code 400 with input < 0 and error message.
        assert rv.status_code == 400
        assert str(context["error"]) == "Please enter a number greater than zero!"

    def test_booking_with_more_than_twelves_places(self, client, monkeypatch, captured_templates):
        data = {"club": "toto", "competition": "Spring Festival", "places": 13}
        self._mock_club_and_competition(monkeypatch)
        rv = client.post("/purchasePlaces", data=data)
        template, context = captured_templates[0]

        # Should return a status_code 400 with places > 12 and error message.
        assert rv.status_code == 400
        assert str(context["error"]) == "The maximum reservation is 12 places!"

    def test_booking_on_past_competition(self, client, monkeypatch, captured_templates):
        self._mock_club_and_competition(monkeypatch)
        route = f"/book/{self.data['competition']}/{self.data['club']}"
        rv = client.get(route)
        template, context = captured_templates[0]

        #  Should return a status_code 400 with date competition < today.
        assert rv.status_code == 400

        # Check template returned
        assert template.name == "welcome.html"

    def test_booking_with_future_competition(self, client, monkeypatch, captured_templates):
        self._mock_club_and_competition(monkeypatch)
        route = f"/book/{self.future_competition['competition']}/{self.future_competition['club']}"
        rv = client.get(route)
        template, context = captured_templates[0]

        #  Should return a status_code 200 with date competition > today.
        assert rv.status_code == 200

        # Check template returned and context.
        assert template.name == "booking.html"
        assert context["club"]["name"] == self.future_competition["club"]
        assert context["competition"]["name"] == self.future_competition["competition"]
