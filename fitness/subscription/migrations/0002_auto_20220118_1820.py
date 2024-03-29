# Generated by Django 3.2.9 on 2022-01-18 18:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('subscription', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='usersubscription',
            old_name='stripe_id',
            new_name='stripe_subscription_id',
        ),
        migrations.AddField(
            model_name='usersubscription',
            name='stripe_customer_id',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='usersubscription',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscription', to=settings.AUTH_USER_MODEL),
        ),
    ]
