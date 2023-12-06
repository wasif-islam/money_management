# Generated by Django 4.2.6 on 2023-12-06 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod4', '0005_remove_transaction_total_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='price_per_unit',
            field=models.DecimalField(decimal_places=20, max_digits=20),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='stock',
            field=models.CharField(max_length=255),
        ),
    ]
