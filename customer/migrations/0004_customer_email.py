# Generated by Django 5.0.2 on 2024-02-08 00:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer', '0003_alter_customer_options_customer_first_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='email',
            field=models.EmailField(default='=', max_length=254),
            preserve_default=False,
        ),
    ]