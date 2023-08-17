from app.custom_exception import LowerThanOneError, PastCompetitionError, PlacesError


class TestException:
    def test_lower_than_one_error(self):
        # Test should return a msg error "Please enter a number greater than zero!" with order less than 1.
        test = LowerThanOneError()
        assert test.__str__() == "Please enter a number greater than zero!"

    def test_error_reservation_more_than_twelves_places(self):
        # Test should return a msg error "The maximum reservation is 12 places!" with order more than 12.
        test = PlacesError(
            nombre_max_places=15,
        )
        assert test.__str__() == "The maximum reservation is 12 places!"

    def test_error_club_points(self):
        # Test should return a msg error "You can book 3 places maximum!" with order more than club's points.
        test = PlacesError(nombre_max_places=3, type_error="error club points")
        assert test.__str__() == "You can book 3 places maximum!"

    def test_error_places_available(self):
        # Test should return a msg error "There are only 5 places available!" with order more than places available.
        test = PlacesError(nombre_max_places=5, type_error="error_places_available")
        assert test.__str__() == "There are only 5 places available!"

    def test_past_competition_error(self):
        # Test should return a msg error "Error: Booking impossible, competiton already finished!" with old competition.
        test = PastCompetitionError()
        assert test.__str__() == "Error: Booking impossible, competiton already finished!"
