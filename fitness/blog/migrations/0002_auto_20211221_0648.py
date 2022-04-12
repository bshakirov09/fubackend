# Generated by Django 3.2.9 on 2021-12-21 06:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('document', '0002_videomodel'),
        ('blog', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='blog',
            old_name='images',
            new_name='image',
        ),
        migrations.CreateModel(
            name='BlogImages',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dttm', models.DateTimeField(auto_now_add=True)),
                ('updated_dttm', models.DateTimeField(auto_now=True)),
                ('blog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='blog_images', related_query_name='blog_images', to='blog.blog')),
                ('image', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='document.imagemodel')),
            ],
            options={
                'ordering': ('-created_dttm',),
                'abstract': False,
            },
        ),
    ]