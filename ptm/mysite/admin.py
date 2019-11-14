from django.contrib import admin

# Register your models here.

from .models import *

class attendenceAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent','classname','drop_time','pick_up_time')


admin.site.register(profileModel)
admin.site.register(child)
admin.site.register(attendence,attendenceAdmin)
admin.site.register(Notifications)
admin.site.register(child_stories)
admin.site.register(Leaves)
admin.site.register(Class)


