from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from api.models import (
    CollegeUser,
    Department,
    Transaction,
    Activity,
    Notification,
)

admin.site.site_header = 'Budget Project Admin'


class CollegeUserAdmin(UserAdmin):
    model = CollegeUser
    list_display = (
        'username',
        'email',
        'department',
        'privilege',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    list_filter = (
        'department',
        'privilege',
        'is_active',
        'is_staff',
        'is_superuser',
    )
    search_fields = ('username', 'email')
    ordering = ('email',)

    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Department Info', {'fields': ('department',)}),
        ('Privilege Info', {'fields': ('privilege',)}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'department', 'privilege'),
        }),
    )


class TransactionAdmin(admin.ModelAdmin):
    model = Transaction
    list_display = (
        'title',
        'activity',
        'user',
        'item',
        'requested_amount',
        'approved_amount',
        'status',
        'request_date',
        'is_read_date',
        'approved_date',
        'rejected_date',
        'is_read',
    )
    list_filter = (
        'activity',
        'user',
        'status',
        'is_read',
    )
    search_fields = ('title', 'activity', 'user', 'item')
    ordering = ('request_date',)
    fieldsets = (
        (None, {'fields': ('title', 'activity', 'user', 'item', 'requested_amount', 'approved_amount', 'file', 'status', 'note', 'request_date', 'is_read_date', 'approved_date', 'rejected_date', 'is_read')}),
    )


class ActivityAdmin(admin.ModelAdmin):
    model = Activity
    list_display = (
        'name',
        'department',
        'available_amount',
        'total_amount',
        'isActive',
    )
    list_filter = (
        'department',
        'isActive',
    )
    search_fields = ('name', 'department')
    ordering = ('name',)


class NotificationAdmin(admin.ModelAdmin):
    model = Notification
    list_display = (
        'title',
        'user',
        'type',
        'redirect_url',
        'is_read',
    )
    list_filter = (
        'user',
        'type',
        'is_read',
    )
    search_fields = ('title', 'user', 'type')
    ordering = ('-id',)
    readonly_fields = ('title', 'user', 'type', 'redirect_url', 'is_read')


class DepartmentAdmin(admin.ModelAdmin):
    model = Department
    list_display = (
        'name',
        'available_amount',
        'total_amount',
        'isActive',
    )
    list_filter = (
        'name',
        'available_amount',
        'total_amount',
        'isActive',
    )
    search_fields = ('name',)
    ordering = ('name',)
    readonly_fields = ('name', 'isActive')


admin.site.register(CollegeUser, CollegeUserAdmin)
admin.site.register(Department, DepartmentAdmin)
admin.site.register(Transaction, TransactionAdmin)
admin.site.register(Activity, ActivityAdmin)
admin.site.register(Notification, NotificationAdmin)
