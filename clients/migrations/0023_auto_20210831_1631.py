# Generated by Django 3.2.6 on 2021-08-31 12:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('clients', '0022_alter_supportrequest_status'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='client',
            options={'verbose_name_plural': 'Manage Clients'},
        ),
        migrations.AlterModelOptions(
            name='clientproject',
            options={'verbose_name_plural': 'Client Projects'},
        ),
        migrations.AlterModelOptions(
            name='clientprojectdocument',
            options={'verbose_name_plural': 'Manage Client Project Documents'},
        ),
        migrations.AlterModelOptions(
            name='supportactivity',
            options={'verbose_name_plural': 'Support Request Activities'},
        ),
        migrations.AlterModelOptions(
            name='supportrequest',
            options={'verbose_name_plural': 'Support Requests'},
        ),
        migrations.AlterModelOptions(
            name='supportrequestactivityfiles',
            options={'verbose_name_plural': 'Support Request Activity Files'},
        ),
        migrations.AlterModelOptions(
            name='supportrequestfiles',
            options={'verbose_name_plural': 'Support Request Files'},
        ),
        migrations.AlterField(
            model_name='client',
            name='logo',
            field=models.FileField(blank=True, default='client_default.png', null=True, upload_to='clients/'),
        ),
    ]
