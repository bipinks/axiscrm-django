# Generated by Django 3.2.6 on 2021-08-23 07:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0004_clientprojectdocument_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='SupportRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('resolved_at', models.DateTimeField(blank=True, null=True)),
                ('description', models.TextField()),
                ('client_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.clientproject')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'support_requests',
            },
        ),
        migrations.CreateModel(
            name='SupportActivity',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField()),
                ('description', models.TextField()),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('support_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.supportrequest')),
            ],
            options={
                'db_table': 'support_activities',
            },
        ),
    ]
