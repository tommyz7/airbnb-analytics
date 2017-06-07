from __future__ import absolute_import, unicode_literals
from celery import shared_task
from .airbnb_api import AirbnbAPI
from .airbnb_api import settings
from .models import Location, Apartment


@shared_task
def update_listings_for_city(city=None):
    airbnb = AirbnbAPI(settings.get_env_variable('AIRBNB_API_KEY'))
    username = settings.get_env_variable('AIRBNB_USERNAME')
    password = settings.get_env_variable('AIRBNB_PASSWORD')
    airbnb.login_by_email(username, password)
    locations = []
    for location in Location.query.all():
        response = airbnb_api.listing_search(location=location.name)).json()
        Apartment()


    return city

@shared_task
def update_listing_info_daily(listing_id=None):
    # call airbnb API
    # use selenium or scrapy to grab vacancy
    return listing_id
