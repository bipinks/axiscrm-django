# Generated by Django 3.2.6 on 2021-08-25 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0011_auto_20210825_1352'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='logo',
            field=models.FileField(blank=True, null=True, upload_to='media/clients/'),
        ),
    ]