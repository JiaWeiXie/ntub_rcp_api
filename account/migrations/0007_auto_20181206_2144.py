# Generated by Django 2.1.3 on 2018-12-06 13:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0006_orgunits_org_uuid'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='orgunits',
            options={'verbose_name': '單位組織資料表'},
        ),
        migrations.AlterModelOptions(
            name='student',
            options={'verbose_name': '學生資料表'},
        ),
        migrations.AlterModelOptions(
            name='teacher',
            options={'verbose_name': '教師資料表'},
        ),
    ]