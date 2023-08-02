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


class MaxPlacesError(Exception):
    """
    Exception class for more than 12 places reserved.
    Return error message.
    """

    def __str__(self) -> str:
        return "The maximum reservation is 12 places!"
