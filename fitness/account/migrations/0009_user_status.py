# Generated by Django 3.2.9 on 2022-01-20 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_auto_20220118_1747'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='status',
            field=models.CharField(choices=[('active', 'Active'), ('blocked', 'Blocked'), ('restricted', 'Restricted')], default='active', max_length=50),
        ),
    ]
