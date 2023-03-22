from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.project, name='projects'),
    path('project/<int:id>/', views.projectDetail, name='projectDetail'),
    path('create/', views.createPost, name='createPost'),
    path('update/<int:postId>', views.updatePost, name='updatePost'),
    path('delete/<int:postId>', views.deletePost, name='deletePost'),
]
