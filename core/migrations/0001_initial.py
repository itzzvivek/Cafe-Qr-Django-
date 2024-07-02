# Generated by Django 5.0.5 on 2024-07-02 11:55

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cafeAdmin', '0003_cafe_qr_code'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coupon',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.CharField(max_length=15)),
                ('amount', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('cafe', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='cafeAdmin.cafe')),
            ],
        ),
        migrations.CreateModel(
            name='MenuItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, upload_to='menu_images')),
                ('max_price', models.DecimalField(decimal_places=2, max_digits=5)),
                ('min_price', models.DecimalField(blank=True, decimal_places=2, max_digits=5, null=True)),
                ('slug', models.SlugField()),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafeAdmin.cafe')),
                ('category', models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.category')),
            ],
        ),
        migrations.CreateModel(
            name='OrderItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ordered', models.BooleanField(default=False)),
                ('quantity', models.IntegerField(default=1)),
                ('is_half_portion', models.BooleanField(default=False)),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.menuitem')),
                ('user', models.ForeignKey(default=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_charge_id', models.CharField(max_length=50)),
                ('amount', models.FloatField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(default=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('order_id', models.AutoField(editable=False, primary_key=True, serialize=False, unique=True)),
                ('customer_name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(blank=True, max_length=15, null=True)),
                ('email', models.EmailField(max_length=245)),
                ('table_number', models.IntegerField(default=False)),
                ('message', models.TextField()),
                ('ordered_date', models.DateTimeField()),
                ('ordered', models.BooleanField(default=False)),
                ('refund_requested', models.BooleanField(default=False)),
                ('refund_granted', models.BooleanField(default=False)),
                ('cafe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafeAdmin.cafe')),
                ('coupon', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.coupon')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('items', models.ManyToManyField(related_name='orders', to='core.orderitem')),
                ('payment', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.payment')),
            ],
        ),
        migrations.CreateModel(
            name='Refund',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reason', models.TextField()),
                ('accepted', models.BooleanField(default=False)),
                ('email', models.EmailField(max_length=254)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.order')),
            ],
        ),
    ]
