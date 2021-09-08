# Generated by Django 3.2.6 on 2021-09-01 08:28

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.datetime_safe


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('clients', '0024_alter_client_logo'),
    ]

    operations = [
        migrations.CreateModel(
            name='AMCRenewal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('created_at', models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now)),
                ('client_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='clients.clientproject')),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Manage AMC Renewals',
                'db_table': 'amc_renewals',
            },
        ),
        migrations.CreateModel(
            name='AMCDocuments',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uploaded_at', models.DateTimeField(blank=True, default=django.utils.datetime_safe.datetime.now)),
                ('file', models.FileField(blank=True, null=True, upload_to='AMCRenewalDocs/')),
                ('amc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='amc.amcrenewal')),
            ],
            options={
                'verbose_name_plural': 'AMC Documents',
                'db_table': 'amc_files',
            },
        ),
    ]