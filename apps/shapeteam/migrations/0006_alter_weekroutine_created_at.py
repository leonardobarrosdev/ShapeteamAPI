# Generated by Django 5.1.7 on 2025-04-18 00:11

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shapeteam', '0005_alter_weekroutine_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weekroutine',
            name='created_at',
            field=models.DateField(db_default=datetime.date(2025, 4, 18)),
        ),
    ]
