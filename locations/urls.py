from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_locations, name="location"),
    path("location_id/", views.location_id, name="location_id"),
    path("search/?", views.search_locations, name="search_locations"),
]
