from django.contrib.auth import get_user_model
from django.http import HttpResponse

from rest_framework import generics

from .models import Annotation, Article
from .serializers import AnnotationSerializer, ArticleSerializer, UserSerializer

# Create your views here.


def index(request):
    return HttpResponse("Being Dope -> Chilling -> Having Fun -> Smiling -> Being Dope")


class ArticleListAPIView(generics.ListAPIView):
    """View all articles"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer


article_list_view = ArticleListAPIView.as_view()


class ArticleRetrieveAPIView(generics.RetrieveAPIView):
    """View one article"""

    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    lookup_field = "uuid"


article_retrieve_view = ArticleRetrieveAPIView.as_view()


class AnnotationListCreateAPIView(generics.ListCreateAPIView):
    """View annotations with a article"""

    # We also select "article" for SlugRelatedField
    queryset = Annotation.objects.select_related("article")
    serializer_class = AnnotationSerializer

    def create(self, request, *args, **kwargs):
        """Temp conditional until we add auth"""
        if "user" not in request.data:
            request.data["user"] = 1
        return super().create(request, *args, **kwargs)


annotation_list_create_view = AnnotationListCreateAPIView.as_view()


class UserListAPIView(generics.ListAPIView):
    """View all users"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


user_list_view = UserListAPIView.as_view()
