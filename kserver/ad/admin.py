# Register your models here.
from django.contrib import admin
from .models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    list_display_links = ["name", ]
    search_fields = ["name", ]

    class Meta:
        Product = Product
admin.site.register(Product, ProductAdmin)


class ModelAdmin(admin.ModelAdmin):
    list_display = ["name",]
    list_display_links = ["name",]
    search_fields = ["name","voltage","current",]

    class Meta:
        Model = Model
admin.site.register(Model, ModelAdmin)


class ScriptAdmin(admin.ModelAdmin):
    list_display = ["name",]
    list_display_links = ["name",]
    search_fields = ["name",]

    class Meta:
        Script = Script
admin.site.register(Script, ScriptAdmin)


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ["name",]
    list_display_links = ["name",]
    search_fields = ["name",]

    class Meta:
        Instrument = Instrument
admin.site.register(Instrument, InstrumentAdmin)

class StationAdmin(admin.ModelAdmin):
    list_display = ["name",]
    list_display_links = ["name",]
    search_fields = ["name",]

    class Meta:
        Station = Station
admin.site.register(Station, StationAdmin)


class CardAdmin(admin.ModelAdmin):
    list_display = ["serialNumber",]
    list_display_links = ["serialNumber",]
    search_fields = ["serialNumber",]

    class Meta:
        Card = Card
admin.site.register(Card, CardAdmin)