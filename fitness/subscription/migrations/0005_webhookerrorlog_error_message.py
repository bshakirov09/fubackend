# Generated by Django 3.2.9 on 2022-01-24 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription', '0004_webhookerrorlog'),
    ]

    operations = [
        migrations.AddField(
            model_name='webhookerrorlog',
            name='error_message',
            field=models.TextField(default=1),
            preserve_default=False,
        ),
    ]
