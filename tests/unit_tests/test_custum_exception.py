from app.custom_exception import FindElementError, LowerThanOneError, PastCompetitionError, PlacesError


class TestException:
    def test_lower_than_one_error(self):
        test = LowerThanOneError()
        assert test.__str__() == "Please enter a number greater than zero!"

    def test_error_reservation_more_than_twelves_places(self):
        test = PlacesError(
            nombre_max_places=15,
        )
        assert test.__str__() == "The maximum reservation is 12 places!"

    def test_error_club_points(self):
        test = PlacesError(nombre_max_places=3, type_error="error club points")
        assert test.__str__() == "You can book 3 places maximum!"

    def test_error_places_available(self):
        test = PlacesError(nombre_max_places=5, type_error="error_places_available")
        assert test.__str__() == "There are only 5 places available!"

    def test_past_competition_error(self):
        test = PastCompetitionError()
        assert test.__str__() == "Error: Booking impossible, competiton already finished!"

    def test_fnd_element_error(self):
        test = FindElementError("element")
        assert test.__str__() == "Error: element inconnu!"
