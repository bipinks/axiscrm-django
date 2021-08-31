# Generated by Django 3.2.6 on 2021-08-31 11:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0021_auto_20210829_1540'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supportrequest',
            name='status',
            field=models.CharField(choices=[('0', 'Pending'), ('1', 'Open'), ('2', 'Awaiting Business Inputs'), ('3', 'With Client Review'), ('4', 'Closed|Resolved'), ('5', 'Deferred')], default='0', max_length=255),
        ),
    ]
