# Generated by Django 5.1.4 on 2024-12-21 18:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auction_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='auctionlot',
            name='images',
            field=models.ImageField(null=True, upload_to='images/'),
        ),
    ]
