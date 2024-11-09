# Generated by Django 5.1.2 on 2024-11-07 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_alter_order_delivery_type_alter_order_order_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_type',
            field=models.CharField(blank=True, choices=[('immediate', 'Immediate'), ('scheduled', 'Scheduled')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_type',
            field=models.CharField(choices=[('delivery', 'Delivery'), ('pickup', 'Pickup')], default='delivery', max_length=10),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(choices=[('processing', 'Processing'), ('preparing', 'Preparing'), ('delivering', 'Delivering'), ('delivered', 'Delivered'), ('canceled', 'Canceled')], default='processing', max_length=20),
        ),
    ]