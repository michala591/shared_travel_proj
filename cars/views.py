from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from cars.serializers import CarSerializer
from users.permissions import IsDriverUser
from .models import Car


@api_view(["GET", "POST", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsDriverUser])
def car_detail(request):

    if request.method == "GET":
        cars = Car.objects.filter(user=request.user)
        serializer = CarSerializer(cars, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        try:
            car = Car.objects.create(
                license_plate=request.data["license_plate"],
                model=request.data["model"],
                max_capacity=request.data["max_capacity"],
                user=request.user,
            )

            car.save()

            return Response(
                {"message": "Car added successfully."},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "PUT":
        try:
            car = get_object_or_404(Car, user=request.user)
            car.license_plate = request.data.get("license_plate", car.license_plate)
            car.model = request.data.get("model", car.model)
            car.max_capacity = request.data.get("max_capacity", car.max_capacity)
            car.user = request.user
            car.save()

            return Response(
                {"message": "Car added successfully."},
                status=status.HTTP_200_OK,
            )
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        car = get_object_or_404(Car, user=request.user)
        car.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
