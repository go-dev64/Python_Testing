import pytest
from flask import url_for, request
from app import server
from tests.test_utils import Utils


class TestEmail(Utils):
    def setup_method(self):
        self.bad_email = "bademail"
        self.email = "admin@irontemple.com"

    def test_email_is_db(self, client, monkeypatch, captured_templates):
        """
        Check if email is in clubs email.
        """
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/showSummary",
            data={"email": self.email},
        )

        assert rv.status_code == 200
        # Check template returned.
        assert template.name == "welcome.html"

    def test_email_is_not_in_db(self, client, monkeypatch, captured_templates):
        """
        Check if bad email return code status 400 and error message
        """
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/showSummary",
            data=self.bad_email,
        )
        assert rv.status_code == 400
        assert b"error" in rv.data
        assert template.name == "index.html"

    def test_data_returned(self, client, monkeypatch, captured_templates):
        """
        test should return wright context email and list of clubs.
        """
        # Check whether the context returned is that of the e-mail supplied.
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/showSummary",
            data={"email": self.email},
        )

        assert context["club"]["email"] == self.email
        assert len(context["list_of_clubs"]) > 0

    def test_dashboard(self, client, monkeypatch, captured_templates):
        """
        Test should return clubs list on page home.
        """
        data_test = {"club": "toto"}
        route = f"/dashboard/{data_test['club']}"
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="GET",
            monkeypatch=monkeypatch,
            route=route,
        )
        assert rv.status_code == 200
        assert template.name == "dashboard.html"
        assert len(context["list_of_clubs"]) > 0

    def test_redirect_index_page(self, client, monkeypatch, captured_templates):
        self._mock_club_and_competition(monkeypatch)
        rv = client.get("/logout")

        rv.status_code == 302
        assert request.path == url_for("index")


class TestBooking(Utils):
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
        """
        Should return a status_code 200 with input > 0.
        """
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=self.data,
        )

        assert rv.status_code == 200
        assert template.name == "welcome.html"

    def test_input_is_negative_number(self, client, monkeypatch, captured_templates):
        """
        Should return a status_code 400 with input < 0 and error message.
        """
        data_test = {"club": "Simply Lift", "competition": "Spring Festival", "places": -2}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )

        assert rv.status_code == 400
        assert str(context["error"]) == "Please enter a number greater than zero!"

    def test_booking_with_input_is_not_number(self, client, monkeypatch, captured_templates):
        """
        Should return a status_code 400 with input != number and error message.
        """
        data_test = {"club": "Simply Lift", "competition": "Spring Festival", "places": "aaaaaa"}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )

        assert rv.status_code == 400
        assert str(context["error"]) == "Please, Enter a number!"

    def test_booking_with_more_than_twelves_places(self, client, monkeypatch, captured_templates):
        """
        Should return a status_code 400 with places > 12 and error message.
        """
        data_test = {"club": "toto", "competition": "Spring Festival", "places": 13}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )

        assert rv.status_code == 400
        assert str(context["error"]) == "The maximum reservation is 12 places!"

    def test_several_orders_with_more_than_twelves_places_in_total(self, client, monkeypatch, captured_templates):
        """
        Should return a status_code 400 with places oSrdered > 12 and error message.
        """
        data_test = {"club": "club_with_competition_booked", "competition": "Spring Festival", "places": 7}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )
        assert rv.status_code == 400
        assert str(context["error"]) == "The maximum reservation is 12 places!"

    def test_update_numbers_places_booked(self, client, monkeypatch, captured_templates):
        data_test = {"club": "club_with_competition_booked", "competition": "Spring Festival", "places": 2}
        self._mock_club_and_competition(monkeypatch)
        # We get club point before request.
        club = [c for c in server.clubs if c["name"] == data_test["club"]][0]
        competition_booked = [c for c in club["competitions_booked"] if c["name"] == data_test["competition"]][0]
        number_places_booked_in_competition = competition_booked["numbers_places_booked"]

        rv = client.post("/purchasePlaces", data=data_test)
        assert rv.status_code == 200
        template, context = captured_templates[0]
        # Checking of deduction of points and  the context returned are those of the requested club.

        competition_booked_after = [c for c in club["competitions_booked"] if c["name"] == data_test["competition"]][0]
        assert context["club"]["name"] == data_test["club"]
        assert (
            competition_booked_after["numbers_places_booked"]
            == number_places_booked_in_competition + data_test["places"]
        )

    def test_booking_with_purchase_more_than_club_points(self, client, monkeypatch, captured_templates):
        """
        Test should retrun status code 400 with places purchase 7 places > toto club's points (5 points).
        """
        data_test = {"club": "toto", "competition": "Spring Festival", "places": 7}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )

        assert rv.status_code == 400
        assert str(context["error"]) == f"You can book {context['club']['points']} places maximum!"

    def test_booking_with_more_places_than_available(self, client, monkeypatch, captured_templates):
        """
        Test should return status code 400 with number places purchease > available places.
        """
        data_test = {"club": "tata", "competition": "next competition", "places": 3}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )
        assert rv.status_code == 400
        assert str(context["error"]) == f"There are only {context['competition']['numberOfPlaces']} places available!"

    def test_booking_on_past_competition(self, client, monkeypatch, captured_templates):
        """
        Should return a status_code 400 with date competition < today.
        """
        route = f"/book/{self.data['competition']}/{self.data['club']}"
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="GET",
            monkeypatch=monkeypatch,
            route=route,
        )

        assert rv.status_code == 400
        assert template.name == "welcome.html"

    def test_booking_with_future_competition(self, client, monkeypatch, captured_templates):
        """
        Test Should return a status_code 200 with date competition > today.
        """
        route = f"/book/{self.future_competition['competition']}/{self.future_competition['club']}"
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="GET",
            monkeypatch=monkeypatch,
            route=route,
        )

        assert rv.status_code == 200
        assert template.name == "booking.html"
        assert context["club"]["name"] == self.future_competition["club"]
        assert context["competition"]["name"] == self.future_competition["competition"]
