from flask import template_rendered
from contextlib import contextmanager


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
        ]

    @staticmethod
    def get_competitions():
        # Retrun cpmpetitons lists.
        return [
            {"name": "Spring Festival", "date": "2020-03-27 10:00:00", "numberOfPlaces": "25"},
            {"name": "Fall Classic", "date": "2020-10-22 13:30:00", "numberOfPlaces": "13"},
        ]
