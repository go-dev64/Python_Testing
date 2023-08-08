from app.custom_exception import LowerThanOneError, PlacesError


"""
Module to function
"""


def find_element(iterable, condition):
    return [x for x in iterable if x["name"] == condition][0]


def update_points_of_club(club, numbers_places_ordered):
    # Updating the number of club points after an order

    club["points"] = int(club["points"]) - numbers_places_ordered


def update_competition_places_available(competition, numbers_places_ordered):
    # Updating the number of places availables after an order

    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - numbers_places_ordered


def update_of_numbers_of_places_reserved_by_the_club(numbers_places_ordered, club, competition):
    """
    If it does not exist, add a new key to club dict, which will be a list of reserverd competitions,
    with a dict of competition and number places reserved, by the club.
    Elif it does not exist, add , to list, dict of cometition reserved with number of places reserved.
    Else, adds the number of places ordered to the number of places already reserved for the competition.

    Args:
        numbers_places_ordered (_type_): _description_
        club (_type_): _description_
        competition (_type_): _description_
    """
    if "competitions_booked" not in club:
        club["competitions_booked"] = [{"name": competition["name"], "numbers_places_booked": numbers_places_ordered}]
    elif len([x for x in club["competitions_booked"] if x["name"] == competition["name"]]) == 0:
        club["competitions_booked"].append(
            {"name": competition["name"], "numbers_places_booked": numbers_places_ordered}
        )
    else:
        update_competition_booked = find_element(club["competitions_booked"], competition["name"])
        update_competition_booked["numbers_places_booked"] += numbers_places_ordered


def update_data_club_and_competition(club, competition, numbers_places_ordered):
    # Update club's points and numbres of places booked of comeption, and competition places availables.
    update_of_numbers_of_places_reserved_by_the_club(numbers_places_ordered, club, competition)
    update_points_of_club(club, numbers_places_ordered)
    update_competition_places_available(competition, numbers_places_ordered)


def order_conditions(placesRequired, club, competition):
    """
    Defines the conditions for ordering competitions places and raise exceptions if conditions is not respected.

    Args:
        club (_type_): Club that reserves places of a competition.
        competition (_type_): Competition booked.
        placesRequired (_type_): Number of places ordered.

    Raises:
        LowerThanOneError: Exception for a order with fewer places than 1.
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
