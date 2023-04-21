from django.db import models


# Create your models here.
class vehicles(models.Model):
    title = models.CharField(max_length=200, null=True, blank=False)
    sub_title = models.CharField(max_length=500, null=True, blank=False)
    price = models.CharField(max_length=20, null=True, blank=False)
    brand = models.CharField(max_length=100, null=True, blank=False)
    model = models.CharField(max_length=100, null=True, blank=False)
    edition = models.CharField(max_length=255, null=True)
    year = models.CharField(max_length=4, null=True, blank=False)
    condition = models.CharField(max_length=100, null=True, blank=False)
    transmission = models.CharField(max_length=100, null=True, blank=False)
    body = models.CharField(max_length=255, null=True, blank=False)
    fuel = models.CharField(max_length=255, null=True, blank=False)
    capacity = models.CharField(max_length=255, null=True, blank=False)
    mileage = models.CharField(max_length=255, null=True)
    location = models.CharField(max_length=255, null=True, blank=False)
    description = models.TextField(null=True)
    post_url = models.CharField(max_length=500, null=True)
    seller_name = models.CharField(max_length=255, null=True, blank=False)
    seller_type = models.CharField(max_length=255, null=True)
    published_date = models.CharField(max_length=255, null=True)
    vehicle_Id = models.BigIntegerField(primary_key=True, db_column='Vehicle_Id')

# class Vehicle(models.Model):
#     Title = models.CharField(max_length=200, null=True, blank=False)
#     Sub_title = models.CharField(max_length=500, null=True, blank=False)
#     Price = models.IntegerField(null=True, blank=False)
#     Brand = models.CharField(max_length=100, null=True, blank=False)
#     Model = models.CharField(max_length=100, null=True, blank=False)
#     Edition = models.CharField(max_length=255, null=True)
#     Year = models.IntegerField(null=True, blank=False)
#     Condition = models.CharField(max_length=100, null=True, blank=False)
#     Transmission = models.CharField(max_length=100, null=True, blank=False)
#     Body = models.CharField(max_length=255, null=True, blank=False)
#     Fuel = models.CharField(max_length=255, null=True, blank=False)
#     Capacity = models.CharField(max_length=255, null=True, blank=False)
#     Mileage = models.CharField(max_length=255, null=True)
#     Location = models.CharField(max_length=255, null=True, blank=False)
#     Description = models.TextField(null=True)
#     Post_url = models.CharField(max_length=500, null=True)
#     Seller_name = models.CharField(max_length=255, null=True, blank=False)
#     Seller_type = models.CharField(max_length=255, null=True)
#     Published_date = models.CharField(max_length=255, null=True)
#     Vehicle_Id = models.BigIntegerField(primary_key=True, db_column='Vehicle_Id')

    def __str__(self):
        return self.Title

    class Meta():
        db_table = 'vehicles'


class UserVehicle(models.Model):
    uv_Id = models.BigIntegerField(primary_key=True, db_column='uv_Id')
    Vehicle_Id = models.BigIntegerField()
    Client_Id = models.BigIntegerField()

    def __int__(self):
        return self.uv_Id

    class Meta():
        db_table = 'user_vehicle'
