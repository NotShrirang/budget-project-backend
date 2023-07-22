from rest_framework.views import APIView
from rest_framework.response import Response

class HomeView(APIView):
    def get(self, request, format=None):
        return Response({"message": "Budget Form Application API"})