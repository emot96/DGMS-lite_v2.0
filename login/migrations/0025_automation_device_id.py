# Generated by Django 3.1.7 on 2021-06-12 16:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0024_automation'),
    ]

    operations = [
        migrations.AddField(
            model_name='automation',
            name='Device_ID',
            field=models.CharField(default='test', max_length=30),
        ),
    ]
