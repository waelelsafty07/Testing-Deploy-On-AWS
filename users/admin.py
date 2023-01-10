from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .forms import CustomUserChangeFrom
from .models import Users
# Register your models here.


class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeFrom
    model = Users
    list_display = ['username', 'email',
                    'first_name', 'last_name', 'is_staff', 'bio']
    fieldsets = UserAdmin.fieldsets + (
        ("User's Bio", {'fields': ('bio',)}),
    )


admin.site.register(Users, CustomUserAdmin)
