from rest_framework.test import APITestCase

BASE_URL = "http://localhost:8000"
AUTH_BASE_URL = f"{BASE_URL}/auth"
REGISTRATION_URL = f"{AUTH_BASE_URL}/registration/"


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

    def test_registration(self):
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

    def test_registration_missing_username(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_registration_missing_email(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "username": "testuser",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_registration_missing_password1(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "username": "testuser",
                "password2": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_registration_missing_password2(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "email": "test@email.com",
                "username": "testuser",
                "password1": "testpassword",
            },
        )
        self.assertEqual(response.status_code, 400)

    def test_registration_passwords_not_matching(self):
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

    def test_registration_with_existing_email(self):
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

    def test_registration_with_existing_username(self):
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

    def test_registration_with_existing_email_in_different_case(self):
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

    def test_registration_with_existing_username_in_different_case(self):
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
