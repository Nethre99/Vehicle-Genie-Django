# Generated by Django 4.2 on 2023-04-11 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0009_remove_vehicles_post_url_alter_vehicles_body_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vehicles',
            name='Year',
            field=models.IntegerField(),
        ),
    ]
