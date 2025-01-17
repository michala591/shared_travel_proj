"""
URL configuration for shared_travel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path
from users.views import CustomTokenObtainPairView

urlpatterns = [
    path("cars/", include("cars.urls")),
    path("locations/", include("locations.urls")),
    path("", include("trips.urls")),
    path("users/", include("users.urls")),
    path("admin/", admin.site.urls),
    path("login/", CustomTokenObtainPairView.as_view(), name="login"),
    path("refresh/", CustomTokenObtainPairView.as_view(), name="refresh"),
]
