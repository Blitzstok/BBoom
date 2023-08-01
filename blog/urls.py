from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.mainmenu),
    path(
        'blog/',
        login_required(views.Blog.as_view()),
        name='blog'),
    path(
        'blog/add',
        login_required(views.AddPost.as_view()),
        name='addpost'),
    path(
        'blog/<int:pk>',
        login_required(views.DeletePost.as_view()),
        name='delpost'),

    path('users/', views.UserList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('posts/', views.PostList.as_view()),
    path('postsbyuser/<int:pk>', views.PostList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
