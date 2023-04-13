# Generated by Django 4.2 on 2023-04-11 19:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='Body',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Brand',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Capacity',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Condition',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Description',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Edition',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Fuel',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Location',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Mileage',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Model',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Post_url',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Price',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Published_date',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Seller_name',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Seller_type',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Sub_title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Title',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Transmission',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Vehicle_Id',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='Year',
            field=models.CharField(max_length=255),
        ),
    ]