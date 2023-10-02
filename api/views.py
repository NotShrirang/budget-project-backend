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
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from django import db

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
            return Response({'status': 'failed', 'data': 'Invalid credentials'}, status=401)

class CollegeUserLogoutView(APIView):
    def post(self, request):
        return Response({'status': 'success', 'data': 'Logged out successfully'})

class CollegeUserViewSet(ModelViewSet):
    queryset = CollegeUser.objects.all()
    serializer_class = CollegeUserSerializer

    def destroy(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1, 2]:
            user = CollegeUser.objects.get(id=kwargs['pk'])
            user.isActive = False
            user.save()
            return Response({'status': 'success', 'data': 'User deleted successfully'})

class DepartmentViewSet(ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    def retrieve(self, request, pk):
        return super().retrieve(request, pk)
    
    def create(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return super().create(request, *args, **kwargs)
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        
    def update(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return super().update(request, *args, **kwargs)
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
    
    def destroy(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            department = Department.objects.get(id=kwargs['pk'])
            department.isActive = False
            department.save()
            return Response({'status': 'success', 'data': 'Department deleted successfully'})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})

class ActivityViewSet(ModelViewSet):
    queryset = Activity.objects.all()
    serializer_class = ActivitySerializer

    def list(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return super().list(request, *args, **kwargs)
        elif current_user.privilege == 2:
            activities = Activity.objects.filter(department=current_user.department)
            return Response({'status': 'success', 'data': ActivitySerializer(activities, many=True).data})
        elif current_user.privilege == 3:
            activities = Activity.objects.filter(department=current_user.department)
            return Response({'status': 'success', 'data': ActivitySerializer(activities, many=True).data})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        
    def retrieve(self, request, pk):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return super().retrieve(self, request, pk)
        elif current_user.privilege == 2:
            activity = Activity.objects.get(id=pk, department=current_user.department)
            return Response({'status': 'success', 'data': ActivitySerializer(activity).data})
        elif current_user.privilege == 3:
            activity = Activity.objects.get(id=pk)
            if activity.department == current_user.department:
                return Response({'status': 'success', 'data': ActivitySerializer(activity).data})
            else:
                return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        
    def create(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return super().create(request, *args, **kwargs)
        elif current_user.privilege == 2:
            data = request.data
            data['department'] = current_user.department.id
            serializer = ActivitySerializer(data=data)
            if not serializer.is_valid():
                return Response({'status': 'failed', 'message': 'Invalid data', 'errors': serializer.errors})
            serializer.save()
            return Response({'status': 'success', 'message': 'Activity created', 'data': serializer.data})
        elif current_user.privilege == 3:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        
    def update(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return super().update(request, *args, **kwargs)
        elif current_user.privilege == 2:
            activity = Activity.objects.get(id=kwargs['pk'], department=current_user.department)
            activity.name = request.data['name'] if request.data['name'] else activity.name
            activity.total_amount = request.data['total_amount'] if request.data['total_amount'] else activity.total_amount
            activity.save()
            return Response({'status': 'success', 'data': ActivitySerializer(activity).data})
        elif current_user.privilege == 3:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
    
    def destroy(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            activity = Activity.objects.get(id=kwargs['pk'])
            activity.isActive = False
            activity.save()
        elif current_user.privilege == 2:
            activity = Activity.objects.get(id=kwargs['pk'], department=current_user.department)
            activity.isActive = False
            activity.save()
            return Response({'status': 'success', 'data': 'Activity deleted successfully'})
        elif current_user.privilege == 3:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})

class TransactionViewSet(ModelViewSet):
    queryset = Transaction.objects.all().order_by('-request_date')
    serializer_class = TransactionSerializer

    def list(self, request, *args, **kwargs):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return super().list(request, *args, **kwargs)
        elif current_user.privilege == 2:
            transactions = Transaction.objects.filter(user__department=current_user.department).order_by('-request_date')
            return Response({'status': 'success', 'data': TransactionSerializer(transactions, many=True).data})
        elif current_user.privilege == 3:
            transactions = Transaction.objects.filter(user=current_user).order_by('-request_date')
            return Response({'status': 'success', 'data': TransactionSerializer(transactions, many=True).data})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})

    def retrieve(self, request, pk):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            transactions = Transaction.objects.get(id=pk)
            return Response({'status': 'success', 'data': TransactionSerializer(transactions).data})
        elif current_user.privilege == 2:
            transactions = Transaction.objects.get(id=pk)
            if transactions.user.department == current_user.department:
                return Response({'status': 'success', 'data': TransactionSerializer(transactions).data})
            else:
                return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        elif current_user.privilege == 3:
            transactions = Transaction.objects.get(id=pk)
            if transactions.user == current_user:
                return Response({'status': 'success', 'data': TransactionSerializer(transactions).data})
            else:
                return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        
    def create(self, request, *args, **kwargs):
        current_user = CollegeUser.objects.get(id=request.user.id)
        activity = Activity.objects.get(id=request.data['activity'])
        if activity.available_amount >= request.data['requested_amount']:
            data = request.data
            data['status'] = 'pending'
            serializer = TransactionSerializer(data=data)
            if not serializer.is_valid():
                return Response({'status': 'failed', 'message': 'Invalid data', 'errors': serializer.errors})
            serializer.save(user=current_user, status='requested')
            return Response({'status': 'success', 'message': 'Transaction created', 'data': serializer.data})
        else:
            return Response({'status': 'failed', 'message': 'Requested amount exceeds available amount'})

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
    
    def destroy(self, request, *args, **kwargs):
        transaction = Transaction.objects.get(id=kwargs['pk'])
        current_user = CollegeUser.objects.get(id=request.user.id)
        if transaction.is_read:
            return Response({'status': 'failed', 'message': 'You cannot delete a transaction that has been read.'})
        if current_user == transaction.user or current_user.privilege in [0, 1, 2]:
            transaction.isActive = False
            transaction.save()
            return Response({'status': 'success', 'data': 'Transaction deleted successfully'})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})


class UpdateTransactionStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, pk):
        with db.transaction.atomic():
            transaction = Transaction.objects.get(id=pk)
            new_status = JSONParser().parse(request)['status']
            current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
            if current_user.privilege in [0, 1, 2] and transaction.user.department == current_user.department and transaction.status == 'pending':
                if new_status == 'approved':
                    transaction.status = new_status
                    activity = Activity.objects.get(id=transaction.activity.id)
                    if transaction.requested_amount <= activity.available_amount:
                        activity.available_amount -= transaction.requested_amount
                        activity.save()
                        transaction.approved_amount = transaction.requested_amount
                    else:
                        transaction.approved_amount = activity.available_amount
                        activity.available_amount = 0
                        activity.save()
                    transaction.approved_date = datetime.now()
                    # TODO: create transaction file
                    transaction.save()
                    return Response({'status': 'success', 'message': 'Transaction has been approved', 'data': TransactionSerializer(transaction).data})
                elif new_status == 'rejected':
                    transaction.status = 'rejected'
                    transaction.rejected_date = datetime.now()
                    transaction.save()
                    return Response({'status': 'failed', 'message': 'Transaction has been rejected'})
            else:
                return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})

class UpdateTransactionReadStatusView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, pk):
        transaction = Transaction.objects.get(id=pk)
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1, 2] and transaction.user.department == current_user.department and transaction.status == 'requested':
            transaction.is_read = True
            transaction.is_read_date = datetime.now()
            transaction.status = 'pending'
            transaction.save()
            return Response({'status': 'success', 'message': 'Transaction has been read', 'data': TransactionSerializer(transaction).data})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
        

class GetRequestCountView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        current_user: CollegeUser = CollegeUser.objects.get(id=request.user.id)
        if current_user.privilege in [0, 1]:
            return Response({'status': 'success', 'data': 
                             {"total": Transaction.objects.filter(status='requested').count(), 
                              "pending": Transaction.objects.filter(status='pending').count(), 
                              "approved": Transaction.objects.filter(status='approved').count(),
                              "rejected": Transaction.objects.filter(status='rejected').count()}})
        elif current_user.privilege == 2:
            return Response({'status': 'success', 'data': 
                             {"total": Transaction.objects.filter(user__department=current_user.department).count(),
                              "pending": Transaction.objects.filter(user__department=current_user.department, status='pending').count(),
                              "approved": Transaction.objects.filter(user__department=current_user.department, status='approved').count(),
                              "rejected": Transaction.objects.filter(user__department=current_user.department, status='rejected').count()}})
        elif current_user.privilege == 3:
            return Response({'status': 'success', 'data': 
                             {"total": Transaction.objects.filter(user=current_user).count(),
                              "pending": Transaction.objects.filter(user=current_user, status='pending').count(),
                              "approved": Transaction.objects.filter(user=current_user, status='approved').count(),
                              "rejected": Transaction.objects.filter(user=current_user, status='rejected').count()}})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})
