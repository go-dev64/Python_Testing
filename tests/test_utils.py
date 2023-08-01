from flask import template_rendered
from contextlib import contextmanager
import pytest
from app import server


"""@contextmanager
def captured_templates(app):
    recorded = []

    def record(sender, template, context, **extra):
        recorded.append((template, context))

    template_rendered.connect(record, app)
    try:
        yield recorded
    finally:
        template_rendered.disconnect(record, app)"""


def captured_templates(app, recorded, **extra):
    def record(sender, template, context):
        recorded.append((template, context))

    return template_rendered.connected_to(record, app)


class MockReponse:
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
