from api.models import (
    CollegeUser,
    Department,
    Activity,
    Transaction
)
from api.serializers import (
    CollegeUserSerializer,
    DepartmentSerializer,
    ActivitySerializer,
    TransactionSerializer
)
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from rest_framework.response import Response

class CollegeUserRegisterView(APIView):
    def post(self, request):
        email = request.data.get('email')
        department = request.data.get('department')
        username = request.data.get('username')
        password = request.data.get('password')
        privilege = request.data.get('privilege')
        is_active = request.data.get('is_active', True)
        is_admin = request.data.get('is_admin', False)
        is_staff = request.data.get('is_staff', False)
        is_superuser = request.data.get('is_superuser', False)
        user = CollegeUser.objects.filter(email=email).first()
        if user:
            return Response({'status': 'failed', 'data': 'Username already exists'})
        else:
            user = CollegeUser.objects.create(
                email=email,
                department=department,
                username=username, 
                privilege=privilege,
                is_active=is_active,
                is_admin=is_admin,
                is_staff=is_staff,
                is_superuser=is_superuser,
                password=password
            )
            return Response({'status': 'success', 'data': CollegeUserSerializer(user).data})

class CollegeUserLoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = CollegeUser.objects.filter(email=email, password=password).first()
        if user:
            return Response({'status': 'success', 'data': CollegeUserSerializer(user).data})
        else:
            return Response({'status': 'failed', 'data': 'Invalid credentials'})

class CollegeUserLogoutView(APIView):
    def post(self, request):
        return Response({'status': 'success', 'data': 'Logged out successfully'})

class CollegeUserViewSet(ModelViewSet):
    queryset = CollegeUser.objects.all()
    serializer_class = CollegeUserSerializer

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer