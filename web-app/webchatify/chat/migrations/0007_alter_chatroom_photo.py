# Generated by Django 4.2.1 on 2023-05-27 22:29

import chat.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0006_rename_color_profile_color_session_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatroom',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to=chat.models.get_upload_chat_path),
        ),
    ]
