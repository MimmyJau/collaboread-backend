from rest_framework.test import APITestCase

BASE_URL = "http://localhost:8000"
AUTH_BASE_URL = f"{BASE_URL}/auth"
REGISTRATION_URL = f"{AUTH_BASE_URL}/registration/"
LOGIN_URL = f"{AUTH_BASE_URL}/login/"


class UserRegistrationTest(APITestCase):
    def setUp(self):
        self.client.post(
            REGISTRATION_URL,
            {
                "email": "existing@email.com",
                "username": "existing",
                "password1": "existingpassword",
                "password2": "existingpassword",
            },
        )

    def test_successful_user_registration(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 201)

    def test_unsuccessful_user_registration_missing_username(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)

    def test_unsuccessful_user_registration_missing_email(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_unsuccessful_user_registration_missing_password1(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "username": "testuser",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password1", response.data)

    def test_unsuccessful_user_registration_missing_password2(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "username": "testuser",
                "password1": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password2", response.data)

    def test_unsuccessful_user_registration_passwords_not_matching(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "username": "testuser",
                "password1": "testpassword",
                "password2": "TESTPASSWORD",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_unsuccessful_user_registration_with_existing_email(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "existing@email.com",
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_unsuccessful_user_registration_with_existing_username(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "username": "existing",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)

    def test_unsuccessful_user_registration_with_existing_email_in_different_case(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "EXISTING@EMAIL.COM",
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("email", response.data)

    def test_unsuccessful_user_registration_with_existing_username_in_different_case(
        self,
    ):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "username": "EXISTING",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("username", response.data)


class UserLoginTest(APITestCase):
    def setUp(self):
        self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )

    def test_successful_login(self):
        response = self.client.post(
            LOGIN_URL,
            {
                "username": "testuser",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("key", response.data)

    def test_successful_login_case_insensitive(self):
        response = self.client.post(
            LOGIN_URL,
            {
                "username": "TESTUSER",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("key", response.data)

    def test_unsuccessful_login_nonexistent_username(self):
        response = self.client.post(
            LOGIN_URL,
            {
                "username": "wronguser",
                "password": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_unsuccessful_login_wrong_password(self):
        response = self.client.post(
            LOGIN_URL,
            {
                "username": "testuser",
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_unsuccessful_login_absent_username_field(self):
        response = self.client.post(
            LOGIN_URL,
            {
                "password": "wrongpassword",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_unsuccessful_login_absent_email_field(self):
        response = self.client.post(
            LOGIN_URL,
            {
                "username": "testuser",
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("password", response.data)
