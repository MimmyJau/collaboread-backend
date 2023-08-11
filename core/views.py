import uuid

from django.contrib.auth import get_user_model
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from rest_framework import generics, status
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import (
    IsAuthenticated,
    IsAuthenticatedOrReadOnly,
)
from rest_framework.response import Response

from accounts.serializers import UserSerializer
from .mixins import AllowPUTAsCreateMixin, MultipleFieldLookupMixin
from .models import Annotation, Article, Bookmark, Comment
from .permissions import IsOwnerOrReadOnly, IsOwnerOnly
from .serializers import (
    AnnotationSerializer,
    ArticleSerializer,
    ArticleListSerializer,
    BookmarkSerializer,
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


class ArticleCreateRootAPIView(generics.CreateAPIView):
    """Create a root article"""

    serializer_class = ArticleSerializer
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        """
        Override create because by default, CreateAPIView passes validated_data to
        .to_representation(), which throws an error since validated_data is an
        OrderedDict, not an Article object. Thus it cannot properly call @property
        methods like `prev` and `next`.

        Instead, we pass the newly created instance to .to_representation() in the
        same way a GET request would.
        """
        request.data["user"] = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        instance = self.perform_create(serializer)
        serializer = self.get_serializer(instance)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )

    def perform_create(self, serializer):
        """We override this method to use MP_Node's API."""
        return Article.create_root(**serializer.validated_data)


article_create_root_view = ArticleCreateRootAPIView.as_view()


class ArticleCreateChildAPIView(generics.CreateAPIView):
    pass


article_create_child_view = ArticleCreateChildAPIView.as_view()


class ArticleCreateSiblingAPIView(generics.CreateAPIView):
    pass


article_create_sibling_view = ArticleCreateSiblingAPIView.as_view()


class ArticleRetrieveUpdateAPIView(generics.RetrieveUpdateAPIView):
    """View one article"""

    authentication_classes = [TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly]

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "slug_full"

    def update(self, request, *args, **kwargs):
        request.data["user"] = request.user
        return super().update(request, *args, **kwargs)


article_retrieve_update_view = ArticleRetrieveUpdateAPIView.as_view()


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


class BookmarkCreateAPIView(generics.CreateAPIView):
    """List and create Bookmarks"""

    serializer_class = BookmarkSerializer

    def get_queryset(self):
        return Bookmark.objects.filter(user=self.request.user)

    def create(self, request, *args, **kwargs):
        print(request.user)
        request.data["user"] = request.user
        return super().create(request, *args, **kwargs)


bookmark_create_view = BookmarkCreateAPIView.as_view()


class BookmarkRetrieveUpdateAPIView(
    AllowPUTAsCreateMixin, generics.RetrieveUpdateAPIView
):
    """Retrieve or update Bookmark"""

    # SessionAuthentication is needed for the browsable API
    # Source: https://stackoverflow.com/a/38626166
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsOwnerOnly]

    queryset = Bookmark.objects.all()
    serializer_class = BookmarkSerializer

    def get_object(self):
        queryset = self.get_queryset()
        # Need the .id: https://stackoverflow.com/a/71108056
        queryset = queryset.filter(user=self.request.user.id)
        queryset = queryset.filter(book__slug_full=self.kwargs.get("book"))
        obj = get_object_or_404(queryset)  # Lookup the object
        self.check_object_permissions(self.request, obj)
        return obj

    def update(self, request, *args, **kwargs):
        request.data["user"] = request.user
        return super().update(request, *args, **kwargs)


bookmark_retrieve_update_view = BookmarkRetrieveUpdateAPIView.as_view()
