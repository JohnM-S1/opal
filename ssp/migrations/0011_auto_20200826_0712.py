# Generated by Django 3.0.7 on 2020-08-26 12:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ssp', '0010_auto_20200826_0700'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='control_implementation',
            name='control_id',
        ),
        migrations.RemoveField(
            model_name='system_control',
            name='control_id',
        ),
    ]