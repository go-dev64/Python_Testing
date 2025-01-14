"""
Custom Exception class module
"""


class LowerThanOneError(Exception):
    """
    Exception class for less than one place reserved.
    Return error message.
    """

    def __str__(self) -> str:
        return "Please enter a number greater than zero!"


class PlacesError(Exception):
    def __init__(self, nombre_max_places, type_error=None):
        """
        Exception class for error number places.
        Return error message.

        Args:
            nombre_max_places (_type_: int): number of places available for reservation.
            type_error (_type_: str, optional): str describe error. Defaults to None.
        """
        self.nombre_max_places = nombre_max_places
        self.type_error = type_error

    def error_reservation_more_than_twelves_places(self) -> str:
        # Error message for booking more than twelves places.
        return "The maximum reservation is 12 places!"

    def error_club_points(self) -> str:
        # Error message for booking more places than club points.
        return f"You can book {self.nombre_max_places} places maximum!"

    def error_places_available(self):
        # Error message for booking more places than club points.
        return f"There are only {self.nombre_max_places} places available!"

    def __str__(self) -> str:
        if self.type_error == "error club points":
            return self.error_club_points()
        elif self.type_error == "error_places_available":
            return self.error_places_available()
        else:
            return self.error_reservation_more_than_twelves_places()


class PastCompetitionError(Exception):
    """
    Exception class for completed competitions.
    Return error message.
    """

    def __str__(self) -> str:
        return "Error: Booking impossible, competiton already finished!"
