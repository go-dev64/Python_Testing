import time
from locust import HttpUser, task, between
from app import server, utils


class ProjectPerfTest(HttpUser):
    # wait_time = between(1, 3)

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
                with self.client.post("/purchasePlaces", data, catch_response=True) as response:
                    if response.status_code == 403:
                        response.success()

    @task
    def dashboard(self):
        for club in server.clubs:
            self.client.get(f"/dashboard/{club['name']}")
