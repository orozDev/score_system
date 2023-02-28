from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from .models import Group, User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'id',
        'phone',
        'get_full_name',
        'email',
        'role',
        'get_online_status',
        'get_avatar',
    )
    list_display_links = ('id', 'phone',)
    search_fields = ('phone', 'first_name', 'last_name', 'email',)
    filter_horizontal = ('groups', 'user_permissions')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    ordering = ('-date_joined',)
    fieldsets = (
        (None, {'fields': (
            'phone',
            'password',
        )}),
        (_('Personal info'), {'fields': (
            'avatar',
            'get_avatar',
            'first_name',
            'last_name',
            'email',
            'group',
            'point',
            'role',
        )}),
        (_('Permissions'), {'fields': (
            'is_active',
            'is_staff',
            'is_superuser',
            'groups',
            'user_permissions',
        )}),
        (_('Important dates'), {'fields': (
            'date_joined',
            'last_login',
            'last_activity',
        )}),
    )
    readonly_fields = (
        'get_full_name',
        #'point',
        'get_avatar',
        'date_joined',
        'last_activity',
        'last_login',
    )
    # autocomplete_fields = (
    #     'address',
    # )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'phone', 
                'email',
                'password1', 
                'password2',
            ),
        }),
    )

    @admin.display(description=_('В сети'), boolean=True)
    def get_online_status(self, user):
        return user.online
    
    @admin.display(description=_('Аватарка'))
    def get_avatar(self, user):
        if user.avatar:
            return mark_safe(
                f'<img src="{user.avatar.url}" alt="{user.get_full_name}" width="100px" />')
        return '-'
    
admin.site.register(Group)
       
# Register your models here.
