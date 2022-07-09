from django.contrib import admin

from .models import Civilian, Estate, Vassal


@admin.register(Civilian)
class CivilianPage(admin.ModelAdmin):
    pass


@admin.register(Estate)
class EstatePage(admin.ModelAdmin):
    pass


@admin.register(Vassal)
class VassalPage(admin.ModelAdmin):
    pass
