from api.models import (
    Department,
    CollegeUser,
    Activity,
    Transaction,
    Notification,
)
from rest_framework import serializers


class CollegeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeUser
        fields = '__all__'


class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Department
        fields = '__all__'


class ActivitySerializer(serializers.ModelSerializer):
    departmentName = serializers.SerializerMethodField()

    class Meta:
        model = Activity
        fields = ['id', 'name', 'department', 'departmentName', 'available_amount', 'total_amount', 'isActive']

    def get_departmentName(self, obj):
        return obj.department.name


class TransactionSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    userEmail = serializers.SerializerMethodField()
    activityName = serializers.SerializerMethodField()
    departmentName = serializers.SerializerMethodField()

    class Meta:
        model = Transaction
        fields = ['id', 'title', 'description', 'activity', 'user', 'username', 'userEmail', 'item', 'requested_amount', 'approved_amount', 'file', 'status', 'note', 'request_date', 'is_read_date', 'approved_date', 'rejected_date', 'is_read', 'activityName', 'departmentName']

    def get_username(self, obj):
        return obj.user.username

    def get_userEmail(self, obj):
        return obj.user.email

    def get_activityName(self, obj):
        return obj.activity.name

    def get_departmentName(self, obj):
        return obj.activity.department.name


class NotificationSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    userEmail = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'title', 'description', 'activity', 'user', 'username', 'userEmail', 'item', 'requested_amount', 'approved_amount', 'file', 'status', 'note', 'request_date', 'is_read_date', 'approved_date', 'rejected_date', 'is_read']

    def get_username(self, obj):
        return obj.user.username

    def get_userEmail(self, obj):
        return obj.user.email
