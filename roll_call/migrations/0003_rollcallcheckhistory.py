# Generated by Django 2.1.1 on 2018-10-18 18:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_orgunits_org_uuid'),
        ('curriculum', '0007_auto_20180605_1736'),
        ('roll_call', '0002_rollcallrecord_record_ratio'),
    ]

    operations = [
        migrations.CreateModel(
            name='RollCallCheckHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check_time', models.TimeField(auto_now_add=True)),
                ('check_date', models.DateField(auto_now_add=True)),
                ('beacon', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='roll_call.Beacon', verbose_name='iBeacon')),
                ('section_time', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='curriculum.SectionTime', verbose_name='節次')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.Student', verbose_name='學生')),
            ],
        ),
    ]
