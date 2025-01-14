import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.custom_exception import LowerThanOneError, PastCompetitionError, PlacesError
from app.utils import find_element, order_conditions, update_data_club_and_competition

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
    except LookupError:
        error = "Oups, Email inconnue!"
        return render_template("index.html", error=error), 403
    else:
        return render_template("welcome.html", club=club, competitions=competitions)


@bp.route("/book/<competition>/<club>")
def book(competition, club):
    try:
        foundClub = find_element(clubs, club)
        foundCompetition = find_element(competitions, competition)
        today = datetime.today().timestamp()
        date_of_competition = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S").timestamp()
        if date_of_competition < today:
            raise PastCompetitionError()
    except PastCompetitionError as msg:
        flash(msg)
        return render_template("welcome.html", club=foundClub, competitions=competitions), 403
    except LookupError:
        flash("Error: Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions), 403
    else:
        return render_template("booking.html", club=foundClub, competition=foundCompetition)


@bp.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    error = None
    try:
        competition = find_element(competitions, request.form["competition"])
        club = find_element(clubs, request.form["club"])
        placesRequired = int(request.form["places"])
        order_conditions(placesRequired, club, competition)

    except LowerThanOneError as msg:
        error = msg
        return render_template("booking.html", club=club, competition=competition, error=error), 403

    except PlacesError as msg:
        error = msg
        return render_template("booking.html", club=club, competition=competition, error=error), 403

    except ValueError:
        error = "Please, Enter a number!"
        return render_template("booking.html", club=club, competition=competition, error=error), 403

    else:
        update_data_club_and_competition(club=club, competition=competition, numbers_places_ordered=placesRequired)
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)


@bp.route("/dashboard/<club>")
def dashboard(club):
    try:
        foundClub = find_element(clubs, club)
    except LookupError:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions), 403

    else:
        return render_template("dashboard.html", club=foundClub, list_of_clubs=clubs)


@bp.route("/logout")
def logout():
    return redirect(url_for("index"))
