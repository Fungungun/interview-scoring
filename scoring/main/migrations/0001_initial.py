# Generated by Django 3.1.4 on 2020-12-29 14:44

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Examiner',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('examiner_id', models.IntegerField(default=0)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Interviewer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('draw_id', models.CharField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='SingleScoreForm',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score_1', models.IntegerField(default=0)),
                ('score_2', models.IntegerField(default=0)),
                ('score_3', models.IntegerField(default=0)),
                ('score_4', models.IntegerField(default=0)),
                ('score_5', models.IntegerField(default=0)),
                ('comment', models.CharField(max_length=1000)),
                ('sig_filename', models.CharField(max_length=1000)),
                ('date', models.DateField(default=datetime.date.today)),
                ('examiner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.examiner')),
                ('interviewer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.interviewer')),
            ],
        ),
    ]
