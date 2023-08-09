from locust import HttpUser, task
from app import server


class ProjectPerfTest(HttpUser):
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
                self.client.post("/showSummary", data)

    @task
    def dashboard(self):
        for club in server.clubs:
            self.client.get(f"/dashboard/{club['name']}")
