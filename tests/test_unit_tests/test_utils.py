import pytest
from app.utils import find_element
from app.custom_exception import LowerThanOneError, PlacesError
from tests.mock import Utils
from app import server


class TestUtils(Utils):
    def test_find_element(self, monkeypatch):
        data_test = {"name": "toto", "email": "toto@mail.fr", "points": "5"}
        self._mock_club_and_competition(monkeypatch)
        clubs = server.clubs
        club_name = data_test["name"]
        club_returned = find_element(clubs, club_name)
        assert club_returned["name"] == club_name
        assert club_returned["email"] == data_test["email"]

    def test_update_numbers_places_booked(self, monkeypatch):
        """
        The test must add the places ordered by the competition's key: numbers_places_booked to the club's:competitions_booked list.

        Args:
            monkeypatch (_type_): _description_
        """
        self._mock_club_and_competition(monkeypatch)
        club = [c for c in server.clubs if c["name"] == "club_with_competition_booked"][0]
        competition = [c for c in server.competitions if c["name"] == "Spring Festival"][0]
        places_ordered = 2
        excepted_result = 9
        server.update_competition_booked_by_the_club(club=club, competition=competition, placesRequired=places_ordered)
        competition_booked = [c for c in club["competitions_booked"] if c["name"] == "Spring Festival"][0]
        assert competition_booked["numbers_places_booked"] == excepted_result

    def _raise_exception(self, club_name, competition_name, placesRequired, type_exception, monkeypatch):
        self._mock_club_and_competition(monkeypatch)
        club = [c for c in server.clubs if c["name"] == club_name][0]
        competition = [c for c in server.competitions if c["name"] == competition_name][0]
        with pytest.raises(type_exception):
            server.purchase_conditions(placesRequired, club, competition)

    def test_raise_exception_with_input_is_negative_number(self, monkeypatch):
        # Test should return LowerThanOneError Exception with placesRequired < 1.
        data_test = {"club": "Simply Lift", "competition": "Spring Festival", "places": -2}
        self._raise_exception(
            data_test["club"],
            data_test["competition"],
            data_test["places"],
            LowerThanOneError,
            monkeypatch,
        )

    def test_raise_exception_with_purchase_more_than_twelves_places(self, monkeypatch):
        # Test should return PlacesError Exception with placesRequired > 12.
        data_test = {"club": "toto", "competition": "Spring Festival", "places": 13}
        self._raise_exception(
            data_test["club"], data_test["competition"], data_test["places"], PlacesError, monkeypatch
        )

    def test_raise_exception_with_purchase_more_than_club_points(self, monkeypatch):
        # Test should return PlacesError Exception with placesRequired > club's points.
        data_test = {"club": "toto", "competition": "Spring Festival", "places": 7}
        self._raise_exception(
            data_test["club"], data_test["competition"], data_test["places"], PlacesError, monkeypatch
        )

    def test_raise_exception_with_purchase_more_places_than_available(self, monkeypatch):
        # Test should return PlacesError Exception with placesRequired > places available in the competition.
        data_test = {"club": "tata", "competition": "next competition", "places": 3}
        self._raise_exception(
            data_test["club"], data_test["competition"], data_test["places"], PlacesError, monkeypatch
        )

    def test_raise_exception_with_several_orders_with_more_than_twelves_places_in_total(self, monkeypatch):
        # Test should return PlacesError Exception with placesRequired > 12 (with several orders).
        data_test = {"club": "club_with_competition_booked", "competition": "Spring Festival", "places": 7}
        self._raise_exception(
            data_test["club"], data_test["competition"], data_test["places"], PlacesError, monkeypatch
        )
