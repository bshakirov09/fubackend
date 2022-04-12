# Generated by Django 3.2.9 on 2021-12-10 11:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0001_initial'),
        ('recipe', '0006_remove_recipe_version'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='order_number',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dttm', models.DateTimeField(auto_now_add=True)),
                ('updated_dttm', models.DateTimeField(auto_now=True)),
                ('order_number', models.PositiveIntegerField()),
                ('image', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='document.imagemodel')),
            ],
            options={
                'ordering': ('-created_dttm',),
                'abstract': False,
            },
        ),
    ]
