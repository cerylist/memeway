# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-01-16 17:21
from __future__ import unicode_literals

from django.db import migrations, models
import memeway


class Migration(migrations.Migration):

    dependencies = [
        ('rater', '0016_user_email'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='can_rest_password',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='code_reset',
            field=models.CharField(default=memeway.random_generator, max_length=16),
        ),
        migrations.AddField(
            model_name='user',
            name='email_link',
            field=models.CharField(default=memeway.random_generator, max_length=16),
        ),
    ]