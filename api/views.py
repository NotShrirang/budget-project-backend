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
    TransactionSerializer,
    RegisterSerializer,
    LoginSerializer,
    LogoutSerializer
)
from rest_framework import generics, permissions
from rest_framework.parsers import JSONParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from datetime import datetime
from django import db
from django.db.models import Q

class CollegeUserRegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self,request):
        user=request.data
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_id = CollegeUser.objects.get(email=user['email']).id
        user_data = serializer.data
        user_data['id'] = user_id
        return Response(user_data, status=status.HTTP_201_CREATED)

class CollegeUserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    def post(self,request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class CollegeUserLogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)

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
            transactions = Transaction.objects.filter(Q(user=current_user) | Q(user__department=current_user.department))
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
        
    def create(self, request, *args, **kwargs):
        current_user = CollegeUser.objects.get(id=request.user.id)
        activity = Activity.objects.get(id=request.data['activity'])
        if activity.available_amount >= request.data['requested_amount']:
            data = request.data
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
            transaction.delete()
            return Response({'status': 'success', 'data': 'Transaction deleted successfully'})
        else:
            return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})


class UpdateTransactionStatusView(APIView):
    def post(self, request, primary_key):
        with db.transaction.atomic():
            transaction = Transaction.objects.get(id=primary_key)
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
                    return Response({'status': 'failed', 'message': 'Transaction has been rejected'})
            else:
                return Response({'status': 'failed', 'message': 'You are not authorized to perform this action'})

class UpdateTransactionReadStatusView(APIView):
    def post(self, request, primary_key):
        transaction = Transaction.objects.get(id=primary_key)
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