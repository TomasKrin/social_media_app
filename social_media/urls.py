from django.urls import path

from . import views

urlpatterns = [
    path('', views.socialmedia_index, name='socialmedia-index'),
    path('register/', views.register_user, name='register-url'),
    path('posts/', views.UserPostsView.as_view(), name='posts'),
]
