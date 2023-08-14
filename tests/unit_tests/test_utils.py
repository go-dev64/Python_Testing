import pytest
from app.utils import find_element
from app.custom_exception import LowerThanOneError, PlacesError
from tests.mock import Utils
from app import server, utils


class TestUtils(Utils):
    def test_find_element(self, monkeypatch):
        # Test should return the correct element from an iterable.
        data_test = {"name": "toto", "email": "toto@mail.fr", "points": "5"}
        self._mock_club_and_competition(monkeypatch)
        clubs = server.clubs
        club_name = data_test["name"]
        club_returned = find_element(clubs, club_name)
        assert club_returned["name"] == club_name
        assert club_returned["email"] == data_test["email"]

    def test_update_points_of_club(self, monkeypatch):
        # Test should return the updated club point number.
        data_test = {"club": "toto", "order_places": 2}
        self._mock_club_and_competition(monkeypatch)
        club = find_element(server.clubs, data_test["club"])
        number_points_after_order = int(club["points"])
        utils.update_points_of_club(club=club, numbers_places_ordered=int(data_test["order_places"]))
        assert club["points"] == number_points_after_order - int(data_test["order_places"])

    def test_update_competition_places_available(self, monkeypatch):
        # Test should retrun the updated competition places availables.
        data_test = {"competition": "Spring Festival", "order_places": 2}
        self._mock_club_and_competition(monkeypatch)
        competition = find_element(server.competitions, data_test["competition"])
        places_available_after_order = int(competition["numberOfPlaces"])
        utils.update_competition_places_available(competition, data_test["order_places"])
        assert competition["numberOfPlaces"] == places_available_after_order - int(data_test["order_places"])

    def test_add_competition_to_list_competition_booked_of_club(self, monkeypatch):
        # Test should add competition and the number of places booked to the club's list of reserved competitions.
        self._mock_club_and_competition(monkeypatch)
        club = find_element(server.clubs, "club_with_competition_booked")
        nomber_competition_booked = len(club["competitions_booked"])
        competition = find_element(server.competitions, "Fall Classic")
        places_ordered = 2
        utils.update_of_numbers_of_places_reserved_by_the_club(
            club=club, competition=competition, numbers_places_ordered=places_ordered
        )
        competition_booked = find_element(club["competitions_booked"], "Fall Classic")
        assert len(club["competitions_booked"]) == nomber_competition_booked + 1
        assert competition_booked["numbers_places_booked"] == places_ordered

    def test_update_of_numbers_of_places_reserved_by_the_club(self, monkeypatch):
        """
        The test must add the places ordered by the competition's key: numbers_places_booked
        to the club's:competitions_booked list.
        """
        self._mock_club_and_competition(monkeypatch)
        club = find_element(server.clubs, "club_with_competition_booked")
        competition = find_element(server.competitions, "Spring Festival")
        places_ordered = 2
        excepted_result = 9
        utils.update_of_numbers_of_places_reserved_by_the_club(
            club=club, competition=competition, numbers_places_ordered=places_ordered
        )
        competition_booked = find_element(club["competitions_booked"], "Spring Festival")
        assert competition_booked["numbers_places_booked"] == excepted_result

    def _raise_exception(self, club_name, competition_name, placesRequired, type_exception, monkeypatch, msg_error):
        # Test check if exception is raising and check error message.
        self._mock_club_and_competition(monkeypatch)
        club = find_element(server.clubs, club_name)
        competition = find_element(server.competitions, competition_name)
        with pytest.raises(type_exception) as exc_info:
            server.order_conditions(placesRequired, club, competition)

        assert str(exc_info.value) == msg_error

    def test_raise_exception_with_input_is_negative_number(self, monkeypatch):
        # Test should return LowerThanOneError Exception with placesRequired < 1.
        data_test = {"club": "Simply Lift", "competition": "Spring Festival", "places": -2}
        execpted_message = "Please enter a number greater than zero!"
        self._raise_exception(
            data_test["club"],
            data_test["competition"],
            data_test["places"],
            LowerThanOneError,
            monkeypatch,
            execpted_message,
        )

    def test_raise_exception_with_purchase_more_than_twelves_places(self, monkeypatch):
        # Test should return PlacesError Exception with placesRequired > 12.
        data_test = {"club": "toto", "competition": "Spring Festival", "places": 13}
        execpted_message = "The maximum reservation is 12 places!"
        self._raise_exception(
            data_test["club"],
            data_test["competition"],
            data_test["places"],
            PlacesError,
            monkeypatch,
            execpted_message,
        )

    def test_raise_exception_with_purchase_more_than_club_points(self, monkeypatch):
        # Test should return PlacesError Exception with placesRequired > club's points.
        data_test = {"club": "toto", "competition": "Spring Festival", "places": 7}
        execpted_message = "You can book 5 places maximum!"
        self._raise_exception(
            data_test["club"],
            data_test["competition"],
            data_test["places"],
            PlacesError,
            monkeypatch,
            execpted_message,
        )

    def test_raise_exception_with_purchase_more_places_than_available(self, monkeypatch):
        # Test should return PlacesError Exception with placesRequired > places available in the competition.
        data_test = {"club": "tata", "competition": "next competition", "places": 3}
        execpted_message = "There are only 2 places available!"
        self._raise_exception(
            data_test["club"],
            data_test["competition"],
            data_test["places"],
            PlacesError,
            monkeypatch,
            execpted_message,
        )

    def test_raise_exception_with_several_orders_with_more_than_twelves_places_in_total(self, monkeypatch):
        # Test should return PlacesError Exception with placesRequired > 12 (with several orders).
        data_test = {"club": "club_with_competition_booked", "competition": "Spring Festival", "places": 7}
        execpted_message = "The maximum reservation is 12 places!"
        self._raise_exception(
            data_test["club"],
            data_test["competition"],
            data_test["places"],
            PlacesError,
            monkeypatch,
            execpted_message,
        )
