# Auto-generated `LayerMapping` dictionary for Counties model
import os
from django.contrib.gis.utils import LayerMapping
from .models import FoodBanks

# Auto-generated `LayerMapping` dictionary for FoodBanks model
foodbanks_mapping = {
    'address': 'address',
    'category': 'category',
    'location_i': 'location_i',
    'name': 'name',
    'zip_code': 'zip_code',
    'lat': 'lat',
    'lon': 'lon',
    'geom': 'POINT',
}

fb_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'data/food_banks.shp'))

def run(verbose=True):
    lm = LayerMapping(FoodBanks, fb_shp, foodbanks_mapping, transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)
