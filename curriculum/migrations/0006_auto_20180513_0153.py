# Generated by Django 2.0.4 on 2018-05-12 17:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0005_auto_20180508_2131'),
    ]

    operations = [
        migrations.AlterField(
            model_name='sectiontime',
            name='subjects',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='section_times', to='curriculum.Subjects', verbose_name='科目'),
        ),
    ]