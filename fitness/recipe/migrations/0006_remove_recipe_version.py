# Generated by Django 3.2.9 on 2021-12-08 12:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0005_alter_recipe_title'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='version',
        ),
    ]