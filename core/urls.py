from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.ListUser.as_view(), name="users"),
    path("documents/", views.ListDocuments.as_view(), name="documents"),
]
