# Generated by Django 3.2.6 on 2021-09-09 11:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_auto_20210901_1228'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'ordering': ['-id'], 'verbose_name_plural': 'Manage Projects'},
        ),
    ]
