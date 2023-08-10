from locust import HttpUser, task, between
from app import server


class ProjectPerfTest(HttpUser):
    wait_time = between(1, 5)

    @task
    def index(self):
        self.client.get("/")

    @task
    def redirect_index(self):
        self.client.get("/logout")

    @task
    def login(self):
        for club in server.clubs:
            self.client.post("/showSummary", {"email": club["email"]})

    @task
    def book(self):
        for competition in server.competitions:
            for club in server.clubs:
                self.client.get(f"/book/{competition['name']}/{club['name']}")

    @task
    def purchase(self):
        for competition in server.competitions:
            for club in server.clubs:
                data = {"club": club["name"], "competition": competition["name"], "places": 1}
                self.client.post("/purchasePlaces", data)

    @task
    def dashboard(self):
        for club in server.clubs:
            self.client.get(f"/dashboard/{club['name']}")
