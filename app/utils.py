from app.custom_exception import LowerThanOneError, PlacesError


"""
Module to function
"""


def find_element(iterable, condition):
    return [x for x in iterable if x["name"] == condition][0]


def update_competition_booked_by_the_club(placesRequired, club, competition):
    if "competitions_booked" not in club:
        club["competitions_booked"] = []
        club["competitions_booked"].append({"name": competition["name"], "numbers_places_booked": 0})
    if competition["name"] not in club["competitions_booked"]:
        club["competitions_booked"].append({"name": competition["name"], "numbers_places_booked": 0})
    update_competition_booked = [c for c in club["competitions_booked"] if c["name"] == competition["name"]][0]
    update_competition_booked["numbers_places_booked"] += placesRequired


def purchase_conditions(placesRequired, club, competition):
    """
    Defines the conditions for ordering competitions places and raise exceptions if conditions is not respected.

    Args:
        club (_type_): Club that reserves places of a competition.
        competition (_type_): Competition booked.
        placesRequired (_type_): Number of places ordered.

    Raises:
        LowerThanOneError: Exception for a order with fewer places than 1.
        PlacesError: _description_
        PlacesError: _description_
        PlacesError: _description_
        PlacesError: _description_
    """
    if placesRequired < 1:
        raise LowerThanOneError()

    elif placesRequired > 12:
        raise PlacesError(nombre_max_places=12)

    elif placesRequired > int(club["points"]):
        raise PlacesError(int(club["points"]), type_error="error club points")

    elif placesRequired > int(competition["numberOfPlaces"]):
        raise PlacesError(int(competition["numberOfPlaces"]), type_error="error_places_available")

    elif "competitions_booked" in club:
        competition_booked = [c for c in club["competitions_booked"] if c["name"] == competition["name"]]
        if len(competition_booked) == 1:
            nomber_places_booked = int(competition_booked[0]["numbers_places_booked"])
            total_order = nomber_places_booked + placesRequired
            if total_order > 12:
                raise PlacesError(nombre_max_places=12)
