"""
Full test on user authentication, signup, login, logout, user details(me)
"""
from tests import TestConfig

class TestSignUp(TestConfig):
    """
    Testing the api/v1/signup endpoint
    """

    def test_signup_with_incorrect_method(self):
        """
        Testing sign up with methods other than post method
        """
        endpoint = 'api/v1/signup'
        resp1 = self.client.get(endpoint)
        resp2 = self.client.put(endpoint)
        resp3 = self.client.delete(endpoint)

        for res in [resp1, resp2, resp3]:
            self.assertEqual(res.status_code, 405)
            print(res.data)