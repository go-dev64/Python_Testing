from app import server
from app.server import showSummary


def test_email_is_db(client, mocker):
    # mock data json in clubs
    mocker.patch.object(
        server,
        "clubs",
        {"name": "Simply Lift", "email": "john@simplylift.co", "points": "13"},
        {"name": "Iron Temple", "email": "admin@irontemple.com", "points": "4"},
        {"name": "She Lifts", "email": "kate@shelifts.co.uk", "points": "12"},
    )
    # check if email is in clubs email.
    email = "admin@irontemple.com"
    response = client.post("/showSummary", data={"email": email})
    assert response.status_code == 200


def test_email_is_not_in_db(client):
    # check if email is not in clubs email and retrun error msg.
    email = "autremail"
    response = client.post("/showSummary", data={"email": email})
    assert b"error" in response.data
    assert response.status_code == 404
