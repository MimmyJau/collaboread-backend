from rest_framework.test import APITestCase

BASE_URL = "http://localhost:8000"

AUTH_BASE_URL = f"{BASE_URL}/auth"
REGISTRATION_URL = f"{AUTH_BASE_URL}/registration/"
LOGIN_URL = f"{AUTH_BASE_URL}/login/"

API_BASE_URL = f"{BASE_URL}/api"
ARTICLE_CREATE_ROOT_URL = f"{API_BASE_URL}/articles/add-root/"


class ArticleCreateTest(APITestCase):
    def setUp(self):
        response = self.client.post(
            REGISTRATION_URL,
            {
                "username": "testuser",
                "email": "test@email.com",
                "password1": "testpassword",
                "password2": "testpassword",
            },
        )
        self.token = response.data["key"]

    def test_successful_create_root_article(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL,
            {
                "title": "Test Article",
                "articleHtml": "<p>This is a test article</p>",
                "articleJson": "{}",
                "articleText": "This is a test article",
                "hidden": False,
            },
        )
        print(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn("uuid", response.data)
        self.assertIn("user", response.data)
        self.assertIn("slug_full", response.data)

    def test_unsuccessful_create_root_article_missing_token(self):
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL,
            {
                "title": "Test Article",
                "articleHtml": "<p>This is a test article</p>",
                "articleJson": "{}",
                "articleText": "This is a test article",
                "hidden": False,
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_unsuccessful_create_root_article_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token + "abc")
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL,
            {
                "title": "Test Article",
                "articleHtml": "<p>This is a test article</p>",
                "articleJson": "{}",
                "articleText": "This is a test article",
                "hidden": False,
            },
        )
        self.assertEqual(response.status_code, 401)

    def test_unsuccessful_create_root_article_missing_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL,
            {
                "articleHtml": "<p>This is a test article</p>",
                "articleJson": "{}",
                "articleText": "This is a test article",
                "hidden": False,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_unsuccessful_create_root_article_missing_article_html(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL,
            {
                "title": "Test Article",
                "articleJson": "{}",
                "articleText": "This is a test article",
                "hidden": False,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("non_field_errors", response.data)

    def test_unsuccessful_create_root_article_empty_string_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL,
            {
                "title": "",
                "articleHtml": "<p>This is a test article</p>",
                "articleJson": "{}",
                "articleText": "This is a test article",
                "hidden": False,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_root_article_title_too_long(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL,
            {
                "title": "In physics, symmetry breaking is a phenomenon where a disordered but symmetric state collapses into an ordered, but less symmetric state. This collapse is often one of many possible bifurcations that a particle can take as it approaches a lower energy state. Due to the many possibilities, an observer may assume the result of the collapse to be arbitrary. This phenomenon is fundamental to quantum field theory (QFT), and further, contemporary understandings of physics. Specifically, it plays a central role in the Glashow–Weinberg–Salam model which forms part of the Standard model modelling the electroweak sector. A (black) particle is always driven to lowest energy. In the proposed Z 2 mathbb {Z} {2}-Symmetric system, it has two possible (purple) states. When it spontaneously breaks symmetry, it collapses into one of the two states. This phenomenon is known as spontaneous symmetry breaking. A 3D representation of a particle in a symmetric system (a Higgs Mechanism) before assuming a lower energy state In an infinite system (Minkowski spacetime) symmetry breaking occurs, however in a finite system (that is, any real super-condensed system), the system is less predictable, but in many cases quantum tunneling occurs. Symmetry breaking and tunneling relate through the collapse of a particle into non-symmetric state as it seeks a lower energy.",
                "articleHtml": "<p>This is a test article</p>",
                "articleJson": "{}",
                "articleText": "This is a test article",
                "hidden": False,
            },
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_root_article_invalid_article_json(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token + "abc")
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL,
            {
                "title": "Test Article",
                "articleHtml": "<p>This is a test article</p>",
                "articleJson": "invalid json",
                "articleText": "This is a test article",
                "hidden": False,
            },
        )
        self.assertEqual(response.status_code, 401)


class ArticleListTest(APITestCase):
    # test that list returns if logged in
    # test that list returns if not logged in
    pass


class ArticleRetrieveTest(APITestCase):
    # test that article returns if logged in
    # test that article returns if not logged in
    # test that
    pass


class ArticleUpdateTest(APITestCase):
    pass


class ArticleDeleteTest(APITestCase):
    pass
