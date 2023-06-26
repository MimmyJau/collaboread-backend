from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

from core.models import Article, Annotation


class CommentAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            username="testuser", email="test@test.com", password="testpassword"
        )
        self.article = Article.objects.create(
            user=self.user,
            title="Test Article",
            article_html="<p>Test Article HTML</p>",
            article_json={"test": "Test Article JSON"},
            article_text="Test Article Text",
        )
        self.annotation = Annotation.objects.create(
            user=self.user,
            article=self.article,
            highlight_start=0,
            highlight_end=10,
        )
        self.comment = {
            "user": self.user.uuid,
            "article": self.article.uuid,
            "annotation": self.annotation.uuid,
            "comment_html": "<p>Test Comment</p>",
            "comment_json": {"test": "Test Comment JSON"},
            "comment_text": "Test Comment",
        }

    def test_post_comment(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post("/api/comments/", self.comment, format="json")
        self.assertEqual(response.status_code, 201)

    def test_get_annotation(self):
        self.client.login(username="testuser", password="testpassword")
        response = self.client.post("/api/comments/", self.comment, format="json")
        route = f"/api/articles/{self.article.uuid}/annotations/"
        response = self.client.get(route)
        self.assertEqual(response.status_code, 200)
        print("response data:", response.data[0])
        self.assertEqual(response.data[0]["comment_html"], "<p>Test Comment</p>")
