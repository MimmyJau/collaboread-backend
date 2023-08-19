from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "articles/<path:parent_path>/add-child/",
        views.article_create_child_view,
        name="article-add-child",
    ),
    path(
        "articles/<path:parent_path>/add-sibling/",
        views.article_create_sibling_view,
        name="article-add-sibling",
    ),
    path("articles/add-root/", views.article_create_root_view, name="article-add-root"),
    path("articles/", views.article_list_view, name="articles"),
    path("toc/<slug_full>/", views.table_of_contents_retrieve_view, name="toc"),
    path(
        "articles/<path:slug_full>/",
        views.article_retrieve_update_destroy_view,
        name="article",
    ),
    path(
        "articles/<path:slug_full>/annotations/",
        views.annotation_list_create_view,
        name="annotations",
    ),
    path(
        "annotations/<uuid>/",
        views.annotation_retrieve_update_destroy_view,
        name="annotation",
    ),
    path("comments/", views.comment_create_view, name="comments"),
    path(
        "comments/<uuid>/", views.comment_retrieve_update_destroy_view, name="comment"
    ),
    path("bookmarks/", views.bookmark_create_view, name="bookmarks"),
    path(
        "bookmark/<path:book>/",
        views.bookmark_retrieve_update_view,
        name="bookmark",
    ),
]
