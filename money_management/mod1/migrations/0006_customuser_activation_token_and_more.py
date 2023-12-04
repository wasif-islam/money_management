# Generated by Django 4.2.7 on 2023-12-02 22:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mod1', '0005_customuser_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='activation_token',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
    ]