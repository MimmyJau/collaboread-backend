from django.contrib.auth import get_user_model
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.views import APIView

from .models import Document
from .serializers import DocumentSerializer, UserSerializer

# Create your views here.


def index(request):
    return HttpResponse("Being Dope -> Chilling -> Having Fun -> Smiling -> Being Dope")


class ListDocuments(generics.ListAPIView):
    """View all documents"""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


class ListUser(generics.ListAPIView):
    """View all users"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
