# Generated by Django 5.0.2 on 2024-02-08 00:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='phone',
        ),
        migrations.AddField(
            model_name='customer',
            name='phone_number',
            field=models.CharField(default='-', max_length=20),
            preserve_default=False,
        ),
    ]
