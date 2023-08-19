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
ARTICLE_DETAIL_URL = f"{API_BASE_URL}/articles"

valid_user_payload = {
    "username": "testuser",
    "email": "test@email.com",
    "password1": "testpassword",
    "password2": "testpassword",
}

valid_second_user_payload = {
    "username": "anotheruser",
    "email": "another@email.com",
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

valid_update_article_payload = {
    "title": "New Article",
    "articleHtml": "<p>This is a new article</p>",
    "articleJson": "{}",
    "articleText": "This is a new article",
    "hidden": False,
}


valid_hidden_article_payload = {
    "title": "Test Article",
    "articleHtml": "<p>This is a test article</p>",
    "articleJson": "{}",
    "articleText": "This is a test article",
    "hidden": True,
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
            response_1.data["slug_full"] + "-2", response_2.data["slug_full"]
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
        # Create first user and store token.
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        self.parent_slug = response.data["slug_full"]
        self.ARTICLE_CREATE_CHILD_URL = (
            f"{API_BASE_URL}/articles/{self.parent_slug}/add-child/"
        )
        self.client.credentials()

        # Create second user and store token.
        response_user_2 = self.client.post(REGISTRATION_URL, valid_second_user_payload)
        self.token_2 = response_user_2.data["key"]

    def test_successful_create_child_article(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
            valid_article_payload,
        )
        self.assertEqual(response.status_code, 201)
        self.assertIn("uuid", response.data)
        self.assertIn("user", response.data)
        self.assertIn("slug_full", response.data)
        self.assertEqual(response.data["slug_full"], self.parent_slug + "/test-article")

    def test_successful_create_child_article_of_a_child_article(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        responses = []
        url = self.ARTICLE_CREATE_CHILD_URL
        for i in range(10):
            responses.append(
                self.client.post(
                    url,
                    valid_article_payload,
                )
            )
            url = (
                f"{API_BASE_URL}/articles/{responses[-1].data['slug_full']}/add-child/"
            )
        for idx, response in enumerate(responses):
            self.assertEqual(response.status_code, 201)
            self.assertIn("uuid", response.data)
            self.assertIn("user", response.data)
            self.assertIn("slug_full", response.data)
            if idx == 0:
                parent_slug = self.parent_slug
            else:
                parent_slug = responses[idx - 1].data["slug_full"]
            self.assertEqual(response.data["slug_full"], parent_slug + "/test-article")

    def test_unsuccessful_create_child_article_missing_token(self):
        response = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
            valid_article_payload,
        )
        self.assertEqual(response.status_code, 401)

    def test_unsuccessful_create_child_article_invalid_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token + "abc")
        response = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
            valid_article_payload,
        )
        self.assertEqual(response.status_code, 401)

    def test_unsuccessful_create_child_article_missing_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        del invalid_article_payload["title"]
        response = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
            invalid_article_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_child_article_missing_article_html(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        del invalid_article_payload["articleHtml"]
        response = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
            invalid_article_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("article_html", response.data)

    def test_unsuccessful_create_child_article_empty_string_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        invalid_article_payload["title"] = ""
        response = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
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
            self.ARTICLE_CREATE_CHILD_URL,
            invalid_article_payload,
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn("title", response.data)

    def test_unsuccessful_create_child_article_invalid_article_json(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token + "abc")
        invalid_article_payload = copy.deepcopy(valid_article_payload)
        invalid_article_payload["articleJson"] = "this is invalid json"
        response = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
            invalid_article_payload,
        )
        self.assertEqual(response.status_code, 401)

    def test_successful_create_two_child_articles_with_same_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response_1 = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
            valid_article_payload,
        )
        response_2 = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
            valid_article_payload,
        )
        self.assertEqual(response_1.status_code, 201)
        self.assertEqual(response_2.status_code, 201)
        self.assertNotEqual(response_1.data["slug_full"], response_2.data["slug_full"])
        self.assertEqual(
            response_1.data["slug_full"] + "-2", response_2.data["slug_full"]
        )

    # test adding 10 articles with the same now, do they all come back with different slugs?
    def test_successful_create_ten_child_articles_with_same_title(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        responses = []
        for i in range(10):
            responses.append(
                self.client.post(
                    self.ARTICLE_CREATE_CHILD_URL,
                    valid_article_payload,
                )
            )
        for response in responses:
            self.assertEqual(response.status_code, 201)

        for response_a, response_b in itertools.combinations(responses, 2):
            self.assertNotEqual(
                response_a.data["slug_full"], response_b.data["slug_full"]
            )

        root_articles = self.client.get(ARTICLE_LIST_URL)
        self.assertEqual(root_articles.status_code, 200)
        self.assertEqual(len(root_articles.data), 1)

    # add child to a non-existent parent node
    def test_unsuccessful_create_child_article_of_nonexistent_parent(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.post(
            f"{API_BASE_URL}/articles/non-existent-node/add-child/",
            valid_article_payload,
        )
        self.assertEqual(response.status_code, 404)

    def test_unsuccessful_create_child_article_for_parent_owned_by_another_user(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_2)
        response = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL,
            valid_article_payload,
        )
        self.assertEqual(response.status_code, 403)


class ArticleListTest(APITestCase):
    def setUp(self):
        # Create first user and store token.
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create root article.
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        # Create hidden root article.
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_hidden_article_payload
        )
        parent_slug = response.data["slug_full"]
        # Create child article.
        self.client.post(
            f"{API_BASE_URL}/articles/{parent_slug}/add-child/",
            valid_article_payload,
        )
        self.client.credentials()

        # Create second user and store token.
        response_user_2 = self.client.post(REGISTRATION_URL, valid_second_user_payload)
        self.token_2 = response_user_2.data["key"]
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create root article.
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        # Create hidden root article.
        response = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_hidden_article_payload
        )
        parent_slug = response.data["slug_full"]
        # Create child article.
        self.client.post(
            f"{API_BASE_URL}/articles/{parent_slug}/add-child/",
            valid_article_payload,
        )
        self.client.credentials()

    def test_successful_list_articles_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get(ARTICLE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)

    def test_successful_list_articles_without_token(self):
        response = self.client.get(ARTICLE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data), 2)


class ArticleRetrieveTest(APITestCase):
    # test that article returns if logged in
    def setUp(self):
        # Create user.
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create parent.
        self.parent = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_article_payload
        ).data
        # Create visible child.
        self.ARTICLE_CREATE_CHILD_URL = (
            f"{API_BASE_URL}/articles/{self.parent['slug_full']}/add-child/"
        )
        self.child = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL, valid_article_payload
        ).data
        self.client.credentials()

    def test_successful_retrieve_parent_article_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{self.parent['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.json())
        self.assertIn("slugFull", response.json())
        self.assertIn("user", response.json())
        self.assertIn("articleHtml", response.json())
        self.assertIn("next", response.json())
        self.assertIn("prev", response.json())

    def test_successful_retrieve_child_article_with_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{self.child['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.json())
        self.assertIn("slugFull", response.json())
        self.assertIn("user", response.json())
        self.assertIn("articleHtml", response.json())
        self.assertIn("next", response.json())
        self.assertIn("prev", response.json())

    def test_successful_retrieve_parent_article_without_token(self):
        response = self.client.get(
            f"{ARTICLE_DETAIL_URL}/{self.parent['slug_full']}/",
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.json())
        self.assertIn("slugFull", response.json())
        self.assertIn("user", response.json())
        self.assertIn("articleHtml", response.json())
        self.assertIn("next", response.json())
        self.assertIn("prev", response.json())

    def test_successful_retrieve_child_article_without_token(self):
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{self.child['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.json())
        self.assertIn("slugFull", response.json())
        self.assertIn("user", response.json())
        self.assertIn("articleHtml", response.json())

    def test_unsuccessful_retrieve_of_hidden_root_article_without_token(self):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        hidden_root = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_hidden_article_payload
        ).data
        self.client.credentials()
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{hidden_root['slug_full']}/")
        self.assertEqual(response.status_code, 404)

    def test_unsuccessful_retrieve_of_hidden_root_article_with_token_but_not_owner(
        self,
    ):
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        hidden_root = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_hidden_article_payload
        ).data
        self.client.credentials()
        # Create second user.
        response = self.client.post(REGISTRATION_URL, valid_second_user_payload)
        another_user_token = response.data["key"]
        # Login as second user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + another_user_token)
        # Retrieve hidden root article.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{hidden_root['slug_full']}/")
        self.assertEqual(response.status_code, 404)

    def test_unsuccessful_retrieve_of_hidden_child_article_without_token(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create hidden child.
        hidden_child = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL, valid_hidden_article_payload
        ).data
        # Logout.
        self.client.credentials()
        # Attempt to get hidden article.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{hidden_child['slug_full']}/")
        self.assertEqual(response.status_code, 404)

    def test_unsuccessful_retrieve_of_hidden_child_article_with_token_but_not_owner(
        self,
    ):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create hidden child.
        hidden_child = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL, valid_hidden_article_payload
        ).data
        # Logout.
        self.client.credentials()
        # Create second user.
        response = self.client.post(REGISTRATION_URL, valid_second_user_payload)
        another_user_token = response.data["key"]
        # Login as second user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + another_user_token)
        # Attempt to get hidden article.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{hidden_child['slug_full']}/")
        self.assertEqual(response.status_code, 404)

    def test_successful_retreive_of_hidden_root_article_as_owner(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create hidden root.
        hidden_root = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_hidden_article_payload
        ).data
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{hidden_root['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.json())
        self.assertIn("slugFull", response.json())
        self.assertIn("user", response.json())
        self.assertIn("articleHtml", response.json())
        self.assertIn("next", response.json())
        self.assertIn("prev", response.json())

    def test_successful_retreive_of_hidden_child_article_as_owner(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create hidden child.
        hidden_child = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL, valid_hidden_article_payload
        ).data
        # Attempt to get hidden article.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{hidden_child['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("title", response.json())
        self.assertIn("slugFull", response.json())
        self.assertIn("user", response.json())
        self.assertIn("articleHtml", response.json())
        self.assertIn("next", response.json())
        self.assertIn("prev", response.json())

    # test returning article that has a <script> or other dangerous tags that bleach does not allow


class ArticleUpdateTest(APITestCase):
    def setUp(self):
        # Create user.
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create parent.
        self.parent = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_article_payload
        ).data
        # Create visible child.
        self.ARTICLE_CREATE_CHILD_URL = (
            f"{API_BASE_URL}/articles/{self.parent['slug_full']}/add-child/"
        )
        self.child = self.client.post(
            self.ARTICLE_CREATE_CHILD_URL, valid_article_payload
        ).data
        # Create grandchild.
        self.ARTICLE_CREATE_GRANDCHILD_URL = (
            f"{API_BASE_URL}/articles/{self.child['slug_full']}/add-child/"
        )
        self.grandchild = self.client.post(
            self.ARTICLE_CREATE_GRANDCHILD_URL, valid_article_payload
        ).data
        self.client.credentials()

    def test_successful_update_of_own_root_article(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Update article.
        response = self.client.put(
            f"{ARTICLE_DETAIL_URL}/{self.parent['slug_full']}/",
            valid_update_article_payload,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["title"], "New Article")
        # Important to check that update changes slug / path
        self.assertEqual(response.json()["slugFull"], "new-article")
        # Check that child's path also changed.
        URL = f"{ARTICLE_DETAIL_URL}/new-article/test-article/"
        child = self.client.get(URL)
        self.assertEqual(child.status_code, 200)
        self.assertEqual(child.json()["slugFull"], "new-article/test-article")
        # Check that grandchild's path also changed.
        URL = f"{ARTICLE_DETAIL_URL}/new-article/test-article/test-article/"
        grandchild = self.client.get(URL)
        self.assertEqual(grandchild.status_code, 200)
        self.assertEqual(
            grandchild.json()["slugFull"], "new-article/test-article/test-article"
        )

    # test successful update own child article (any of the fields)
    def test_successful_update_of_child_article(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Update article.
        child = self.client.put(
            f"{ARTICLE_DETAIL_URL}/{self.child['slug_full']}/",
            valid_update_article_payload,
        )
        child = self.client.get(f"{ARTICLE_DETAIL_URL}/test-article/new-article/")
        self.assertEqual(child.status_code, 200)
        self.assertEqual(child.json()["title"], "New Article")
        self.assertEqual(child.json()["slugFull"], "test-article/new-article")
        # Check that grandchild's path also changed.
        URL = f"{ARTICLE_DETAIL_URL}/test-article/new-article/test-article/"
        grandchild = self.client.get(URL)
        self.assertEqual(grandchild.status_code, 200)
        self.assertEqual(
            grandchild.json()["slugFull"], "test-article/new-article/test-article"
        )

    def test_unsuccesful_update_of_non_existent_article(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Update article.
        response_from_put = self.client.put(
            f"{ARTICLE_DETAIL_URL}/non-existent-article/",
            valid_update_article_payload,
        )
        self.assertEqual(response_from_put.status_code, 404)
        response_from_get = self.client.get(
            f"{ARTICLE_DETAIL_URL}/non-existent-article/",
        )
        self.assertEqual(response_from_get.status_code, 404)

    def test_unsuccessful_update_of_root_article_by_user_that_is_not_owner(self):
        # Register new user.
        response = self.client.post(REGISTRATION_URL, valid_second_user_payload)
        second_token = response.data["key"]
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + second_token)
        # Update article.
        response = self.client.put(
            f"{ARTICLE_DETAIL_URL}/{self.parent['slug_full']}/",
            valid_update_article_payload,
        )
        self.assertEqual(response.status_code, 403)
        # Get article just to make sure.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{self.parent['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slugFull"], "test-article")

    def test_unsuccessful_update_of_child_article_by_user_that_is_not_owner(self):
        # Register new user.
        response = self.client.post(REGISTRATION_URL, valid_second_user_payload)
        second_token = response.data["key"]
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + second_token)
        # Update article.
        response = self.client.put(
            f"{ARTICLE_DETAIL_URL}/{self.child['slug_full']}/",
            valid_update_article_payload,
        )
        self.assertEqual(response.status_code, 403)
        # Get root article just to make sure.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{self.parent['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slugFull"], "test-article")
        # Get child article just to make sure.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{self.child['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slugFull"], "test-article/test-article")
        # Get grandchild article just to make sure.
        response = self.client.get(
            f"{ARTICLE_DETAIL_URL}/{self.grandchild['slug_full']}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["slugFull"], "test-article/test-article/test-article"
        )

    # test unsuccessful update if not logged in
    def test_unsuccessful_update_of_root_article_if_not_logged_in(self):
        response = self.client.put(
            f"{ARTICLE_DETAIL_URL}/{self.parent['slug_full']}/",
            valid_update_article_payload,
        )
        self.assertEqual(response.status_code, 401)
        # Get article just to make sure.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{self.parent['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slugFull"], "test-article")

    def test_unsuccessful_update_of_child_article_if_not_logged_in(self):
        response = self.client.put(
            f"{ARTICLE_DETAIL_URL}/{self.child['slug_full']}/",
            valid_update_article_payload,
        )
        self.assertEqual(response.status_code, 401)
        # Get root article just to make sure.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{self.parent['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slugFull"], "test-article")
        # Get child article just to make sure.
        response = self.client.get(f"{ARTICLE_DETAIL_URL}/{self.child['slug_full']}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["slugFull"], "test-article/test-article")
        # Get grandchild article just to make sure.
        response = self.client.get(
            f"{ARTICLE_DETAIL_URL}/{self.grandchild['slug_full']}/"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["slugFull"], "test-article/test-article/test-article"
        )

    # test making an article hidden
    # test successful move node to root and that all of its children slugs update prooperly


class ArticleDeleteTest(APITestCase):
    pass
