# Generated by Django 5.0.5 on 2024-07-15 19:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_rename_payment_charge_id_payment_razorpay_charge_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='payment',
            name='razorpay_charge_id',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]