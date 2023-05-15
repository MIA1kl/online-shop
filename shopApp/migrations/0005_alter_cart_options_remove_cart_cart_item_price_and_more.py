# Generated by Django 4.2.1 on 2023-05-15 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopApp', '0004_cart_cart_item_price_delete_order'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={},
        ),
        migrations.RemoveField(
            model_name='cart',
            name='cart_item_price',
        ),
        migrations.AddField(
            model_name='cart',
            name='total_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
    ]
