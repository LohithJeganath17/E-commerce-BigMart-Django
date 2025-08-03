from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,UserProfile
from django.utils.html import format_html

# Register your models here.
class Accountadmin(UserAdmin):
    filter_horizontal=()
    list_filter=()
    fieldsets=()

    list_display=('username','email','first_name','last_name','date_joined','is_active')
    list_display_links = ('username','email')
    readonly_fields = ('date_joined','is_active')
    ordering = ('-date_joined',)

class UserProfileAdmin(admin.ModelAdmin):
    def thumbnail(self, object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.profile_picture.url))
    thumbnail.short_description = 'Profile Picture'
    list_display = ('thumbnail', 'user', 'city', 'state', 'country')

admin.site.register(Account,Accountadmin)
admin.site.register(UserProfile,UserProfileAdmin)