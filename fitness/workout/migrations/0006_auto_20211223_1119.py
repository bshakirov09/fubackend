# Generated by Django 3.2.9 on 2021-12-23 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('workout', '0005_auto_20211223_1105'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gymtrack',
            name='percentage',
        ),
        migrations.AddField(
            model_name='gymtrack',
            name='completed_quad_count',
            field=models.PositiveSmallIntegerField(default=0),
        ),
    ]
