# Generated by Django 5.0.2 on 2024-02-08 00:51

import datetime
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('previous_balance', models.DecimalField(decimal_places=2, max_digits=20)),
                ('current_balance', models.DecimalField(decimal_places=2, max_digits=20)),
                ('transaction_time', models.DateTimeField(default=datetime.datetime.now)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=20)),
                ('transaction_id', models.CharField(max_length=100)),
                ('type', models.CharField(choices=[('Withdrawal', 'Withdrawal'), ('Deposit', 'Deposit'), ('Account Transfer', 'Account Transfer')], max_length=50)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]