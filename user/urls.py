from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    path('', views.profile, name='profile'),
    path('profile/<int:pk>', views.profile_detail, name='profile-detail'),
    path('account/', views.userAccounts, name='account'),
    path('edit-account/', views.editAccount, name='edit-account'),
    path('add-skill/', views.addSkill, name='add-skill'),\
    path('edit-skill/<int:pk>', views.updateSkill, name='edit-skill'),
    path('delete-skill/<int:pk>', views.delete_skill, name='delete-skill'),

    path('inbox/', views.inbox, name='inbox'),
    path('message/<int:pk>', views.viewMessage, name='message-detail'),
    path('create-message/<int:pk>', views.createMessage, name='create-message'),
]
