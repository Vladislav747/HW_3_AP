from locust import HttpUser, task, between

class ShortenerUser(HttpUser):
    wait_time = between(0.5, 2)

    @task
    def create_link(self):
        self.client.post(
            "/links/shorten",
            json={"original_url": "https://example.com"}
        )

    @task(3)
    def access_link(self):
        self.client.get("/abc123")