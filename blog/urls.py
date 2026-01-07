from django.urls import path

from blog.views import IndexView, PostView, index


urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("post/<int:pk>", PostView.as_view(), name="post-detail"),
]

app_name = "blog"
