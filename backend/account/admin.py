from django.contrib import admin
from .models import User, AdminUser, CustomerUser, Permissions, Roles

# Register your models here.
admin.site.register(User)
admin.site.register(AdminUser)
admin.site.register(CustomerUser)
admin.site.register(Roles)
admin.site.register(Permissions)