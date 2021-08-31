# Generated by Django 3.2.6 on 2021-08-26 13:31

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0017_auto_20210826_1534'),
    ]

    operations = [
        migrations.AddField(
            model_name='supportrequest',
            name='title',
            field=models.CharField(default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='supportrequestactivityfiles',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='TicketActivityFiles/'),
        ),
        migrations.CreateModel(
            name='SupportRequestFiles',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(blank=True, default=datetime.datetime.now)),
                ('file', models.FileField(blank=True, null=True, upload_to='TicketFiles/')),
                ('support_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.supportrequest')),
            ],
            options={
                'db_table': 'support_request_files',
            },
        ),
    ]
