from django.urls import path
from . import views

app_name = "acc"
urlpatterns = [
    path('', views.index, name="index"),
    path('login', views.login_user, name="login_user"),
    path('logout', views.logout_user, name="logout_user"),
    path('regist', views.signup_user, name="signup_user"),
    path('profile', views.profile_user, name="profile_user"),
    path('update', views.update, name="update"),
    path('delete', views.delete, name="delete"),
    path('assign', views.assign),
]
