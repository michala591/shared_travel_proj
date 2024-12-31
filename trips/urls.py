from django.urls import path
from . import views

urlpatterns = [
    path("", views.get_trips, name="trip"),
    path("add_trips/", views.add_trips, name="add_trips"),
    path("active_trips/", views.get_active_trips, name="get_active_trips"),
    path("<int:id>/", views.trip_detail, name="trip_detail"),
    path("<int:id>/passengers/", views.get_passengers, name="get_passengers"),
    path("<int:id>/invite/", views.invite_to_trip, name="invite_to_trip"),
    path("search/", views.search_trips, name="search_trips"),
    path("my_trips/", views.my_trips, name="my_trips"),
    path("delete_trip/<int:trip_id>/", views.delete_trip, name="delete_trip"),
    path("freeze_passenger/", views.freeze_passenger, name="freeze_passenger"),
]
