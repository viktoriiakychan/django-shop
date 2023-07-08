# Generated by Django 4.2.2 on 2023-07-05 14:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_deliverydetails_order_basket'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField()),
                ('email', models.CharField()),
                ('subject', models.CharField(blank=True, null=True)),
                ('message', models.CharField()),
            ],
        ),
    ]
