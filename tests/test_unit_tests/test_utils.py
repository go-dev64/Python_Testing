from app.utils import find_element
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
