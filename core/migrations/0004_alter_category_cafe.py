# Generated by Django 5.0.5 on 2024-06-23 17:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cafeAdmin', '0002_rename_name_cafe_cafe_name'),
        ('core', '0003_category_cafe'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='cafe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cafeAdmin.cafe'),
        ),
    ]
