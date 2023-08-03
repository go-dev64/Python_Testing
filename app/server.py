import json
from flask import Blueprint, render_template, request, redirect, flash, url_for

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
    foundClub = [c for c in clubs if c["name"] == club][0]
    foundCompetition = [c for c in competitions if c["name"] == competition][0]
    if foundClub and foundCompetition:
        return render_template("booking.html", club=foundClub, competition=foundCompetition)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@bp.route("/purchasePlaces", methods=["POST"])
def purchasePlaces():
    competition = [c for c in competitions if c["name"] == request.form["competition"]][0]
    club = [c for c in clubs if c["name"] == request.form["club"]][0]
    placesRequired = int(request.form["places"])
    competition["numberOfPlaces"] = int(competition["numberOfPlaces"]) - placesRequired
    flash("Great-booking complete!")
    return render_template("welcome.html", club=club, competitions=competitions)


@bp.route("/home/<club>")
def home(club):
    foundClub = [c for c in clubs if c["name"] == club][0]
    if foundClub:
        return render_template("booking.html", club=foundClub, list_of_clubs=clubs)
    else:
        flash("Something went wrong-please try again")
        return render_template("welcome.html", club=club, competitions=competitions)


@bp.route("/logout")
def logout():
    return redirect(url_for("index"))
