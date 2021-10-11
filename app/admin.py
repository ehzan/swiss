from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.Player)
admin.site.register(models.Sport)
admin.site.register(models.Tournament)
admin.site.register(models.Participant)
admin.site.register(models.Match)
