from __future__ import absolute_import, unicode_literals
from celery import shared_task


@shared_task
def update_listings_for_city(city=None):
    return city

@shared_task
def update_listing_info_daily(listing_id=None):
    # call airbnb API
    # use selenium or scrapy to grab vacancy
    return listing_id
