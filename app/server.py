import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.utils import LowerThanOneError, PlacesError

bp = Blueprint("server", __name__)


def loadClubs():
    with open("app/clubs.json") as club:
        listOfClubs = json.load(club)["clubs"]
        return listOfClubs


def loadCompetitions():
    with open("app/competitions.json") as comp:
        listOfCompetitions = json.load(comp)["competitions"]
        return listOfCompetitions


competitions = loadCompetitions()
clubs = loadClubs()


@bp.route("/")
def index():
    return render_template("index.html")


@bp.route("/showSummary", methods=["POST"])
def showSummary():
    error = None
    try:
        club = [club for club in clubs if club["email"] == request.form["email"]][0]
    except:
        error = "Oups, Email inconnue!"
        return render_template("index.html", error=error), 400
    else:
        return render_template("welcome.html", club=club, competitions=competitions, list_of_clubs=clubs)


@bp.route("/book/<competition>/<club>")
def book(competition, club):
    error = None
    try:
        foundClub = [c for c in clubs if c["name"] == club][0]
        foundCompetition = [c for c in competitions if c["name"] == competition][0]
        today = datetime.today().timestamp()
        date_of_competition = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S").timestamp()
        assert date_of_competition > today
    except:
        flash("Error: Booking impossible, competiton already finished!")
        return render_template("welcome.html", club=foundClub, competitions=competitions, list_of_clubs=clubs), 400
    else:
        if foundClub and foundCompetition:
            return render_template("booking.html", club=foundClub, competition=foundCompetition)
        else:
            flash("Error: Something went wrong-please try again")
            return render_template("welcome.html", club=club, competitions=competitions, list_of_clubs=clubs)


@bp.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    error = None
    try:
        competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
        club = [c for c in clubs if c["name"] == request.form["club"]][0]
        placesRequired = int(request.form["places"])
        if placesRequired < 1:
            raise LowerThanOneError()
        elif placesRequired > 12:
            raise PlacesError(nombre_max_places=12)
        elif placesRequired > int(club["points"]):
            raise PlacesError(int(club["points"]), type_error="error_max_places")
        elif placesRequired > int(competition["numberOfPlaces"]):
            raise PlacesError(int(competition["numberOfPlaces"]), type_error="error_max_places")

    except LowerThanOneError as exc:
        error = exc
        return render_template("booking.html", club=club, competition=competition, error=error), 400

    except PlacesError as exc:
        error = exc
        return render_template("booking.html", club=club, competition=competition, error=error), 400

    except ValueError:
        error = "Please, Enter a number!"
        return render_template("booking.html", club=club, competition=competition, error=error), 400

    else:
        club["points"] = int(club["points"]) - placesRequired
        competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)


@bp.route("/dashboard/<club>")
def dashboard(club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    if foundClub:
        return render_template("dashboard.html", club=foundClub, list_of_clubs=clubs)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@bp.route("/logout")
def logout():
    return redirect(url_for("index"))
