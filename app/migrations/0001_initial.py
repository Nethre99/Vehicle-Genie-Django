# Generated by Django 4.2 on 2023-04-11 11:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='vehicles',
            fields=[
                ('title', models.CharField(max_length=255)),
                ('sub_title', models.CharField(max_length=255)),
                ('price', models.CharField(max_length=255)),
                ('brand', models.CharField(max_length=255)),
                ('model', models.CharField(max_length=255)),
                ('edition', models.CharField(max_length=255)),
                ('year', models.CharField(max_length=255)),
                ('condition', models.CharField(max_length=255)),
                ('transmission', models.CharField(max_length=255)),
                ('body', models.CharField(max_length=255)),
                ('fuel', models.CharField(max_length=255)),
                ('capacity', models.CharField(max_length=255)),
                ('mileage', models.CharField(max_length=255)),
                ('location', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=255)),
                ('post_url', models.CharField(max_length=255)),
                ('seller_name', models.CharField(max_length=255)),
                ('seller_type', models.CharField(max_length=255)),
                ('published_date', models.CharField(max_length=255)),
                ('vehicle_Id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='Vehicle_Id'
                )),
            ],
            options={
                'db_table': 'vehicles',
            },
        ),
        migrations.CreateModel(
            name='user_vehicle',
            fields=[
                ('Client_Id', models.BigIntegerField()),
                ('Vehicle_Id', models.BigIntegerField()),
                ('uv_Id', models.BigAutoField(
                    auto_created=True, primary_key=True, serialize=False, verbose_name='Vehicle_Id'
                )),
            ],
            options={
                'db_table': 'user_vehicle',
            },
        ),
    ]
