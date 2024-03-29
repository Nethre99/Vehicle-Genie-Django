# Generated by Django 4.2 on 2023-05-02 05:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0003_rename_client_id_uservehicle_client_id_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='uservehicle',
            old_name='Client_id',
            new_name='Client_Id',
        ),
        migrations.AlterField(
            model_name='uservehicle',
            name='Vehicle_Id',
            field=models.BigIntegerField(),
        ),
        migrations.AlterField(
            model_name='vehicles',
            name='vehicle_Id',
            field=models.BigIntegerField(db_column='Vehicle_Id', primary_key=True, serialize=False),
        ),
    ]
