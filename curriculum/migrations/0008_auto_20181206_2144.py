# Generated by Django 2.1.3 on 2018-12-06 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0007_auto_20180605_1736'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='sectiontime',
            options={'verbose_name': '課程節次資料表'},
        ),
        migrations.AlterModelOptions(
            name='subjects',
            options={'verbose_name': '課程資料表'},
        ),
    ]