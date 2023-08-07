from api.models import (
    Department,
    CollegeUser,
    Activity,
    Transaction,
)
from rest_framework import serializers

class CollegeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CollegeUser
        fields = '__all__'