# Generated by Django 4.2.1 on 2023-05-25 21:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatroom',
            name='invite_link',
            field=models.CharField(default='D27B72B93007', max_length=100),
        ),
        migrations.AlterField(
            model_name='message',
            name='timestamp',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
