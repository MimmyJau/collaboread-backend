from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("articles/", views.article_list_view, name="articles"),
    path("toc/<slug_full>/", views.table_of_contents_retrieve_view, name="toc"),
    path(
        "articles/<path:slug_full>/annotations/",
        views.annotation_list_create_view,
        name="annotations",
    ),
    path("articles/<path:slug_full>/", views.article_retrieve_view, name="article"),
    path(
        "annotations/<uuid>/",
        views.annotation_retrieve_update_destroy_view,
        name="annotation",
    ),
    path("comments/", views.comment_create_view, name="comments"),
    path(
        "comments/<uuid>/", views.comment_retrieve_update_destroy_view, name="comment"
    ),
]
