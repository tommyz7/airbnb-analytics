from django.db import models


class TimeStampedMixin(models.Model):

    created = models.DateTimeField(auto_now=True)
    modified = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Apartment(TimeStampedMixin):

    # Aitbnb info
    airbnb_id = models.IntegerField(unique=True)
    airbnb_user_id = models.IntegerField()

    # Name and Location
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    zipcode = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    country = models.CharField(max_length=255)
    lat = models.FloatField()
    lng = models.FloatField()

    # Details
    bedrooms = models.FloatField()
    bathrooms = models.FloatField()
    beds = models.FloatField()

    property_type = models.CharField(max_length=255)  # ie. Apartment, Hosue
    # room_type = models.CharField(max_length=255)  # ie. Entire home/apt
    room_type_category = models.CharField(max_length=255)  # ie. entire_home
    square_feet = models.CharField(max_length=255)
    person_capacity = models.IntegerField()

    thumbnail_url = models.CharField(max_length=512)
    description = models.TextField()


    def __str__(self):
        return self.name


class Price(TimeStampedMixin):

    apartment = models.ForeignKey(Apartment,
                                  on_delete=models.CASCADE,
                                  related_name="prices",
                                  unique_for_date="date")
    date = models.DateTimeField()
    vacancy = models.BooleanField()  # True - it's free, False - it's occupied

    native_currency = models.CharField(max_length=255)

    price = models.FloatField()
    weekend_price = models.FloatField()
    weekly_price = models.FloatField()
    monthly_price = models.FloatField()
    price_for_extra_person = models.FloatField()
    cleaning_fee = models.FloatField()
    security_deposit = models.FloatField()

    guests_included = models.IntegerField()  # Guests included in base price

    def __str__(self):
        return self.price
