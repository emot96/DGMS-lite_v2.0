# Generated by Django 3.1.7 on 2021-07-25 19:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0032_auto_20210718_2356'),
    ]

    operations = [
        migrations.AlterField(
            model_name='manager',
            name='User',
            field=models.ForeignKey(max_length=50, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]