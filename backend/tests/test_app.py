from tests import TestConfig


class TestApp(TestConfig):
    """
    Test app.py, testing the base endpoint of the api
    """
    def test_base_endpoint(self):
        """
        Test base endpoint
        """
        resp = self.client.get("/")
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json["message"], "Welcome to dummy api")

    def test_base_endpoint_with_unsafe_methods(self):
        """
        Test base endpoint with either post/push/patch/delete
        """
        resp = self.client.post("/")
        resp2 = self.client.put("/")
        resp3 = self.client.delete("/")
        resp4 = self.client.patch("/")
        for res in [resp, resp2, resp3, resp4]:
            self.assertEqual(res.status_code, 405)
