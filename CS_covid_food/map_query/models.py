from __future__ import unicode_literals
from django.db import models
from django.contrib.gis.db import models
from django.db.models import Manager as GeoManager

# Create your models here.
class CovidFood(models.Model):
    objectid = models.FloatField()
    shape_area = models.FloatField()
    shape_len = models.FloatField()
    zip = models.BigIntegerField()
    fs_ratio = models.FloatField(null=True)
    pr_fs_rati = models.FloatField(null=True, default=0.0)
    death_rate = models.FloatField(null=True)
    geom = models.MultiPolygonField(srid=4326)

    class Meta:
        verbose_name_plural='Covid_Food'

    def __unicode__(self):
        return self.zip


class FoodBanks(models.Model):
    address = models.CharField(max_length=80)
    category = models.CharField(max_length=80, default="Null")
    location_i = models.BigIntegerField(default=1)
    name = models.CharField(max_length=80)
    zip_code = models.BigIntegerField()
    lat = models.FloatField()
    lon = models.FloatField()
    geom = models.PointField(srid=4326)
    class Meta:
        verbose_name_plural='Food Banks'

    def __unicode__(self):
        return self.data_loc_2


