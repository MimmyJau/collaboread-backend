from rest_framework.test import APITestCase

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


class BookmarkCreateTest(APITestCase):
    def test_successful_bookmark_create_by_user(self):
        pass

    def test_unsuccessful_bookmark_create_another_bookmark_by_user(self):
        # unclear what should happen here.
        # either 1) old bookmark is deleted or 2) new bookmark is not created.
        pass

    def test_unsuccessful_bookmark_create_by_nonuser(self):
        pass

    def test_unsuccessful_bookmark_create_missing_book_field(self):
        pass

    def test_unsuccessful_bookmark_create_missing_article_field(self):
        pass

    def test_unsuccessful_bookmark_create_missing_highlight_field(self):
        pass

    def test_unsuccessful_bookmark_create_highlight_start_neq_highlight_end(self):
        pass


class BookmarkUpdateTest(APITestCase):
    def test_successful_bookmark_update_by_user(self):
        pass

    def test_successful_bookmark_PUTAsCreate_by_user(self):
        pass

    def test_unsuccessful_bookmark_update_by_another_user(self):
        pass

    def test_unsuccessful_bookmark_update_by_nonuser(self):
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
