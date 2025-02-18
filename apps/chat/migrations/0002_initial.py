# Generated by Django 5.0.2 on 2025-02-18 10:49

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chat', '0001_initial'),
        ('shapeteam', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='chat',
            name='connection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='shapeteam.connection'),
        ),
        migrations.AddField(
            model_name='chat',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='my_messages', to=settings.AUTH_USER_MODEL),
        ),
    ]
