# Generated by Django 5.0.5 on 2024-06-16 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_alter_payment_payment_charge_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(related_name='orders', to='core.orderitem'),
        ),
    ]
