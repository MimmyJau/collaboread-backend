from django.contrib.auth import get_user_model
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import AllowAny, IsAuthenticated

from accounts.serializers import UserSerializer
from .models import Annotation, Article
from .serializers import AnnotationSerializer, ArticleSerializer


def index(request):
    return HttpResponse("Being Dope -> Chilling -> Having Fun -> Smiling -> Being Dope")


class ArticleListAPIView(generics.ListAPIView):
    """View all articles"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


article_list_view = ArticleListAPIView.as_view()


class ArticleRetrieveAPIView(generics.RetrieveAPIView):
    """View one article"""

    permission_classes = [AllowAny]

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "uuid"


article_retrieve_view = ArticleRetrieveAPIView.as_view()


class AnnotationListCreateAPIView(generics.ListCreateAPIView):
    """View annotations with a article"""

    authentication_classes = [SessionAuthentication, TokenAuthentication]

    serializer_class = AnnotationSerializer

    def get_queryset(self):
        qs = Annotation.objects.filter(
            article__uuid=self.kwargs["article_uuid"],
            is_public=True,
        )  # SELECT Annotations for a specific Article
        qs = qs.select_related(
            "article"
        )  # SELECT Article info as well to remove duplicate query (for SlugRelatedField)
        return qs

    def create(self, request, *args, **kwargs):
        """Temp conditional until we add auth"""
        if "user" not in request.data:
            request.data["user"] = 1
        return super().create(request, *args, **kwargs)


annotation_list_create_view = AnnotationListCreateAPIView.as_view()


class AnnotationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """Retrive, Update, or Delete an annotation"""

    queryset = Annotation.objects.all()
    serializer_class = AnnotationSerializer
    lookup_field = "uuid"

    def update(self, request, *args, **kwargs):
        """Temp conditional until we add auth"""
        if "user" not in request.data:
            request.data["user"] = 1
        return super().update(request, *args, **kwargs)


annotation_retrieve_update_destroy_view = (
    AnnotationRetrieveUpdateDestroyAPIView.as_view()
)


class UserListAPIView(generics.ListAPIView):
    """View all users"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


user_list_view = UserListAPIView.as_view()
