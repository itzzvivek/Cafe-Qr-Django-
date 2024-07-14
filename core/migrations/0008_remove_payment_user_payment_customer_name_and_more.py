# Generated by Django 5.0.5 on 2024-07-14 13:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_orderitem_user_alter_menuitem_cafe'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='payment',
            name='user',
        ),
        migrations.AddField(
            model_name='payment',
            name='customer_name',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='payment',
            name='payment_method',
            field=models.CharField(blank=True, choices=[('cash', 'Cash'), ('razorpay', 'Razorpay')], max_length=50, null=True),
        ),
    ]
