# Generated by Django 3.2.6 on 2021-08-25 07:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0009_remove_supportactivity_files'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportactivity',
            name='files',
            field=models.FileField(default=1, upload_to='documents/'),
            preserve_default=False,
        ),
    ]
