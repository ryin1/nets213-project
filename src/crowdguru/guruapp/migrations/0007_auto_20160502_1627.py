# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2016-05-02 16:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('guruapp', '0006_auto_20160502_1627'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userdetails',
            name='interests',
        ),
        migrations.AddField(
            model_name='userdetails',
            name='interests',
            field=models.CharField(blank=True, max_length=1000),
        ),
    ]