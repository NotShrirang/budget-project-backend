from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.views import APIView
from rest_framework.response import Response
from api.views import (
    CollegeUserViewSet,
    DepartmentViewSet,
    ActivityViewSet,
    TransactionViewSet,
    CollegeUserLoginView,
    CollegeUserRegisterView,
    CollegeUserLogoutView,
    UpdateTransactionStatusView,
    UpdateTransactionReadStatusView,
    GetRequestCountView,
)

router = DefaultRouter()
router.register(r'college-users', CollegeUserViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'activities', ActivityViewSet)
router.register(r'transactions', TransactionViewSet)

class HomeView(APIView):
    def get(self, request):
        return Response({
            'message': 'Welcome to College API',
            'endpoints': [
                '/login/',
                '/register/',
                '/logout/',
                '/college-users/',
                '/departments/',
                '/activities/',
                '/transactions/',
                '/request-count/',
                '/update-status-transactions/<int:pk>/',
                '/update-read-status-transactions/<int:pk>/',
            ]
        })

urlpatterns = [
    path('', HomeView.as_view(), name="home"),
    path('request-count/', GetRequestCountView.as_view(), name='request-count'),
    path('update-status-transactions/<str:pk>/', UpdateTransactionStatusView.as_view(), name='update-transaction-status'),
    path('update-read-status-transactions/<str:pk>/', UpdateTransactionReadStatusView.as_view(), name='update-transaction-read-status'),
    path('login/', CollegeUserLoginView.as_view(), name="login"),
    path('register/', CollegeUserRegisterView.as_view(), name="register"),
    path('logout/', CollegeUserLogoutView.as_view(), name="logout"),
] + router.urls