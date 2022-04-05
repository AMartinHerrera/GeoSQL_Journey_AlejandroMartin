from django.contrib import admin
from .models import WorldBorder, Stops, QuartiersCada

# Register your models here.

# class WorldBorderAdmin(admin.ModelAdmin):
#     list_display = ('name')

admin.site.register(WorldBorder)
admin.site.register(Stops)
admin.site.register(QuartiersCada)