from django.urls import path

from . import views

urlpatterns = [
    path('', views.socialmedia_index, name='socialmedia-index'),
    path('register/', views.register_user, name='register-url'),
    path('posts/', views.UserPostsView.as_view(), name='posts'),
    path('myprofile/', views.my_profile_view, name='myprofile'),
    path('profile/<int:pk>', views.profile_view, name='profile'),
    path('profile/<int:pk>/friends', views.friends_view, name='friends'),
    path('posts/liked', views.like_unlike_post, name='liked'),
]
