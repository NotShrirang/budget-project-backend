from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CollegeUser
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

admin.site.register(CollegeUser, CollegeUserAdmin)
admin.site.register(Department)
admin.site.register(Transaction)
admin.site.register(Activity)
admin.site.register(Notification)