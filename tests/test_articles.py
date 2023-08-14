import copy
import itertools

from rest_framework.test import APITestCase

BASE_URL = "http://localhost:8000"

AUTH_BASE_URL = f"{BASE_URL}/auth"
REGISTRATION_URL = f"{AUTH_BASE_URL}/registration/"
LOGIN_URL = f"{AUTH_BASE_URL}/login/"

API_BASE_URL = f"{BASE_URL}/api"
ARTICLE_CREATE_ROOT_URL = f"{API_BASE_URL}/articles/add-root/"
ARTICLE_LIST_URL = f"{API_BASE_URL}/articles/"

valid_user_payload = {
    "username": "testuser",
    "email": "test@email.com",
    "password1": "testpassword",
    "password2": "testpassword",
}

valid_article_payload = {
    "title": "Test Article",
    "articleHtml": "<p>This is a test article</p>",
    "articleJson": "{}",
    "articleText": "This is a test article",
    "hidden": False,
}


class ArticleCreateRootTest(APITestCase):
    def setUp(self):
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]

    def test_successful_create_root_article(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        self.assertEqual(response.status_code, 201)
        self.assertIn("uuid", response.data)
        self.assertIn("user", response.data)
        self.assertIn("slug_full", response.data)

    def test_unsuccessful_create_root_article_missing_token(self):
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        self.assertEqual(response.status_code, 401)

    def test_unsuccessful_create_root_article_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token + "abc")
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        self.assertEqual(response.status_code, 401)

    def test_unsuccessful_create_root_article_missing_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        del invalid_article_payload["title"]
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, invalid_article_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_root_article_missing_article_html(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        del invalid_article_payload["articleHtml"]
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, invalid_article_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("article_html", response.data)

    def test_unsuccessful_create_root_article_empty_string_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        invalid_article_payload["title"] = ""
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, invalid_article_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_root_article_title_too_long(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        invalid_article_payload[
            "title"
        ] = """
            In physics, symmetry breaking is a phenomenon where a disordered but symmetric state collapses into an ordered, but less symmetric state. 
            This collapse is often one of many possible bifurcations that a particle can take as it approaches a lower energy state. 
            Due to the many possibilities, an observer may assume the result of the collapse to be arbitrary. 
            This phenomenon is fundamental to quantum field theory (QFT), and further, contemporary understandings of physics. 
            Specifically, it plays a central role in the Glashow–Weinberg–Salam model which forms part of the Standard model modelling the electroweak sector. 
            A (black) particle is always driven to lowest energy. In the proposed Z 2 mathbb {Z} {2}-Symmetric system, it has two possible (purple) states. 
            When it spontaneously breaks symmetry, it collapses into one of the two states. This phenomenon is known as spontaneous symmetry breaking. 
            A 3D representation of a particle in a symmetric system (a Higgs Mechanism) before assuming a lower energy state In an infinite system 
            (Minkowski spacetime) symmetry breaking occurs, however in a finite system (that is, any real super-condensed system), 
            the system is less predictable, but in many cases quantum tunneling occurs. 
            Symmetry breaking and tunneling relate through the collapse of a particle into non-symmetric state as it seeks a lower energy.
        """
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, invalid_article_payload)
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_root_article_invalid_article_json(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token + "abc")
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        invalid_article_payload["articleJson"] = "this is invalid json"
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, invalid_article_payload)
        self.assertEqual(response.status_code, 401)

    def test_successful_create_two_root_articles_with_same_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response_1 = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        response_2 = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 201)
        self.assertNotEqual(response_1.data["slug_full"], response_2.data["slug_full"])
        self.assertEqual(
            response_1.data["slug_full"] + "-1", response_2.data["slug_full"]
        )

    # test adding 10 articles with the same now, do they all come back with different slugs?
    def test_successful_create_ten_root_articles_with_same_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        responses = []
        for i in range(10):
            responses.append(
                self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
            )
        for response in responses:
            self.assertEqual(response.status_code, 201)

        for response_a, response_b in itertools.combinations(responses, 2):
            self.assertNotEqual(
                response_a.data["slug_full"], response_b.data["slug_full"]
            )

        all_articles = self.client.get(ARTICLE_LIST_URL)
        self.assertEqual(all_articles.status_code, 200)
        self.assertEqual(len(all_articles.data), 10)


class ArticleCreateChildTest(APITestCase):
    def setUp(self):
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        self.parent_slug = response.data["slug_full"]

    def test_successful_create_child_article(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            valid_article_payload,
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("uuid", response.data)
        self.assertIn("user", response.data)
        self.assertIn("slug_full", response.data)
        self.assertEqual(
            response.data["slug_full"], self.parent_slug + "/" + response.data["title"]
        )

    def test_unsuccessful_create_child_article_missing_token(self):
        response = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            valid_article_payload,
        )
        self.assertEqual(response.status_code, 401)

    def test_unsuccessful_create_child_article_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token + "abc")
        response = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            valid_article_payload,
        )
        self.assertEqual(response.status_code, 401)

    def test_unsuccessful_create_child_article_missing_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        del invalid_article_payload["title"]
        response = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            invalid_article_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_child_article_missing_article_html(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        del invalid_article_payload["articleHtml"]
        response = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            invalid_article_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("article_html", response.data)

    def test_unsuccessful_create_child_article_empty_string_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        invalid_article_payload["title"] = ""
        response = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            invalid_article_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_child_article_title_too_long(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        invalid_article_payload[
            "title"
        ] = """
            In physics, symmetry breaking is a phenomenon where a disordered but symmetric state collapses into an ordered, but less symmetric state. 
            This collapse is often one of many possible bifurcations that a particle can take as it approaches a lower energy state. 
            Due to the many possibilities, an observer may assume the result of the collapse to be arbitrary. 
            This phenomenon is fundamental to quantum field theory (QFT), and further, contemporary understandings of physics. 
            Specifically, it plays a central role in the Glashow–Weinberg–Salam model which forms part of the Standard model modelling the electroweak sector. 
            A (black) particle is always driven to lowest energy. In the proposed Z 2 mathbb {Z} {2}-Symmetric system, it has two possible (purple) states. 
            When it spontaneously breaks symmetry, it collapses into one of the two states. This phenomenon is known as spontaneous symmetry breaking. 
            A 3D representation of a particle in a symmetric system (a Higgs Mechanism) before assuming a lower energy state In an infinite system 
            (Minkowski spacetime) symmetry breaking occurs, however in a finite system (that is, any real super-condensed system), 
            the system is less predictable, but in many cases quantum tunneling occurs. 
            Symmetry breaking and tunneling relate through the collapse of a particle into non-symmetric state as it seeks a lower energy.
        """
        response = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            invalid_article_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_child_article_invalid_article_json(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token + "abc")
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        invalid_article_payload["articleJson"] = "this is invalid json"
        response = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            invalid_article_payload,
        )
        self.assertEqual(response.status_code, 401)

    def test_successful_create_two_child_articles_with_same_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response_1 = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            valid_article_payload,
        )
        response_2 = self.client.post(
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
            valid_article_payload,
        )
        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 201)
        self.assertNotEqual(response_1.data["slug_full"], response_2.data["slug_full"])
        self.assertEqual(
            response_1.data["slug_full"] + "-1", response_2.data["slug_full"]
        )

    # test adding 10 articles with the same now, do they all come back with different slugs?
    def test_successful_create_ten_child_articles_with_same_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        responses = []
        for i in range(10):
            responses.append(
                self.client.post(
                    f"{API_BASE_URL}/articles/{self.parent_slug}/add-child",
                    valid_article_payload,
                )
            )
        for response in responses:
            self.assertEqual(response.status_code, 201)

        for response_a, response_b in itertools.combinations(responses, 2):
            self.assertNotEqual(
                response_a.data["slug_full"], response_b.data["slug_full"]
            )

        all_articles = self.client.get(ARTICLE_LIST_URL)
        self.assertEqual(all_articles.status_code, 200)
        self.assertEqual(len(all_articles.data), 10)

    # test that object coming back is exactly what i think it is (just test keys and nested structure)


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
