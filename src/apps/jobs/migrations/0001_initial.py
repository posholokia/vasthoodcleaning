# Generated by Django 5.0.7 on 2024-09-05 12:01

import datetime
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('clients', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobModel',
            fields=[
                ('id', models.CharField(max_length=64, primary_key=True, serialize=False, unique=True)),
                ('schedule', models.DateTimeField(null=True)),
                ('address', models.CharField(max_length=256)),
                ('status', models.CharField(choices=[('unscheduled', 'needs scheduling'), ('scheduled', 'scheduled'), ('in_progress', 'in progress'), ('completed', 'complete unrated'), ('canceled', 'pro canceled')])),
                ('total_cost', models.IntegerField()),
                ('last_updated', models.DateTimeField(default=datetime.datetime(2024, 9, 5, 5, 0, 51, 971699))),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='jobs', to='clients.customermodel')),
            ],
        ),
    ]
