# Generated by Django 4.2.2 on 2023-06-17 16:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='imagePath',
            field=models.CharField(max_length=500, null=True),
        ),
    ]
