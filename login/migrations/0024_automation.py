# Generated by Django 3.1.7 on 2021-06-12 16:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0023_auto_20210612_1411'),
    ]

    operations = [
        migrations.CreateModel(
            name='Automation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Status', models.CharField(max_length=30)),
                ('Start_Time', models.DateTimeField()),
                ('End_Time', models.DateTimeField()),
                ('Button', models.CharField(blank=True, max_length=30)),
            ],
        ),
    ]
