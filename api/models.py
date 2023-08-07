from django.db import models
from users.models import CustomUser
from uuid import uuid4

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    available_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'department'

class CollegeUser(CustomUser):
    PRIVILEGE_CHOICES = (
        ('superuser', 'Superuser'),
        ('principal', 'Principal'),
        ('hod', 'HOD'),
        ('employee', 'Employee'),
    )
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, related_name='users')
    privilege = models.CharField(max_length=255, choices=PRIVILEGE_CHOICES, default='employee')
    
    class Meta:
        db_table = 'user'

class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True, related_name='activities')

    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'activity'

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE, blank=True, null=True, related_name='transactions')
    user = models.ForeignKey(CollegeUser, on_delete=models.CASCADE, blank=True, null=True, related_name='transactions')
    item = models.CharField(max_length=255, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    requested_amount = models.IntegerField(default=0)
    approved_amount = models.IntegerField(default=0)
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='requested')
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'transaction'