from django.contrib import admin

from .models import Aircraft, AirPortInfo, Flight

# Register your models here.
admin.site.register(Aircraft)
admin.site.register(AirPortInfo)
admin.site.register(Flight)
