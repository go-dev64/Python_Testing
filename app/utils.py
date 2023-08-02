"""
Custom Exception class module
"""


class LowerThanOneError(BaseException):
    """
    Exception class for less than one place reserved.
    Return error message.
    """

    def __str__(self) -> str:
        return "Please enter a number greater than zero!"

    def __repr__(self) -> str:
        return "Please enter a number greater than zero!"


class MaxPlacesError(BaseException):
    """
    Exception class for more than 12 places reserved.
    Return error message.
    """

    def __str__(self) -> str:
        return "The maximum reservation is 12 places!"

    def __repr__(self) -> str:
        return "The maximum reservation is 12 places!"


class ClubPointsExceededError(BaseException):
    """
    Exception class for number places booked more than club's points.
    Return error message.
    """

    def __init__(self, club_points):
        self.club_point = club_points

    def __str__(self) -> str:
        return f"You can book {self.club_point} places maximum!"

    def __repr__(self) -> str:
        return f"You can book {self.club_point} places maximum!"
