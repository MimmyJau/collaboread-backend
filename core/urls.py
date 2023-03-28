from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("users/", views.user_list_view, name="users"),
    path("articles/", views.article_list_view, name="articles"),
    path("articles/<uuid>/", views.article_retrieve_view, name="article"),
    path(
        "articles/<article_uuid>/annotations/",
        views.annotation_list_create_view,
        name="get_annotations",
    ),
    path(
        "annotations/<uuid>/",
        views.annotation_retrieve_update_destroy_view,
        name="retrieve_update_destroy_annotations",
    ),
]
