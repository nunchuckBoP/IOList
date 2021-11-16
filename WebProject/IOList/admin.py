from django.contrib import admin

from .models import Customer, Plant, IOList, Chassis, ValveBank, Solenoid, Card, Point, BusDevice

class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name']
admin.site.register(Customer, CustomerAdmin)

class PlantAdmin(admin.ModelAdmin):
    list_display = ['customer', 'short_name', 'street', 'line2', 'city', 'state', 'zip_code']
admin.site.register(Plant, PlantAdmin)

class IOListAdmin(admin.ModelAdmin):
    list_display = ['name', 'plant']
admin.site.register(IOList, IOListAdmin)

class ChassisAdmin(admin.ModelAdmin):
    list_display = ['name', 'io_list', 'address']
admin.site.register(Chassis, ChassisAdmin)

class ValveBankAdmin(admin.ModelAdmin):
    list_display = ['name', 'io_list', 'address']
admin.site.register(ValveBank, ValveBankAdmin)

class SolenoidAdmin(admin.ModelAdmin):
    list_display = ['number', 'bank', 'tag', 'address', 'description_1', 'description_2', 'description_3', 'description_4']
admin.site.register(Solenoid, SolenoidAdmin)

class CardAdmin(admin.ModelAdmin):
    list_display = ['slot', 'rack']
admin.site.register(Card, CardAdmin)

class PointAdmin(admin.ModelAdmin):
    list_display = ['number', 'card', 'tag', 'address', 'description_1', 'description_2', 'description_3', 'description_4']
admin.site.register(Point, PointAdmin)

class BusDeviceAdmin(admin.ModelAdmin):
    list_display = ['io_list', 'address', 'tag', 'description_1', 'description_2', 'description_3', 'description_4']
admin.site.register(BusDevice, BusDeviceAdmin)