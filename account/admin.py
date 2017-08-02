# coding: utf8
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from account.forms import CreationFormUser
from account.forms import UserChangeForm
from account.models import User


class UserAdmin(UserAdmin):
    form = UserChangeForm
    add_form = CreationFormUser

    list_display = [
        'first_name',
        'last_name',
        'email',
        'phone',
        'vin_number',
        'esn_number',


    ]
    list_filter = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {
            'fields': (
                'avatar',
                'first_name',
                'last_name',
                'phone',
                'esn_number',
                'vin_number',


            )}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password',
            )
        }),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()

admin.site.register(User, UserAdmin)
