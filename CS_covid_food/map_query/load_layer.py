# Auto-generated `LayerMapping` dictionary for Counties model
import os
from django.contrib.gis.utils import LayerMapping
from .models import CovidFood

# Auto-generated `LayerMapping` dictionary for Zips model
covidfood_mapping = {
    'objectid': 'objectid',
    'shape_area': 'shape_area',
    'shape_len': 'shape_len',
    'zip': 'zip',
    'fs_ratio': 'fs_ratio',
    'pr_fs_rati': 'pr_fs_rati',
    'death_rate': 'death_rate',
    'geom': 'MULTIPOLYGON',
}


covidfood_shp = os.path .abspath(os.path.join(os.path.dirname(__file__), 'data/covid_food.shp'))


def run(verbose=True):
    lm = LayerMapping(CovidFood, covidfood_shp, covidfood_mapping, transform=False, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)