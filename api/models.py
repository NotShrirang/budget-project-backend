from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from uuid import uuid4
from datetime import datetime

class CollegeUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have email address")
        if not username:
            raise ValueError("Users must have username")
        
        user = self.model(
            email = self.normalize_email(email),
            username = username,
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_admin', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, username, password, **extra_fields)

class Department(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    available_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = 'department'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.id is None:
            self.available_amount = self.total_amount
        else:
            if self.total_amount < self.available_amount:
                raise ValueError("Total amount cannot be less than available amount")
        super(Department, self).save(*args, **kwargs)
    

class CollegeUser(AbstractBaseUser, PermissionsMixin):
    PRIVILEGE_CHOICES = (
        (0, 'Superuser'),
        (1, 'Principal'),
        (2, 'HOD'),
        (3, 'Employee'),
    )
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=255, unique=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='users')
    privilege = models.IntegerField(choices=PRIVILEGE_CHOICES, default=3)

    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CollegeUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    class Meta:
        db_table = 'college_user'

class Activity(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    name = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='activities')
    available_amount = models.IntegerField(default=0)
    total_amount = models.IntegerField(default=0)
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = 'activity'

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if self.id is None:
            self.available_amount = self.total_amount
        else:
            if self.total_amount < self.available_amount:
                raise ValueError("Total amount cannot be less than available amount")
        super(Activity, self).save(*args, **kwargs)

class Transaction(models.Model):
    STATUS_CHOICES = (
        ('requested', 'Requested'),
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    def get_datetime():
        return datetime.now()

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    activity = models.ForeignKey(Activity, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='transactions')
    user = models.ForeignKey(CollegeUser, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='transactions')
    item = models.TextField(blank=True, null=True)
    requested_amount = models.IntegerField(default=0)
    approved_amount = models.IntegerField(default=0)
    file = models.FileField(upload_to='transactions/', blank=True, null=True)
    status = models.CharField(max_length=255, choices=STATUS_CHOICES, default='requested')
    note = models.TextField(blank=True, null=True)
    request_date = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    is_read_date = models.DateTimeField(blank=True, null=True)
    approved_date = models.DateTimeField(blank=True, null=True)
    rejected_date = models.DateTimeField(blank=True, null=True)
    is_read = models.BooleanField(default=False)
    isActive = models.BooleanField(default=True)

    class Meta:
        db_table = 'transaction'

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.id is None:
            Notification.objects.create(
                user=CollegeUser.objects.get(privilege=2, department=self.activity.department),
                transaction=self,
                title=f"New transaction request for {self.title}",
                body=f"{self.user.username} has requested ₹{self.requested_amount} for {self.activity.name} activity.",
                type='transaction',
                redirect_url=f"/transactions/{self.id}"
            )
        super(Transaction, self).save(*args, **kwargs)


class Notification(models.Model):
    NOTIFICATION_TYPE_CHOICES = (
        ('transaction', 'Transaction'),
        ('activity', 'Activity'),
        ('department', 'Department'),
    )

    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(CollegeUser, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='notifications')
    transaction = models.ForeignKey(Transaction, on_delete=models.DO_NOTHING, blank=True, null=True, related_name='notifications')
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    redirect_url = models.CharField(max_length=255, blank=True, null=True)
    is_read = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    isActive = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    
    class Meta:
        db_table = 'notification'