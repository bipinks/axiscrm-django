# Generated by Django 3.2.6 on 2021-08-21 07:00

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0003_clientprojectdocument'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprojectdocument',
            name='file',
            field=models.CharField(default=django.utils.timezone.now, max_length=255),
            preserve_default=False,
        ),
    ]
