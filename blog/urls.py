from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.mainmenu),
    path(
        'blog/',
        login_required(views.Blog.as_view()),
        name='blog'
    ),
    path(
        'blog/add',
        login_required(views.AddPost.as_view()),
        name='addpost'
    ),
    path(
        'blog/<int:pk>',
        login_required(views.DeletePost.as_view()),
        name='delpost'
    ),
    path(
        'usertable/',
        login_required(views.UserTable.as_view()),
        name='usertab'
    ),
    path(
        'user/<int:pk>',
        login_required(views.Blog.as_view()),
        name='blog'
    ),

###    API Entries  ###
    path('users/', views.UserList.as_view(), name = 'userlist'),
    path('posts/<int:pk>/', views.PostDetail.as_view(), name = 'getpost'),
    path('postsbyuser/<int:pk>', views.PostList.as_view(), name = 'postsbyuser'),
    path('posts/', views.PostList.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
