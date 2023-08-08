from django.contrib import admin
from api.models import (
    CollegeUser,
    Department,
    Transaction,
    Activity,
)

admin.site.site_header = 'Budget Project Admin'

admin.site.register(CollegeUser)
admin.site.register(Department)
admin.site.register(Transaction)
admin.site.register(Activity)