from django.contrib import admin
from .models import Profile


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'email', 'city', 'phone_number', 'date_joined')
    search_fields = ('user__username', 'first_name', 'last_name', 'email', 'city', 'phone_number')
    readonly_fields = ('date_joined',)
