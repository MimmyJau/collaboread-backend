from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.user_list_view, name="users"),
    path("articles/", views.article_list_view, name="articles"),
    path("articles/<uuid>/", views.article_retrieve_view, name="article"),
    path(
        "annotations/<article_uuid>/",
        views.annotation_list_create_view,
        name="annotations",
    ),
]
