# Generated by Django 5.1.3 on 2024-11-07 16:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travelapp', '0010_remove_cart_contact_no_remove_cart_from_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cart',
            name='qty',
            field=models.IntegerField(default=1),
        ),
    ]
