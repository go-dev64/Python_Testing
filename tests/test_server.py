def test_email_is_db(client):
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
