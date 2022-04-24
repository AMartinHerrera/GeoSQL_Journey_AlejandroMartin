from django.contrib import admin
from .models import WorldBorder, Stops, QuartiersCada, SecteursCada, IlotsCada

# Register your models here.

# class WorldBorderAdmin(admin.ModelAdmin):
#     list_display = ('name')

admin.site.register(WorldBorder)
admin.site.register(Stops)
admin.site.register(QuartiersCada)
admin.site.register(SecteursCada)
admin.site.register(IlotsCada)