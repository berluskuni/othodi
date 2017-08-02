from django.contrib import admin
from .models import Place, TimeInterval, Date, VGarbage, Routes

# Register your models here.


class PlaceAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'phone', 'email', 'v_garbage', 'date']
    list_display_links = ['email']


class TimeIntervalAdmin(admin.ModelAdmin):
    list_display = ['time_interval', 'display_data', 'ordering', 'viz_30', 'viz_60', 'viz_120']
    list_display_links = ['time_interval']


class VGarbageAdmin(admin.ModelAdmin):
    list_display = ['garbage', 'ordering']
    list_display_links = ['garbage']


class RoutesAdmin(admin.ModelAdmin):
    list_display = ['title', 'ordering', 'route_place']

admin.site.register(VGarbage)
admin.site.register(Date)
admin.site.register(Place, PlaceAdmin)
admin.site.register(TimeInterval, TimeIntervalAdmin)
admin.site.register(Routes)