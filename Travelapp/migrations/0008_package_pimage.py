# Generated by Django 5.1.3 on 2024-11-06 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Travelapp', '0007_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='package',
            name='pimage',
            field=models.ImageField(default=0, upload_to='image'),
            preserve_default=False,
        ),
    ]
