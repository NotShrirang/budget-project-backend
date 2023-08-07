from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to College API'
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
]