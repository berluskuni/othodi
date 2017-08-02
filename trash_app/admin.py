from django.contrib import admin
from .models import Place, TimeInterval, Date, VGarbage

# Register your models here.


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'v_garbage', 'date']
    list_display_links = ['email']


class TimeIntervalAdmin(admin.ModelAdmin):
    list_display = ['time_interval', 'display_data', 'ordering']
    list_display_links = ['time_interval']


class VGarbageAdmin(admin.ModelAdmin):
    list_display = ['garbage', 'ordering']
    list_display_links = ['garbage']

admin.site.register(VGarbage)
admin.site.register(Date)
admin.site.register(Place, PlaceAdmin)
admin.site.register(TimeInterval, TimeIntervalAdmin)