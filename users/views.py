from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from .serializers import userSerializer, LoginUserSerializer
from .models import User


@api_view(["GET", "POST"])
@permission_classes([IsAdminUser])
def get_users(request):
    if request.method == "GET":
        users = User.objects.all()
        serializer = userSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = userSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
@permission_classes([IsAuthenticated, IsAdminUser])
def user_detail(request, id):
    user = get_object_or_404(User, id=id)

    if request.method == "GET":
        serializer = userSerializer(user)
        return Response(serializer.data)

    elif request.method == "PUT":
        serializer = userSerializer(user, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        user.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["POST"])
def register(request):
    try:
        user = User.objects.create_user(
            username=request.data["username"],
            email=request.data["email"],
            password=request.data["password"],
            user_type=request.data["user_type"],
            name=request.data["name"],
            phone_number=request.data.get("phone_number", ""),  # Optional phone number
        )
        user.is_enabled = True
        user.save()
        return Response(
            {"message": "New user created successfully."},
            status=status.HTTP_201_CREATED,
        )
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(["POST"])
def login(request):
    username = request.data.get("username")
    password = request.data.get("password")

    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        return Response({"access": access_token}, status=status.HTTP_200_OK)

    return Response(
        {"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])  # Ensure user is authenticated
def get_user_info(request):
    user = request.user  # Get the authenticated user
    serializer = LoginUserSerializer(user)
    return Response(serializer.data)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def active_passengers(request):
    user = request.user
    if user:
        if user.is_enabled == True:
            user.is_enabled = not user.is_enabled
            user.save()
            return Response(
                {
                    "status": f"{user.username} active status updated to {user.is_enabled}"
                },
            )
        else:
            user.is_enabled = not user.is_enabled
            user.save()
            return Response(
                {
                    "status": f"{user.username} active status updated to {user.is_enabled}"
                },
            )
    else:
        return Response(
            {"error": "User not part of this trip"},
            status=status.HTTP_404_NOT_FOUND,
        )
