import copy

from rest_framework.test import APITestCase

BASE_URL = "http://localhost:8000"

AUTH_BASE_URL = f"{BASE_URL}/auth"
REGISTRATION_URL = f"{AUTH_BASE_URL}/registration/"
LOGIN_URL = f"{AUTH_BASE_URL}/login/"

API_BASE_URL = f"{BASE_URL}/api"
ARTICLE_CREATE_ROOT_URL = f"{API_BASE_URL}/articles/add-root/"
ARTICLE_LIST_URL = f"{API_BASE_URL}/articles/"
ARTICLE_DETAIL_URL = f"{API_BASE_URL}/articles"

BOOKMARK_CREATE_URL = f"{API_BASE_URL}/bookmarks/"
BOOKMARK_DETAIL_URL = f"{API_BASE_URL}/bookmark"

BOOK_AT_BOOKMARK_RETRIEVE_URL = f"{API_BASE_URL}/book-at-bookmark/"


valid_user_payload = {
    "username": "testuser",
    "email": "test@email.com",
    "password1": "testpassword",
    "password2": "testpassword",
}

valid_user_payload_2 = {
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

valid_article_payload_2 = {
    "title": "Another Article",
    "articleHtml": "<p>This is a another article</p>",
    "articleJson": "{}",
    "articleText": "This is a another article",
    "hidden": False,
}

valid_article_payload_3 = {
    "title": "Third Article",
    "articleHtml": "<p>This is a third article</p>",
    "articleJson": "{}",
    "articleText": "This is a third article",
    "hidden": False,
}


def generate_bookmark_payload(article_path, index):
    return {
        "article": article_path,
        "highlight": [
            {
                "characterRange": {
                    "start": index,
                    "end": index,
                }
            }
        ],
    }


class BookmarkCreateTest(APITestCase):
    """
    All Bookmark create tests should be unsuccessful.
    To successfully create a new Bookmark, use PUTAsCreate.
    """

    def setUp(self):
        # Create user.
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create article.
        response = self.client.post(ARTICLE_CREATE_ROOT_URL, valid_article_payload)
        self.book_path = response.data["slug_full"]
        # Logout.
        self.client.credentials()

    def test_unsuccessful_bookmark_create_by_user(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.post(BOOKMARK_CREATE_URL, valid_bookmark_payload)
        self.assertEqual(response.status_code, 405)

    def test_unsuccessful_bookmark_create_by_nonuser(self):
        # Create bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.post(BOOKMARK_CREATE_URL, valid_bookmark_payload)
        self.assertEqual(response.status_code, 401)


class BookmarkUpdateTest(APITestCase):
    def setUp(self):
        # Create user.
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create article.
        self.book = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_article_payload
        ).data
        self.book_path = self.book["slug_full"]
        # Create child article.
        self.child = self.client.post(
            f"{API_BASE_URL}/articles/{self.book_path}/add-child/",
            valid_article_payload_2,
        ).data
        self.child_path = self.child["slug_full"]
        # Set URL path.
        self.BOOKMARK_UPDATE_URL = f"{BOOKMARK_DETAIL_URL}/{self.book_path}/"
        # Logout.
        self.client.credentials()

    def test_successful_bookmark_PUTAsCreate_by_user(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # PUTAsCreate bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, valid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["book"], "test-article")
        self.assertEqual(response.data["article"], "test-article")
        self.assertEqual(response.data["highlight"][0]["characterRange"]["start"], 5)
        self.assertEqual(response.data["highlight"][0]["characterRange"]["end"], 5)

    def test_successful_bookmark_update_by_user(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # PUTAsCreate bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, valid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["book"], "test-article")
        self.assertEqual(response.data["article"], "test-article")
        self.assertEqual(response.data["highlight"][0]["characterRange"]["start"], 5)
        self.assertEqual(response.data["highlight"][0]["characterRange"]["end"], 5)
        # Update bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.child_path, 9)
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, valid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["book"], "test-article")
        self.assertEqual(response.data["article"], "test-article/another-article")
        self.assertEqual(response.data["highlight"][0]["characterRange"]["start"], 9)
        self.assertEqual(response.data["highlight"][0]["characterRange"]["end"], 9)
        # Retrieve and check only one exists.
        response = self.client.get(f"{BOOKMARK_DETAIL_URL}/{self.book_path}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["book"], "test-article")
        self.assertEqual(response.data["article"], "test-article/another-article")
        self.assertEqual(response.data["highlight"][0]["characterRange"]["start"], 9)
        self.assertEqual(response.data["highlight"][0]["characterRange"]["end"], 9)

    def test_successful_bookmark_using_non_root_article(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        NON_ROOT_URL = f"{BOOKMARK_DETAIL_URL}/{self.child_path}/"
        response = self.client.put(NON_ROOT_URL, valid_bookmark_payload, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["book"], "test-article")
        self.assertEqual(response.data["article"], "test-article")
        self.assertEqual(response.data["highlight"][0]["characterRange"]["start"], 5)
        self.assertEqual(response.data["highlight"][0]["characterRange"]["end"], 5)

    def test_successful_bookmark_by_another_user_has_no_effect_on_first_bookmark(
        self,
    ):
        # Login as first user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, valid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["book"], "test-article")
        self.assertEqual(response.data["article"], "test-article")
        self.assertEqual(response.data["highlight"][0]["characterRange"]["start"], 5)
        self.assertEqual(response.data["highlight"][0]["characterRange"]["end"], 5)
        # Logout.
        self.client.credentials()
        # Create second user and store token.
        response_user_2 = self.client.post(REGISTRATION_URL, valid_user_payload_2)
        self.token_2 = response_user_2.data["key"]
        # Login as second user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_2)
        # Create second bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.child_path, 9)
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, valid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["book"], "test-article")
        self.assertEqual(response.data["article"], "test-article/another-article")
        self.assertEqual(response.data["highlight"][0]["characterRange"]["start"], 9)
        self.assertEqual(response.data["highlight"][0]["characterRange"]["end"], 9)
        # Logout.
        self.client.credentials()
        # Login as first user (again).
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Retrieve and check only one exists.  response = self.client.get(f"{BOOKMARK_DETAIL_URL}/{self.book_path}/")
        response = self.client.get(f"{BOOKMARK_DETAIL_URL}/{self.book_path}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["book"], "test-article")
        self.assertEqual(response.data["article"], "test-article")
        self.assertEqual(response.data["highlight"][0]["characterRange"]["start"], 5)
        self.assertEqual(response.data["highlight"][0]["characterRange"]["end"], 5)

    def test_unsuccessful_bookmark_update_by_nonuser(self):
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, valid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 401)

    def test_unsuccessful_bookmark_update_for_nonexistent_book(self):
        # Login as first user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create bookmark.
        NON_EXISTENT_BOOK_URL = f"{BOOKMARK_DETAIL_URL}/this-book-does-not-exist/"
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.put(
            NON_EXISTENT_BOOK_URL, valid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_unsuccessful_bookmark_update_missing_book_field(self):
        # Login as first user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create bookmark.
        NON_EXISTENT_BOOK_URL = f"{BOOKMARK_DETAIL_URL}/"
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.put(
            NON_EXISTENT_BOOK_URL, valid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 404)

    def test_unsuccessful_bookmark_update_missing_article_field(self):
        # Login as first user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create invalid bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        invalid_bookmark_payload = copy.deepcopy(valid_bookmark_payload)
        invalid_bookmark_payload.pop("article")
        # Post invalid bookmark.
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, invalid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_unsuccessful_bookmark_update_missing_highlight_field(self):
        # Login as first user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create invalid bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        invalid_bookmark_payload = copy.deepcopy(valid_bookmark_payload)
        invalid_bookmark_payload.pop("highlight")
        # Post invalid bookmark.
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, invalid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 400)

    def test_unsuccessful_bookmark_update_highlight_start_neq_highlight_end(self):
        # Login as first user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create invalid bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        invalid_bookmark_payload = copy.deepcopy(valid_bookmark_payload)
        invalid_bookmark_payload["highlight"][0]["characterRange"]["end"] = 6
        # Post invalid bookmark.
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, invalid_bookmark_payload, format="json"
        )
        self.assertEqual(response.status_code, 400)


class BookmarkRetrieveTest(APITestCase):
    def setUp(self):
        # Create user.
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create article.
        self.book = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_article_payload
        ).data
        self.book_path = self.book["slug_full"]
        # Create child article.
        self.child = self.client.post(
            f"{API_BASE_URL}/articles/{self.book_path}/add-child/",
            valid_article_payload_2,
        ).data
        self.child_path = self.child["slug_full"]
        # Set URL path.
        self.BOOKMARK_UPDATE_URL = f"{BOOKMARK_DETAIL_URL}/{self.book_path}/"
        self.PARENT_NODE_BOOKMARK_URL = f"{BOOKMARK_DETAIL_URL}/{self.book_path}/"
        self.CHILD_NODE_BOOKMARK_URL = f"{BOOKMARK_DETAIL_URL}/{self.child_path}/"
        # Create bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.put(
            self.BOOKMARK_UPDATE_URL, valid_bookmark_payload, format="json"
        )
        # Logout.
        self.client.credentials()

    def test_successful_bookmark_retrieve_by_user(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Retrieve bookmark
        response = self.client.get(self.PARENT_NODE_BOOKMARK_URL)
        self.assertEqual(response.status_code, 200)

    def test_successful_bookmark_retreive_by_user_in_another_section_of_book_with_bookmark(
        self,
    ):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Retrieve bookmark at child node.
        response = self.client.get(self.CHILD_NODE_BOOKMARK_URL)
        self.assertEqual(response.status_code, 200)

    def test_unsuccessful_bookmark_retrieve_by_another_user_in_section_with_bookmark(
        self,
    ):
        # Create second user and store token.
        response_user_2 = self.client.post(REGISTRATION_URL, valid_user_payload_2)
        self.token_2 = response_user_2.data["key"]
        # Login as second user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_2)
        response = self.client.get(self.PARENT_NODE_BOOKMARK_URL)
        self.assertEqual(response.status_code, 204)

    def test_unsuccessful_bookmark_retrieve_by_another_user_in_section_other_than_section_with_bookmark(
        self,
    ):
        # Create second user and store token.
        response_user_2 = self.client.post(REGISTRATION_URL, valid_user_payload_2)
        self.token_2 = response_user_2.data["key"]
        # Login as second user.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token_2)
        response = self.client.get(self.CHILD_NODE_BOOKMARK_URL)
        self.assertEqual(response.status_code, 204)

    def test_unsuccessful_bookmark_retrieve_by_nonuser(self):
        response = self.client.get(self.CHILD_NODE_BOOKMARK_URL)
        self.assertEqual(response.status_code, 401)


class BookmarkListTest(APITestCase):
    def test_successful_bookmark_list_by_user(self):
        pass

    def test_successful_empty_bookmark_list_by_user(self):
        pass

    def test_unsuccessful_bookmark_list_by_another_user(self):
        pass

    def test_unsuccessful_bookmark_list_by_nonuser(self):
        pass


class BookmarkDeleteTest(APITestCase):
    def test_successful_bookmark_delete_by_user(self):
        pass

    def test_unsuccessful_bookmark_delete_of_nonexistent_bookmark_by_user(self):
        pass

    def test_unsuccessful_bookmark_delete_of_nonexistent_bookmark_by_another_user(self):
        pass

    def test_unsuccessful_bookmark_delete_of_nonexistent_bookmark_by_nonuser(self):
        pass


class ArticleListWithBookmarkTest(APITestCase):
    def setUp(self):
        # Create user.
        response = self.client.post(REGISTRATION_URL, valid_user_payload)
        self.token = response.data["key"]
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create article.
        self.book = self.client.post(
            ARTICLE_CREATE_ROOT_URL, valid_article_payload
        ).data
        self.book_path = self.book["slug_full"]
        # Create first child article.
        self.child = self.client.post(
            f"{API_BASE_URL}/articles/{self.book_path}/add-child/",
            valid_article_payload_2,
        ).data
        self.child_path = self.child["slug_full"]
        # Create second child article.
        self.child_2 = self.client.post(
            f"{API_BASE_URL}/articles/{self.book_path}/add-child/",
            valid_article_payload_3,
        ).data
        self.child_path_2 = self.child_2["slug_full"]
        # Set URL path.
        self.PARENT_NODE_BOOKMARK_URL = f"{BOOKMARK_DETAIL_URL}/{self.book_path}/"
        self.CHILD_1_NODE_BOOKMARK_URL = f"{BOOKMARK_DETAIL_URL}/{self.child_path}/"
        self.CHILD_2_NODE_BOOKMARK_URL = f"{BOOKMARK_DETAIL_URL}/{self.child_path_2}/"
        self.BOOK_LIST_URL = f"{API_BASE_URL}/articles/"
        # Logout.
        self.client.credentials()

    def test_successful_return_root_bookmark_path_to_user(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create bookmark at root.
        valid_bookmark_payload = generate_bookmark_payload(self.book_path, 5)
        response = self.client.put(
            self.PARENT_NODE_BOOKMARK_URL, valid_bookmark_payload, format="json"
        )
        # Retrieve book.
        response = self.client.get(self.BOOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        book_data = response.data[0]
        self.assertEqual(book_data["bookmark_path"], self.book_path)

    def test_successful_return_child_bookmark_path_to_user(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Create bookmark at child.
        valid_bookmark_payload = generate_bookmark_payload(self.child_path, 9)
        response = self.client.put(
            self.CHILD_1_NODE_BOOKMARK_URL, valid_bookmark_payload, format="json"
        )
        # Retrieve book.
        response = self.client.get(self.BOOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        book_data = response.data[0]
        self.assertEqual(book_data["bookmark_path"], self.child_path)

    def test_successful_return_null_bookmark_path_to_user_if_there_is_no_bookmark(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Retrieve book.
        response = self.client.get(self.BOOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        book_data = response.data[0]
        self.assertEqual(book_data["bookmark_path"], None)

    def test_successful_return_null_bookmark_path_to_nonuser(self):
        # Login.
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token)
        # Update bookmark.
        valid_bookmark_payload = generate_bookmark_payload(self.child_path, 9)
        response = self.client.put(
            self.PARENT_NODE_BOOKMARK_URL, valid_bookmark_payload, format="json"
        )
        # Logout
        self.client.credentials()
        # Retrieve book.
        response = self.client.get(self.BOOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        book_data = response.data[0]
        self.assertEqual(book_data["bookmark_path"], None)
