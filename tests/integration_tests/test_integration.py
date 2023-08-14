import pytest
from flask import url_for, request
from app import server
from app.utils import find_element

from tests.mock import Utils


class TestIntegration(Utils):
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
            data={"email": "admin@irontemple.com"},
        )

        assert context["club"]["email"] == "admin@irontemple.com"

    def test_input_is_positive_number(self, client, monkeypatch, captured_templates):
        """
        Should return a status_code 200 with 12 > order > 0.
        """
        data_test = {"club": "toto", "competition": "Spring Festival", "places": 2}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )

        assert rv.status_code == 200
        assert template.name == "welcome.html"
        club = [c for c in server.clubs if c["name"] == data_test["club"]][0]
        competition_booked = [c for c in club["competitions_booked"] if c["name"] == data_test["competition"]][0]
        number_places_booked_in_competition = competition_booked["numbers_places_booked"]
        assert number_places_booked_in_competition == data_test["places"]

    def test_update_numbers_places_booked(self, client, monkeypatch, captured_templates):
        # Should return a number of places booked of cluf updated.
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

    def test_booking_with_more_than_twelves_places(self, client, monkeypatch, captured_templates):
        # Should return a status_code 403 with places > 12 and error message.

        data_test = {"club": "toto", "competition": "Spring Festival", "places": 13}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )

        assert rv.status_code == 403
        assert str(context["error"]) == "The maximum reservation is 12 places!"

    def test_several_orders_with_more_than_twelves_places_in_total(self, client, monkeypatch, captured_templates):
        # Should return a status_code 403 with places oSrdered > 12 and error message.

        data_test = {"club": "club_with_competition_booked", "competition": "Spring Festival", "places": 7}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )
        assert rv.status_code == 403
        assert str(context["error"]) == "The maximum reservation is 12 places!"

    def test_booking_with_purchase_more_than_club_points(self, client, monkeypatch, captured_templates):
        # Test should retrun status code 403 with places purchase 7 places > toto club's points (5 points).

        data_test = {"club": "toto", "competition": "Spring Festival", "places": 7}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )

        assert rv.status_code == 403
        assert str(context["error"]) == f"You can book {context['club']['points']} places maximum!"

    def test_booking_with_more_places_than_available(self, client, monkeypatch, captured_templates):
        # Test should return status code 403 with number places purchease > available places.

        data_test = {"club": "tata", "competition": "next competition", "places": 3}
        rv, template, context = self.get_response_value_and_template_context(
            captured_templates=captured_templates,
            client=client,
            method="POST",
            monkeypatch=monkeypatch,
            route="/purchasePlaces",
            data=data_test,
        )
        assert rv.status_code == 403
        assert str(context["error"]) == f"There are only {context['competition']['numberOfPlaces']} places available!"

    def test_update_point_club(self, client, monkeypatch, captured_templates):
        """
        We are testing if ,after registering  for acompetition,
        the number of entries is deducted from club's points.
        """
        data_test = {"club": "toto", "competition": "Spring Festival", "places": 2}
        self._mock_club_and_competition(monkeypatch)
        # We get club point before request.
        club = find_element(server.clubs, data_test["club"])
        nombre_point = int(club["points"])
        rv = client.post("/purchasePlaces", data=data_test)
        assert rv.status_code == 200
        template, context = captured_templates[0]
        # Checking of deduction of points and  the context returned are those of the requested club.
        assert context["club"]["name"] == data_test["club"]
        assert int(context["club"]["points"]) == nombre_point - data_test["places"]
