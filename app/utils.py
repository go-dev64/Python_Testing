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
