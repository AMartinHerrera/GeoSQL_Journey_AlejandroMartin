
# This is a file in which you can register your models so you have them in django administration site.

from django.contrib import admin
from .models import WorldBorder, Stops, QuartiersCada, SecteursCada, IlotsCada

admin.site.register(WorldBorder)
admin.site.register(Stops)
admin.site.register(QuartiersCada)
admin.site.register(SecteursCada)
admin.site.register(IlotsCada)