# Generated by Django 3.2.9 on 2022-01-18 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0002_auto_20220118_1820'),
    ]

    operations = [
        migrations.AddField(
            model_name='usersubscription',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]
