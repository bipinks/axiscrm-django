# Generated by Django 3.2.6 on 2021-09-08 12:04

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('amc', '0003_auto_20210908_1600'),
    ]

    operations = [
        migrations.AddField(
            model_name='amcrenewal',
            name='renewed_date',
            field=models.DateField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]