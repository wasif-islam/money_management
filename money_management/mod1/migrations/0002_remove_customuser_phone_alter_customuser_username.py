# Generated by Django 4.2.7 on 2023-11-15 20:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod1', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='phone',
        ),
        migrations.AlterField(
            model_name='customuser',
            name='username',
            field=models.CharField(max_length=30, unique=True),
        ),
    ]
