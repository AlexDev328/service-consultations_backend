# Generated by Django 3.2.5 on 2021-07-19 16:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('consultations', '0005_auto_20210719_1444'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='auth_code',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='consultations.authcode'),
        ),
    ]
