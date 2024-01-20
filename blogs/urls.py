from django.urls import path
from .views import base_page, blog_page, edit_blog


urlpatterns = [
    path("", base_page, name="base_page"),
    path("blog/id=<int:blog_id>", blog_page, name="blog_page"),
    path("blog/edit/id=<int:blog_id>", edit_blog, name="edit_blog"),
]
