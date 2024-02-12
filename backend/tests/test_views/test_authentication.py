"""
Full test on user authentication, signup, login, logout, user details(me)
"""
from tests import TestConfig
from models.user import User

class TestSignUp(TestConfig):
    """
    Testing the api/v1/signup endpoint
    """
    def setUp(self):
        self.endpoint = "api/v1/signup"
        super().setUp()
    
    

    def test_signup_with_incorrect_method(self):
        """
        Testing sign up with methods other than post method
        """
        resp1 = self.client.get(self.endpoint)
        resp2 = self.client.put(self.endpoint)
        resp3 = self.client.delete(self.endpoint)

        for res in [resp1, resp2, resp3]:
            self.assertEqual(res.status_code, 405)
            self.assertRegex(res.data.decode('utf-8'), r".*Method Not Allowed.*")

    def test_signup_with_none_passed_as_json(self):
        """
        Tests that the application doesn't break when none is passed as json value
        """
        resp = self.client.post(self.endpoint, json=None, headers={"content-type": "application/json"})
        self.assertEqual(resp.status_code, 400)

    def test_signup_with_incomplete_credentials(self):
        """
        Testing signp with incomplete credentials
        """
        expected_err_msg = "email, password, confirm_password fields are all required"
        # test without an email

        resp = self.client.post(self.endpoint, json={"password": "134", "confirm_password": "134"})

        # test without password
        resp2 = self.client.post(self.endpoint, json={"email":"johndoe@mail.com"})

        #test without confirm password
        resp3 = self.client.post(self.endpoint, json={"email": "johndoe@mail.com", "password": "142"})

        
        for res in [resp, resp2, resp3]:

            self.assertEqual(res.status_code, 401)
            self.assertEqual(res.json["error"], expected_err_msg)
        

    def test_signup_with_complete_credentials_but_with_short_passwords(self):
        """
        Testing signup with short password, password must atleast be 8 characters to pass this test
        """
        expected_err_msg = "Password validation failed"
        resp = self.client.post(self.endpoint, json={"email": "johndoe@mail.com", "password": "1235", "confirm_password": "1235"})
        resp2 = self.client.post(self.endpoint, json={"email": "johndoe@mail.com", "password": "1235353", "confirm_password": "1235353"})
        resp3 = self.client.post(self.endpoint, json={"email": "johndoe@mail.com", "password": None, "confirm_password": None})
        
        for res in [resp, resp2]:
            self.assertEqual(res.status_code, 401)
            self.assertEqual(res.json["error"], expected_err_msg)
        self.assertEqual(resp3.status_code, 401)
        self.assertEqual(resp3.json["error"], "email, password, confirm_password fields are all required")


    def test_signup_with_complete_credentials_but_with_non_matching_passwords(self):
        """
        Tests signup endpoint with non matching password and confirm password field
        """
        expected_err_msg = "Password validation failed"
        resp = self.client.post(self.endpoint, json={"email": "johndoe@mail.com", "password": "282802503985", "confirm_password": "0250852708522"})
        self.assertEqual(resp.status_code, 401)
        self.assertEqual(resp.json["error"], expected_err_msg)

    def test_signup_with_complete_and_correct_credentials(self):
        """
        Test signup when the user provides complete and correct credentials
        """

        expected_success_msg = "Account registered successfully"
        resp = self.client.post(self.endpoint, json={"email":"johndoe@mail.com", "password": "123456789", "confirm_password": "123456789"})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json["message"], expected_success_msg)
        # confirm user was created
        with self.app.app_context():
            q = User.query.all()
            print(q)
            self.assertEqual(len(q), 1)
            self.assertEqual(q[0].email, "johndoe@mail.com")

    def test_signup_with_already_existing_email(self):
        """
        Test signup with already existing email
        """
        expected_success_msg = "Account registered successfully"
        expected_err_msg = "Account already exists, please login"
        resp = self.client.post(self.endpoint, json={"email":"johndoe@mail.com", "password": "123456789", "confirm_password": "123456789"})
        self.assertEqual(resp.status_code, 201)
        self.assertEqual(resp.json["message"], expected_success_msg)

       
        # attempt to create another user with same email
        resp2 = self.client.post(self.endpoint, json={"email":"johndoe@mail.com", "password": "password", "confirm_password": "password"})
        self.assertEqual(resp2.status_code, 202)
        self.assertEqual(resp2.json["message"], expected_err_msg)

         # confirm we still have only one user in the database
        with self.app.app_context():
            q = User.query.all()
            self.assertEqual(len(q), 1)
            self.assertEqual(q[0].email, "johndoe@mail.com")
 