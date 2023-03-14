from django.contrib.auth import get_user_model
from django.http import HttpResponse

from rest_framework import generics

from .models import Annotation, Document
from .serializers import AnnotationSerializer, DocumentSerializer, UserSerializer

# Create your views here.


def index(request):
    return HttpResponse("Being Dope -> Chilling -> Having Fun -> Smiling -> Being Dope")


class DocumentListAPIView(generics.ListAPIView):
    """View all documents"""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer


document_list_view = DocumentListAPIView.as_view()


class DocumentRetrieveAPIView(generics.RetrieveAPIView):
    """View one document"""

    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    lookup_field = "uuid"


document_retrieve_view = DocumentRetrieveAPIView.as_view()


class AnnotationListCreateAPIView(generics.ListCreateAPIView):
    """View annotations with a document"""

    serializer_class = AnnotationSerializer

    def get_queryset(self, *args, **kwargs):
        document_uuid = self.kwargs["document_uuid"]
        return Annotation.objects.filter(document__uuid=document_uuid)

    def create(self, request, *args, **kwargs):
        print(request.data)
        return super().create(request, *args, **kwargs)


annotation_list_create_view = AnnotationListCreateAPIView.as_view()


class UserListAPIView(generics.ListAPIView):
    """View all users"""

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer


user_list_view = UserListAPIView.as_view()
