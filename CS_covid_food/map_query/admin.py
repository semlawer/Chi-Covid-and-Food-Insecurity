from django.contrib import admin
from .models import FoodBanks, CovidFood
from leaflet.admin import LeafletGeoAdmin

# Register your models here.

class CovidFoodAdmin(LeafletGeoAdmin):
    # pass
    list_display = ('zip', 'death_rate', 'fs_ratio', 'pr_fs_rati')

class FoodBanksAdmin(LeafletGeoAdmin):
    # pass
    list_display = ('address',)



admin.site.register(FoodBanks, FoodBanksAdmin)
admin.site.register(CovidFood, CovidFoodAdmin)