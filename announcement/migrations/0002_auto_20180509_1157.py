# Generated by Django 2.0.4 on 2018-05-09 03:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcement', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='announcement',
            name='postTarget',
            field=models.ManyToManyField(to='curriculum.Subjects', verbose_name='公告目標'),
        ),
    ]