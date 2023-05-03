from django.contrib.auth import get_user_model
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.serializers import UserSerializer
from .models import Annotation, Article, ArticleMP, Comment
from .permissions import IsOwnerOrReadOnly
from .serializers import (
    AnnotationReadSerializer,
    AnnotationWriteSerializer,
    ArticleSerializer,
    ArticleListSerializer,
    ArticleMPSerializer,
    CommentSerializer,
)


def index(request):
    return HttpResponse("Being Dope -> Chilling -> Having Fun -> Smiling -> Being Dope")


class ArticleListAPIView(generics.ListAPIView):
    """View all articles"""

    queryset = ArticleMP.get_root_nodes()
    serializer_class = ArticleListSerializer


article_list_view = ArticleListAPIView.as_view()


class ArticleRetrieveAPIView(generics.RetrieveUpdateAPIView):
    """View one article"""

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    queryset = ArticleMP.get_root_nodes()
    serializer_class = ArticleMPSerializer
    lookup_field = "uuid"

    def update(self, request, *args, **kwargs):
        request.data["user"] = request.user
        return super().update(request, *args, **kwargs)


article_retrieve_view = ArticleRetrieveAPIView.as_view()


class AnnotationListCreateAPIView(generics.ListCreateAPIView):
    """View annotations with a article"""

    authentication_classes = [SessionAuthentication, TokenAuthentication]

    def get_queryset(self):
        qs = Annotation.objects.filter(
            article__uuid=self.kwargs["article_uuid"],
        )  # SELECT Annotations for a specific Article
        qs = qs.select_related(
            "article"
        )  # SELECT Article info as well to remove duplicate query (for SlugRelatedField)
        return qs

    def get_serializer_class(self):
        if self.request.method == "GET":
            return AnnotationReadSerializer
        return AnnotationWriteSerializer

    def create(self, request, *args, **kwargs):
        """Temp conditional until we add auth"""
        request.data["user"] = request.user
        return super().create(request, *args, **kwargs)


annotation_list_create_view = AnnotationListCreateAPIView.as_view()


class AnnotationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrive, Update, or Delete an annotation"""

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Annotation.objects.all()
    serializer_class = AnnotationWriteSerializer
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


class CommentListCreateAPIView(generics.ListCreateAPIView):
    """List your comments and create a comment."""

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = CommentSerializer

    def get_queryset(self):
        qs = Comment.objects.filter(user=self.request.user)
        return qs

    def create(self, request, *args, **kwargs):
        request.data["user"] = request.user
        return super().create(request, *args, **kwargs)


comment_list_create_view = CommentListCreateAPIView.as_view()


class CommentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrive, Update, or Delete a comment."""

    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    lookup_field = "uuid"

    def update(self, request, *args, **kwargs):
        request.data["user"] = request.user
        return super().update(request, *args, **kwargs)


comment_retrieve_update_destroy_view = CommentRetrieveUpdateDestroyAPIView.as_view()
