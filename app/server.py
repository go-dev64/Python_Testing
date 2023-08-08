import json
from datetime import datetime
from flask import Blueprint, render_template, request, redirect, flash, url_for
from app.custom_exception import LowerThanOneError, PastCompetitionError, PlacesError
from app.utils import find_element, purchase_conditions, update_competition_booked_by_the_club

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
        foundClub = find_element(clubs, club)
        foundCompetition = find_element(competitions, competition)
        today = datetime.today().timestamp()
        date_of_competition = datetime.strptime(foundCompetition["date"], "%Y-%m-%d %H:%M:%S").timestamp()
        if date_of_competition < today:
            raise PastCompetitionError()
    except PastCompetitionError as msg:
        flash(msg)
        return render_template("welcome.html", club=foundClub, competitions=competitions, list_of_clubs=clubs), 400
    except:
        flash("Error: Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions, list_of_clubs=clubs), 400
    else:
        return render_template("booking.html", club=foundClub, competition=foundCompetition)


@bp.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    error = None
    try:
        competition = find_element(competitions, request.form["competition"])
        club = find_element(clubs, request.form["club"])
        placesRequired = int(request.form["places"])
        purchase_conditions(placesRequired, club, competition)

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
        update_competition_booked_by_the_club(club=club, competition=competition, placesRequired=placesRequired)
        club["points"] = int(club["points"]) - placesRequired
        competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
        flash("Great-booking complete!")
        return render_template("welcome.html", club=club, competitions=competitions)


@bp.route("/dashboard/<club>")
def dashboard(club):
    try:
        foundClub = find_element(clubs, club)
    except:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions), 400

    else:
        return render_template("dashboard.html", club=foundClub, list_of_clubs=clubs)


@bp.route("/logout")
def logout():
    return redirect(url_for("index"))
