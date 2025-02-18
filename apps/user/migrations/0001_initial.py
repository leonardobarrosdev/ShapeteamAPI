# Generated by Django 5.0.2 on 2025-02-18 09:49

import apps.user.models
import cloudinary.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Goal',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.SmallIntegerField(blank=True, choices=[(1, 'Hipertrofia Muscular '), (2, 'Perda de Peso '), (3, 'Definição Muscular '), (4, 'Ganho de Resistência'), (5, 'Aumento de Força '), (6, 'Saúde e Bem-estar '), (7, 'Melhora da Mobilidade e Flexibilidade '), (8, 'Reabilitação Física '), (9, 'Condicionamento Esportivo')], null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=30, unique=True)),
                ('first_name', models.CharField(blank=True, max_length=80, null=True)),
                ('last_name', models.CharField(blank=True, max_length=120, null=True)),
                ('thumbnail', cloudinary.models.CloudinaryField(default='profile.png', max_length=255, validators=[apps.user.models.file_validation])),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('gender', models.SmallIntegerField(blank=True, choices=[(1, 'male'), (2, 'female'), (3, 'other')], null=True)),
                ('height', models.FloatField(blank=True, null=True)),
                ('weight', models.FloatField(blank=True, null=True)),
                ('date_birth', models.DateField(blank=True, null=True)),
                ('level', models.SmallIntegerField(choices=[(1, 'basic'), (2, 'medium'), (3, 'advanced')], default=1)),
                ('is_staff', models.BooleanField(default=False)),
                ('is_active', models.BooleanField(default=False)),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
                ('goal', models.ManyToManyField(to='user.goal')),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', apps.user.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(default='Brazil', max_length=100)),
                ('zipcode', models.IntegerField()),
                ('state', models.CharField(max_length=2)),
                ('city', models.CharField(max_length=200)),
                ('neighborhood', models.CharField(blank=True, max_length=200, null=True)),
                ('street', models.CharField(blank=True, max_length=200, null=True)),
                ('number', models.PositiveSmallIntegerField(default=0)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
