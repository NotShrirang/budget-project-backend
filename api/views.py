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
from rest_framework.parsers import JSONParser

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

    def list(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return super().list(request, *args, **kwargs)
        elif current_user.privilege == 2:
            transactions = Transaction.objects.filter(user=current_user, user__department=current_user.department)
            return Response({'status': 'success', 'data': TransactionSerializer(transactions, many=True).data})
        elif current_user.privilege == 3:
            transactions = Transaction.objects.filter(user=current_user)
            return Response({'status': 'success', 'data': TransactionSerializer(transactions, many=True).data})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})

    def retrieve(self, request, pk):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return super().retrieve(self, request, pk)
        elif current_user.privilege == 2:
            transactions = Transaction.objects.get(id=pk, user=current_user, user__department=current_user.department)
            return Response({'status': 'success', 'data': TransactionSerializer(transactions, many=True).data})
        elif current_user.privilege == 3:
            transactions = Transaction.objects.get(id=pk, user=current_user)
            return Response({'status': 'success', 'data': TransactionSerializer(transactions, many=True).data})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        

    def update(self, request, *args, **kwargs):
        transaction = Transaction.objects.get(id=kwargs['pk'])
        current_user = CollegeUser.objects.get(id=request.user.id)
        if transaction.is_read:
            return Response({'status': 'failed', 'message': 'You cannot edit a transaction that has been read.'})
        if current_user == transaction.user:
            transaction.requested_amount = request.data['requested_amount'] if request.data['requested_amount'] else transaction.requested_amount
            transaction.description = request.data['description'] if request.data['description'] else transaction.description
            transaction.item = request.data['item'] if request.data['item'] else transaction.item
            transaction.save()
            return Response({'status': 'success', 'data': TransactionSerializer(transaction).data})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})

            
        

class UpdateTransactionStatusView(APIView):
    def post(self, request, primary_key):
        transaction = Transaction.objects.get(id=primary_key)
        new_status = JSONParser().parse(request)['status']
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1, 2] and transaction.user.department == current_user.department and transaction.status in ['requested', 'pending']:
            if new_status == 'approved':
                transaction.status = new_status
                transaction.save()
                return Response({'status': 'success', 'data': TransactionSerializer(transaction).data})
            else:
                return Response({'status': 'failed', 'message': 'You can only approve a transaction'})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})