from django.db import models


# Create your models here.
class vehicles(models.Model):
    Title = models.CharField(max_length=200, null=True, blank=False)
    Sub_title = models.CharField(max_length=500, null=True, blank=False)
    Price = models.CharField(max_length=20, null=True, blank=False)
    Brand = models.CharField(max_length=100, null=True, blank=False)
    Model = models.CharField(max_length=100, null=True, blank=False)
    Edition = models.CharField(max_length=255, null=True)
    Year = models.CharField(max_length=4, null=True, blank=False)
    Condition = models.CharField(max_length=100, null=True, blank=False)
    Transmission = models.CharField(max_length=100, null=True, blank=False)
    Body = models.CharField(max_length=255, null=True, blank=False)
    Fuel = models.CharField(max_length=255, null=True, blank=False)
    Capacity = models.CharField(max_length=255, null=True, blank=False)
    Mileage = models.CharField(max_length=255, null=True)
    Location = models.CharField(max_length=255, null=True, blank=False)
    Description = models.TextField(null=True)
    Post_url = models.CharField(max_length=500, null=True)
    Seller_name = models.CharField(max_length=255, null=True, blank=False)
    Seller_type = models.CharField(max_length=255, null=True)
    Published_date = models.CharField(max_length=255, null=True)
    Vehicle_Id = models.BigIntegerField(primary_key=True, db_column='Vehicle_Id')

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
