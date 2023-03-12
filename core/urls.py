from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.user_list_view, name="users"),
    path("documents/", views.document_list_view, name="documents"),
    path("documents/<int:pk>/", views.document_retrieve_view, name="document"),
    path(
        "annotations/<document_uuid>/",
        views.annotation_list_view,
        name="annotations",
    ),
]
