# Generated by Django 3.2 on 2022-08-20 08:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('checkout_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='country_code',
            new_name='country',
        ),
    ]
