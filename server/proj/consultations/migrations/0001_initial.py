# Generated by Django 3.2.5 on 2021-07-07 05:13

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('closed_at', models.DateTimeField(blank=True, null=True)),
                ('data', models.JSONField(blank=True, null=True, verbose_name='Данные о элементе консультации')),
                ('is_done', models.BooleanField(default=False, verbose_name='Завершен')),
                ('is_active', models.BooleanField(default=True, verbose_name='Активен')),
            ],
            options={
                'verbose_name': 'Консультация',
                'verbose_name_plural': 'Консультации',
            },
        ),
        migrations.CreateModel(
            name='Conclusion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cons_text', models.TextField(default='', verbose_name='Заключение консультанта')),
                ('user_text', models.TextField(blank=True, default='', verbose_name='Комментарий товароведа')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('final', models.BooleanField()),
                ('application', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='consultations.application')),
            ],
            options={
                'verbose_name': 'Заключение',
                'verbose_name_plural': 'Заключения',
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Тема консультации')),
            ],
            options={
                'verbose_name': 'категория',
                'verbose_name_plural': 'категории',
            },
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, related_name='profile', serialize=False, to='auth.user')),
                ('city', models.CharField(blank=True, default='', max_length=70, verbose_name='Город')),
                ('filial', models.CharField(blank=True, default='', max_length=255, verbose_name='филиал')),
                ('peerid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid пользователя(товароведа)')),
                ('consultant', models.BooleanField(blank=True, default=False, verbose_name='Консультант')),
                ('user_inner_id', models.CharField(blank=True, max_length=255, null=True, verbose_name='Внешний id пользователя')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='WorkerProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, default='', max_length=255, verbose_name='ФИО')),
                ('city', models.CharField(blank=True, default='', max_length=70, verbose_name='Город')),
                ('filial', models.CharField(blank=True, default='', max_length=255, verbose_name='филиал')),
                ('peerid', models.UUIDField(default=uuid.uuid4, editable=False, verbose_name='uuid пользователя(товароведа)')),
                ('consultant', models.BooleanField(blank=True, default=False, verbose_name='Консультант')),
                ('user_inner_id', models.CharField(max_length=255, verbose_name='Внешний id пользователя')),
            ],
            options={
                'verbose_name': 'Товаровед',
                'verbose_name_plural': 'Пользователи',
            },
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='', verbose_name='фотография')),
                ('conclusion', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='consultations.conclusion')),
            ],
        ),
        migrations.AddField(
            model_name='conclusion',
            name='consultant',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='consultations.userprofile'),
        ),
        migrations.AddField(
            model_name='application',
            name='insigator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='consultations.workerprofile', verbose_name='инициатор'),
        ),
        migrations.AddField(
            model_name='application',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='consultations.topic', verbose_name='Категория'),
        ),
    ]
