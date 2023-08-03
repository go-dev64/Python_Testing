import pytest
from app import server
from tests.conftest import captured_templates


class MockReponse:
    """
    Mock clubs and competitions

    Returns:
        _type_: Mock of clubs and cpmpettions.
    """

    @staticmethod
    def get_clubs():
        # Return clubs lists.
        return [
            {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
            {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
            {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
            {"name": "toto", "email": "toto@mail.fr", "points": "5"},
        ]

    @staticmethod
    def get_competitions():
        # Retrun cpmpetitons lists.
        return [
            {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
            {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
            {"name": "next competition", "date": "2025-10-22 13:30:00", "numberOfPlaces": "13"},
        ]

    def _mock_club_and_competition(self, monkeypatch):
        return monkeypatch.setattr(server, "clubs", self.get_clubs()), monkeypatch.setattr(
            server, "competitions", self.get_competitions()
        )


class Utils(MockReponse):
    def get_response_value_and_template_context(
        self, captured_templates, client, monkeypatch, method, route, *args, **kwargs
    ):
        """
        Method to return response value , Template returned and context returned.

        Args:
            captured_templates (_type_): _description_
            client (_type_): _description_
            monkeypatch (_type_): _description_
            method (_type_): _description_
            route (_type_): _description_

        Returns:
            _type_: response_value of request, template returned and context returned.
        """
        self._mock_club_and_competition(monkeypatch=monkeypatch)
        if method == "GET":
            rv = client.get(route)
            template, context = captured_templates[0]
            return rv, template, context
        elif method == "POST":
            rv = client.post(route, **kwargs)
            template, context = captured_templates[0]
            return rv, template, context
