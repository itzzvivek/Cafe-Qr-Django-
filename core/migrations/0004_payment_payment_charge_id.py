# Generated by Django 5.0.5 on 2024-06-08 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_order_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='payment',
            name='payment_charge_id',
            field=models.CharField(default=False, max_length=50),
        ),
    ]