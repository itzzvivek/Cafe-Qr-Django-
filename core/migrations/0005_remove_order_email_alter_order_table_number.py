# Generated by Django 5.0.5 on 2024-07-10 06:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_order_user_remove_orderitem_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
        migrations.AlterField(
            model_name='order',
            name='table_number',
            field=models.IntegerField(),
        ),
    ]
