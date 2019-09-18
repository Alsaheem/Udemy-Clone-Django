from django.urls import path
from blog.views import PostListView,PostDetailView

app_name = 'blogs'

urlpatterns = [

    path("blog/",PostListView.as_view(),name='post_list'),
    path('blog/<int:pk>/',PostDetailView.as_view(),name='post_detail'),


]
