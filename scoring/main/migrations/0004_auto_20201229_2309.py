# Generated by Django 3.1.4 on 2020-12-29 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20201229_2309'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examiner',
            name='room_id',
            field=models.IntegerField(default=1),
        ),
    ]
