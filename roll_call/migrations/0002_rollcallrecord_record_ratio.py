# Generated by Django 2.1.1 on 2018-10-18 18:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('roll_call', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='rollcallrecord',
            name='record_ratio',
            field=models.FloatField(default=0.0, verbose_name='到課比例'),
        ),
    ]