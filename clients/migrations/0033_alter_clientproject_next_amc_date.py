# Generated by Django 3.2.6 on 2021-09-14 09:28

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0032_alter_clientproject_next_amc_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='clientproject',
            name='next_amc_date',
            field=models.DateField(default=datetime.datetime(2022, 9, 14, 9, 28, 38, 734694, tzinfo=utc)),
        ),
    ]
