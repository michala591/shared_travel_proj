from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_users, name="user"),
    path("<int:id>/", views.user_detail, name="user_detail"),
    path("register/", views.register, name="register"),
    path("active/", views.active_passengers, name="active_passengers"),
    path("user/", views.get_user_info, name="get_user_info"),
]
