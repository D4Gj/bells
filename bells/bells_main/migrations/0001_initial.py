# Generated by Django 5.0.4 on 2024-04-18 08:51

import django.contrib.auth.validators
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
            name='Bell',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('weight', models.FloatField()),
                ('manufacturer', models.CharField(max_length=100)),
                ('audio_file', models.FileField(blank=True, default=None, upload_to='bells/')),
                ('status', models.CharField(choices=[('READY_TO_TRANSFER', 'Готов к передаче'), ('IN_REQUEST_FOR_APPROVAL', 'В заявке на согласование'), ('IN_USE', 'Используется'), ('BELL_MISSING', 'Не хватает колокола')], default='PENDING', max_length=50)),
                ('image', models.ImageField(blank=True, default=None, upload_to='bell_images/')),
            ],
            options={
                'verbose_name': 'Колокол',
                'verbose_name_plural': 'Колоколы',
            },
        ),
        migrations.CreateModel(
            name='Temple',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('address', models.CharField(max_length=200)),
            ],
            options={
                'verbose_name': 'Храм',
                'verbose_name_plural': 'Храмы',
            },
        ),
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('phone_number', models.CharField(max_length=15, unique=True)),
                ('user_type', models.CharField(choices=[('admin', 'Админ'), ('church_operator', 'Оператор храма'), ('moderator', 'Moderator')], max_length=20)),
                ('is_key_keeper', models.BooleanField(default=False)),
                ('is_bell_ringer', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Belltower',
            fields=[
                ('temple', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='bells_main.temple')),
                ('belltower_name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Колокольня',
                'verbose_name_plural': 'Колокольни',
            },
        ),
        migrations.CreateModel(
            name='BellMovementRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('status', models.CharField(choices=[('PENDING', 'Ожидание'), ('REJECTED', 'Отклонён'), ('APPROVED', 'Одобрено')], default='PENDING', max_length=20, verbose_name='Статус')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('bell', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='bells_main.bell')),
                ('requester', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='requested_bell_movements', to=settings.AUTH_USER_MODEL)),
                ('temple_from', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bell_movement_requests_from', to='bells_main.temple', verbose_name='Храм откуда передаём')),
                ('temple_to', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bell_movement_requests_to', to='bells_main.temple', verbose_name='Храм куда передаём')),
                ('belltowerfrom', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bell_movement_tower_from', to='bells_main.belltower', verbose_name='Колокольня откуда')),
                ('belltowerto', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='bell_movement_tower_to', to='bells_main.belltower', verbose_name='Колокольня куда')),
            ],
            options={
                'verbose_name': 'Перемещение колокола',
                'verbose_name_plural': 'Перемещение колоколов',
            },
        ),
        migrations.AddField(
            model_name='bell',
            name='belltower',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bells', to='bells_main.belltower'),
        ),
    ]
