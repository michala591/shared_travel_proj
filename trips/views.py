from datetime import timezone
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cars.models import Car
from users.models import User
from users.permissions import IsDriverUser
from .serializers import (
    SearchTripsSerializer,
    UserSerializer,
    tripsSerializer,
)
from .models import FrozenPassenger, Trips


@api_view(["GET"])
def get_trips(request):
    if request.method == "GET":
        trips = Trips.objects.all()
        serializer = tripsSerializer(trips, many=True)
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([IsAuthenticated, IsDriverUser])
def add_trips(request):
    try:
        car = Car.objects.filter(user=request.user).first()
        car_id = car.id
        if not car:
            return Response(
                {"error": "No car found for the user."},
                status=status.HTTP_400_BAD_REQUEST,
            )
        trip = Trips.objects.create(
            car_id=car_id,
            days=request.data["days"],
            departure_time=request.data["departure_time"],
            return_time=request.data["return_time"],
            origin_station_id=request.data["origin_station"],
            destination_station_id=request.data["destination_station"],
        )
        trip.users.add(request.user)

        if "users" in request.data:
            trip.users.set(request.data["users"])
        trip.save()

        return Response(
            {"message": "Trip added successfully."},
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsDriverUser])
def trip_detail(request, id):
    trip = get_object_or_404(Trips, id=id)

    if trip.car.user != request.user:
        return Response(
            {"error": "You can only access your own trips."},
            status=status.HTTP_403_FORBIDDEN,
        )
    if request.method == "GET":
        serializer = tripsSerializer(trip)
        return Response(serializer.data)

    if request.method == "PUT":
        try:
            car = Car.objects.filter(user=request.user).first()
            car_id = car.id
            if not car:
                return Response(
                    {"error": "No car found for the user."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            trip.days = request.data.get("days", trip.days)
            trip.departure_time = request.data.get(
                "departure_time", trip.departure_time
            )
            trip.return_time = request.data.get("return_time", trip.return_time)
            trip.origin_station_id = request.data.get(
                "origin_station", trip.origin_station_id
            )
            trip.destination_station_id = request.data.get(
                "destination_station", trip.destination_station_id
            )
            trip.car_id = car_id  # Ensure the car remains assigned to the trip

            if "users" in request.data:
                trip.users.set(request.data["users"])
            trip.save()

            return Response(
                {"message": "Trip update successfully."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        trip.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
@permission_classes([IsAuthenticated, IsDriverUser])
def get_passengers(request, id):
    trip = get_object_or_404(Trips, id=id)
    passengers = trip.users.all()
    serializer = UserSerializer(passengers, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def get_active_trips(request):
    if request.method == "GET":
        trips = Trips.objects.filter(users__user_type="DR", users__is_enabled=True)
        serializer = tripsSerializer(trips, many=True)
        return Response(serializer.data)


# @api_view(["GET"])
# def search_trips(request):
#     letter = request.query_params.get("letter", None)

#     if letter:
#         trips = Trips.objects.filter(
#             origin_station__city__startswith=letter
#         ) | Trips.objects.filter(origin_station__zone__startswith=letter)

#         trips = [trip for trip in trips if trip.has_available_seats()]

#         serializer = SearchTripsSerializer(trips, many=True)
#         return Response(serializer.data)

#     return Response(
#         {"detail": "Letter parameter is required."}, status=status.HTTP_400_BAD_REQUEST
#     )


@api_view(["GET"])
def search_trips(request):
    letter = request.query_params.get("letter", None)
    if letter:
        trips = Trips.objects.filter(
            origin_station__city__istartswith=letter
        ) | Trips.objects.filter(origin_station__zone__istartswith=letter)
        trips = [trip for trip in trips if trip.available_seats()]
        serializer = SearchTripsSerializer(trips, many=True)
        return Response(serializer.data)
    return Response(
        {"detail": "Letter parameter is required."}, status=status.HTTP_400_BAD_REQUEST
    )


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def invite_to_trip(request, id):
    trip = get_object_or_404(Trips, id=id)

    if request.user in trip.users.all():
        return Response(
            {"error": "You are already part of this trip."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    if (
        Trips.objects.filter(users=request.user).exists()
        and request.user.user_type == "PA"
    ):
        return Response(
            {"error": "You are already part of trips."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if trip.available_seats() == 0:
        return Response(
            {"error": "No available seats on this trip."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    trip.users.add(request.user)
    return Response(
        {
            "status": f"You have been successfully added to the trip from {trip.origin_station} to {trip.destination_station}.",
            "available_seats": trip.available_seats(),  # Fixed to return as integer
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def my_trips(request):
    trips = Trips.objects.filter(users=request.user)
    serializer = tripsSerializer(trips, many=True)
    return Response(serializer.data)


from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Trips


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_trip(request, trip_id):
    try:
        # Fetch the specific trip by ID
        trip = Trips.objects.get(id=trip_id)

        # Check if the requesting user is part of the trip
        if request.user not in trip.users.all():
            return Response(
                {"detail": "You are not part of this trip."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Remove the user from the trip
        trip.users.remove(request.user)

        return Response(
            {"detail": "Trip successfully deleted from your list."},
            status=status.HTTP_204_NO_CONTENT,
        )

    except Trips.DoesNotExist:
        return Response({"detail": "Trip not found."}, status=status.HTTP_404_NOT_FOUND)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def freeze_passenger(request, id):
    trip = get_object_or_404(Trips, id=id)

    # Check if the user is part of the trip
    if request.user not in trip.users.all():
        return Response(
            {"error": "You are not part of this trip."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Freeze the user for one day
    freeze_until = timezone.now() + timezone.timedelta(days=1)

    # Create a record in FrozenPassenger
    FrozenPassenger.objects.create(
        trip=trip, user=request.user, freeze_until=freeze_until
    )

    return Response(
        {
            "status": f"{request.user} has been frozen for 1 day on the trip from {trip.origin_station} to {trip.destination_station}.",
            "freeze_until": freeze_until,
        },
        status=status.HTTP_200_OK,
    )
