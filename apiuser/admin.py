from django.contrib import admin
from .models import ApiUser, ApiKey
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User

# Register your models here.

class ApiKeyInLine(admin.StackedInline):
    model = ApiKey
    readonly_fields = ("created", "last_accessed", "last_accessed_ip", "api_secret")
    min_num = 1
    extra = 0


class ApiUserAdmin(BaseUserAdmin):
    inlines = (ApiKeyInLine,)


# admin.site.unregister(User)
admin.site.register(ApiUser, ApiUserAdmin)