from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
import uuid

from accounts.serializers import UserSerializer
from .models import Annotation, Article, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    AnnotationSerializer,
    ArticleSerializer,
    ArticleListSerializer,
    CommentSerializer,
    TableOfContentsSerializer,
)


def index(request):
    return HttpResponse("Being Dope -> Chilling -> Having Fun -> Smiling -> Being Dope")


class ArticleListAPIView(generics.ListAPIView):
    """View all articles"""

    queryset = Article.get_root_nodes().filter(hidden=False)
    serializer_class = ArticleListSerializer


article_list_view = ArticleListAPIView.as_view()


class ArticleRetrieveAPIView(generics.RetrieveUpdateAPIView):
    """View one article"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug_full"

    def update(self, request, *args, **kwargs):
        request.data["user"] = request.user
        return super().update(request, *args, **kwargs)


article_retrieve_view = ArticleRetrieveAPIView.as_view()


class TableOfContentsRetrieveView(generics.RetrieveAPIView):
    """Get table of contents of an article"""

    queryset = Article.objects.all()
    serializer_class = TableOfContentsSerializer
    lookup_field = "slug_full"


table_of_contents_retrieve_view = TableOfContentsRetrieveView.as_view()


class AnnotationListCreateAPIView(generics.ListCreateAPIView):
    """View annotations with a article"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = AnnotationSerializer

    def get_queryset(self):
        # SELECT Annotations for a specific Article
        qs = Annotation.objects.filter(
            article__slug_full=self.kwargs["slug_full"],
        )
        # SELECT public annotations or user's annotations
        # Need conditional depending on whether user is logged in or not
        if self.request.user.is_authenticated:
            qs = qs.filter(Q(is_public=True) | Q(user=self.request.user))
        else:
            qs = qs.filter(is_public=True)
        # SELECT Article info as well to remove duplicate query (for SlugRelatedField)
        qs = qs.select_related("article")
        return qs

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user
        if "uuid" not in request.data:
            request.data["uuid"] = uuid.uuid4()
        return super().create(request, *args, **kwargs)


annotation_list_create_view = AnnotationListCreateAPIView.as_view()


class AnnotationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrive, Update, or Delete an annotation"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    lookup_field = "uuid"

    def update(self, request, *args, **kwargs):
        """Temp conditional until we add auth"""
        request.data["user"] = request.user
        return super().update(request, *args, **kwargs)


annotation_retrieve_update_destroy_view = (
    AnnotationRetrieveUpdateDestroyAPIView.as_view()
)


class UserListAPIView(generics.ListAPIView):
    """View all users"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


user_list_view = UserListAPIView.as_view()


class CommentCreateAPIView(generics.CreateAPIView):
    """List your comments and create a comment."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        qs = Comment.objects.filter(user=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user
        return super().create(request, *args, **kwargs)


comment_create_view = CommentCreateAPIView.as_view()


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrive, Update, or Delete a comment."""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "uuid"

    def update(self, request, *args, **kwargs):
        request.data["user"] = request.user
        return super().update(request, *args, **kwargs)


comment_retrieve_update_destroy_view = CommentRetrieveUpdateDestroyAPIView.as_view()
