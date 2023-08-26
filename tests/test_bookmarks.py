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
        self.assertEqual(response.status_code, 405)


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
        self.BOOKMARK_UPDATE_URL = f"{API_BASE_URL}/bookmark/{self.book_path}/"
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

    def test_unsuccessful_bookmark_update_by_another_user(self):
        pass

    def test_unsuccessful_bookmark_update_by_nonuser(self):
        pass

    def test_unsuccessful_bookmark_update_for_nonexistent_book(self):
        pass

    def test_unsuccessful_bookmark_update_missing_book_field(self):
        pass

    def test_unsuccessful_bookmark_update_missing_article_field(self):
        pass

    def test_unsuccessful_bookmark_update_missing_highlight_field(self):
        pass

    def test_unsuccessful_bookmark_update_highlight_start_neq_highlight_end(self):
        pass


class BookmarkRetrieveTest(APITestCase):
    def test_successful_bookmark_retrieve_by_user(self):
        pass

    def test_successful_bookmark_returns_nothing_if_section_has_no_bookmark(self):
        pass

    def test_unsuccessful_bookmark_retrieve_by_another_user(self):
        pass

    def test_unsuccessful_bookmark_retrieve_by_nonuser(self):
        pass


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


class ArticleRetrieveWithBookmarkTest(APITestCase):
    def test_successful_retrieve_book_section_with_bookmark_by_user(self):
        pass

    def test_successful_retrieve_book_first_section_without_bookmark_by_user(self):
        pass

    def test_successful_retrieve_book_first_section_without_bookmark_by_nonuser(self):
        pass


class ArticleListWithBookmarkTest(APITestCase):
    def test_successful_retrieve_list_of_books_with_bookmarks_by_user(self):
        pass

    def test_successful_retrieve_empty_list_of_books_with_bookmarks_by_user(self):
        pass

    def test_unsuccessful_retrieve_list_of_books_with_bookmarks_by_another_user(self):
        pass

    def test_unsuccessful_retrieve_list_of_books_with_bookmarks_by_nonuser(self):
        pass
