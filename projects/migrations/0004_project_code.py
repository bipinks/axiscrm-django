# Generated by Django 3.2.6 on 2021-08-28 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_auto_20210826_1537'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='code',
            field=models.CharField(default=0, max_length=255),
            preserve_default=False,
        ),
    ]