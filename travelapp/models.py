from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


# Create your models here.


class City(models.Model):
    city = models.CharField(max_length=200)
    bestlink = models.CharField(max_length=200)
    weekgetlinks = models.CharField(max_length=200)

    def __srt__(self):
        return self.city


class Flights(models.Model):
    id = models.AutoField(primary_key=True)
    source = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    flight_number = models.CharField(max_length=10)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    eprice = models.IntegerField(null=True)
    dept_time = models.TimeField(auto_now=False, auto_now_add=False)
    dest_time = models.TimeField(auto_now=False, auto_now_add=False)
    company = models.CharField(max_length=15, default=" ")
    seats = models.IntegerField()
    separately_booked = models.BooleanField(default=False)

    def __str__(self):
        return self.flight_number


class Hotels(models.Model):
    id = models.AutoField(primary_key=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=200)
    hotel_address = models.CharField(max_length=500)
    hotel_price = models.IntegerField(null=True)
    hotel_rating = models.IntegerField(null=True)
    amenities = models.CharField(max_length=500)  # удобства
    dist_from_airport = models.IntegerField(null=True)
    rooms = models.IntegerField(default=0)
    image1 = models.ImageField(null=True, upload_to='img/')
    separately_booked = models.BooleanField(default=False)
    description = models.TextField(default='Fill in this field')

    def __str__(self):
        return self.hotel_name


class Famous(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    place_name = models.CharField(max_length=200)
    image = models.ImageField(null=True, upload_to='img/')
    desc = models.CharField(max_length=2000)  # описание

    def __str__(self):
        return self.place_name


class BookFlight(models.Model):
    username_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.CharField(max_length=10)
    date = models.CharField(max_length=20)
    seat = models.IntegerField(default=1)


    def __str__(self):
        return self.date


class BookHotel(models.Model):
    username_id = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel_name = models.CharField(max_length=100)
    date = models.CharField(max_length=20)
    room = models.IntegerField(default=1)

    def __str__(self):
        return self.date


class BookPackage(models.Model):
    username_id = models.ForeignKey(User, on_delete=models.CASCADE)
    flight = models.CharField(max_length=10)
    date = models.CharField(max_length=20)
    seat = models.IntegerField(default=1)
    hotel_name = models.CharField(max_length=100)
    room = models.IntegerField(default=1)


    def __str__(self):
        return self.date


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255, default='none')
    hotel = models.ForeignKey(Hotels, related_name="reviews", on_delete=models.CASCADE)
    text = models.TextField()
    created_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_date']

    def __str__(self):
        return f'{self.hotel.hotel_name} - {self.user}'


