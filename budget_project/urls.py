from django.contrib import admin
from django.urls import path, include
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request, format=None):
        return Response({
            "message": "Budget Form Application Project",
            "admin" : "admin/",
            "api": "api/",
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('admin/', admin.site.urls),
    path('api/', include("api.urls")),
]
