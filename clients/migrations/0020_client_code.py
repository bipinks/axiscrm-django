# Generated by Django 3.2.6 on 2021-08-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0019_alter_supportrequest_created_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='client',
            name='code',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]
