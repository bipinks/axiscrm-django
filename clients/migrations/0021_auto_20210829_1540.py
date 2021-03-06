# Generated by Django 3.2.6 on 2021-08-29 11:40

import clients.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0020_client_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientproject',
            name='next_amc_date',
            field=models.DateField(default=clients.models.date_next_year),
        ),
        migrations.AddField(
            model_name='clientproject',
            name='status',
            field=models.CharField(choices=[('0', 'Active'), ('1', 'Due For AMC Renewal'), ('2', 'Project setup in progress'), ('3', 'Closed')], default='0', max_length=255),
        ),
    ]
