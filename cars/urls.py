from django.urls import path
from . import views

urlpatterns = [
    path("my_car/", views.car_detail, name="car_detail"),
]
