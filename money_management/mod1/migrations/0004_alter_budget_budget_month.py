# Generated by Django 4.2.7 on 2023-11-22 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod1', '0003_budget'),
    ]

    operations = [
        migrations.AlterField(
            model_name='budget',
            name='budget_month',
            field=models.CharField(max_length=7),
        ),
    ]
