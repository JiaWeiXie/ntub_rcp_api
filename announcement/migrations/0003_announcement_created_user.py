# Generated by Django 2.1.1 on 2018-10-19 04:04

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('announcement', '0002_auto_20180509_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='created_user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL, verbose_name='張貼人'),
        ),
    ]
