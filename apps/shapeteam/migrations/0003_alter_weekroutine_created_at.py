# Generated by Django 5.0.2 on 2025-03-01 20:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shapeteam', '0002_alter_weekroutine_created_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='weekroutine',
            name='created_at',
            field=models.DateField(db_default=datetime.date(2025, 3, 1)),
        ),
    ]
