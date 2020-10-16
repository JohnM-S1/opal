# Generated by Django 3.0.7 on 2020-10-15 18:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ssp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='attachment',
            name='hash',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='ssp.hashed_value'),
        ),
    ]
