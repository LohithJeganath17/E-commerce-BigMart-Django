from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account

# Register your models here.
class Accountadmin(UserAdmin):
    filter_horizontal=()
    list_filter=()
    fieldsets=()

    list_display=('username','email','first_name','last_name','date_joined','is_active')
    list_display_links = ('username','email')
    readonly_fields = ('date_joined','is_active')
    ordering = ('-date_joined',)

admin.site.register(Account,Accountadmin)