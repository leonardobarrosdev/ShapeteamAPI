# Generated by Django 5.0.2 on 2025-03-01 20:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chat', '0002_initial'),
        ('shapeteam', '0003_alter_weekroutine_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chat',
            name='connection',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='created',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='message',
        ),
        migrations.RemoveField(
            model_name='chat',
            name='user',
        ),
        migrations.AddField(
            model_name='chat',
            name='participants',
            field=models.ManyToManyField(related_name='chats', to='shapeteam.connection'),
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('contact', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='messages', to='shapeteam.connection')),
            ],
        ),
        migrations.AddField(
            model_name='chat',
            name='messages',
            field=models.ManyToManyField(blank=True, to='chat.message'),
        ),
    ]
