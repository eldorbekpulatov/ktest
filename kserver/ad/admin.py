# Register your models here.
from django.contrib import admin
from ad.models import *

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = ["name", ]
    list_display_links = ["name", ]
    search_fields = ["name", ]

    class Meta:
        Product = Product
admin.site.register(Product, ProductAdmin)


class ModelAdmin(admin.ModelAdmin):
    list_display = ['name','product','voltage','current',]
    list_display_links = ['name','product','voltage','current',]
    search_fields = ['name','product__name','voltage','current',]
    autocomplete_fields = ["product"]

    class Meta:
        Model = Model
admin.site.register(Model, ModelAdmin)


class ScriptAdmin(admin.ModelAdmin):
    list_display = ['name','file','dvm','osc','rctrl','actrl','eload']
    list_display_links = ['name','file','dvm','osc','rctrl','actrl','eload']
    search_fields = ['name','file']
    autocomplete_fields = []

    class Meta:
        Script = Script
admin.site.register(Script, ScriptAdmin)


class StationAdmin(admin.ModelAdmin):
    list_display = ["name",]
    list_display_links = ["name",]
    search_fields = ["name",]

    class Meta:
        Station = Station
admin.site.register(Station, StationAdmin)


class InstrumentAdmin(admin.ModelAdmin):
    list_display = ['name','type','station','serialNumber','kepcoNumber','calibrationDate','expirationDate']
    list_display_links = ['name','type','station','serialNumber','kepcoNumber','calibrationDate','expirationDate']
    search_fields = ['name','type','station__name','serialNumber','kepcoNumber','calibrationDate','expirationDate']
    autocomplete_fields = ["station"]

    class Meta:
        Instrument = Instrument
admin.site.register(Instrument, InstrumentAdmin)


class CardAdmin(admin.ModelAdmin):
    list_display = ['serial','user','station','product','model']
    list_display_links = ['serial','user','station','product','model']
    search_fields = ['serial', 'user__first_name', 'user__last_name', 'station__name', 'product__name', 'model__name']
    autocomplete_fields = ['user', 'station', 'product', 'model']
    
    class Meta:
        Card = Card
admin.site.register(Card, CardAdmin)


class LogAdmin(admin.ModelAdmin):
    list_display = ['card','script','file','status',]
    list_display_links = ['card','script','file','status',]
    search_fields = ['card__serial','script__name', 'file', 'status']
    autocomplete_fields = ['card','script'] # must be foreign key or many-to-many

    class Meta:
        Log = Log
admin.site.register(Log, LogAdmin)