# Generated by Django 2.0.5 on 2018-06-05 09:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('curriculum', '0006_auto_20180513_0153'),
    ]

    operations = [
        migrations.RenameField(
            model_name='sectiontime',
            old_name='weak',
            new_name='week',
        ),
        migrations.AlterUniqueTogether(
            name='sectiontime',
            unique_together={('subjects', 'week', 'section')},
        ),
    ]