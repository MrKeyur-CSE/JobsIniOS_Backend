from django.contrib import admin
from .models import CustomUser

# Register your models here.


class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'full_name', 'phone_number', 'address')
    readonly_fields = ('password', )


admin.site.register(CustomUser, CustomUserAdmin)
