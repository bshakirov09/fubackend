# Generated by Django 3.2.9 on 2022-01-18 17:47

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, unique=True)),
                ('type', models.CharField(choices=[('monthly', 'monthly'), ('yearly', 'yearly')], max_length=64, unique=True)),
                ('description', models.TextField()),
                ('price_amount', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='UserSubscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_dttm', models.DateTimeField(auto_now_add=True)),
                ('updated_dttm', models.DateTimeField(auto_now=True)),
                ('stripe_id', models.CharField(max_length=255)),
                ('is_trial', models.BooleanField(default=False)),
                ('subscription', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscriptions', to='subscription.subscription')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_subscriptions', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'subscription')},
            },
        ),
    ]
