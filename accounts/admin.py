from django.contrib import admin
from .models import User

class UserView(admin.ModelAdmin):
    list_display = [
        'id',
        'username',
        'email',
        'first_name',
        'last_name',
        'is_staff',
        'is_superuser'
    ]
    class Meta:
        model = User
admin.site.register(User, UserView)