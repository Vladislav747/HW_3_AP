from locust import HttpUser, task, between
from faker import Faker

class ShortenerUser(HttpUser):
    host = "http://localhost:8000"
    wait_time = between(0.5, 2)
    fake = Faker()

    def generate_random_credentials(self):
        login = self.fake.user_name()
        password = self.fake.password()
        return login, password

    @task
    def create_user(self):
        login, password = self.generate_random_credentials()
        self.client.post(
            "/user/create",
            json={"login": login, "password": password}
        )

    @task(3)
    def expired_links(self):
        self.client.get("/links/expired")