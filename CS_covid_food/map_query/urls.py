from django.urls import path
from django.conf.urls import include, url
from .views import *

urlpatterns= [
    path('', search_query, name='search_q'),
    url(r'^$', HomePageView.as_view(),  name='home'),
    url(r'^fodbank_data/$', fb_datasets, name='foodbank'),
    url(r'^covid_food/$', covid_food_datasets, name='covid_food'),
]