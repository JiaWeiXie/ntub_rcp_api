# Generated by Django 2.1.3 on 2018-12-06 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('roll_call', '0003_rollcallcheckhistory'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='rollcallcheck',
            options={'verbose_name': '點名資料表'},
        ),
        migrations.AlterModelOptions(
            name='rollcallcheckhistory',
            options={'verbose_name': '點名歷史資料表'},
        ),
        migrations.AlterModelOptions(
            name='rollcallrecord',
            options={'verbose_name': '缺曠紀錄資料表'},
        ),
    ]
