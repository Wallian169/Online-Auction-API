# Generated by Django 5.1.4 on 2025-02-19 08:38

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('image', models.ImageField(blank=True, default=None, null=True, upload_to='images/categories')),
            ],
            options={
                'verbose_name_plural': 'Categories',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='AuctionLot',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('item_name', models.CharField(max_length=100)),
                ('description', models.TextField(max_length=1000)),
                ('location', models.CharField(max_length=100)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('initial_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('min_step', models.DecimalField(decimal_places=2, max_digits=10)),
                ('buyout_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('close_time', models.DateTimeField()),
                ('is_active', models.BooleanField(default=True)),
                ('favourites', models.ManyToManyField(blank=True, related_name='favourite_lots', to=settings.AUTH_USER_MODEL)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction_lots', to=settings.AUTH_USER_MODEL)),
                ('winner', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='won_auction_lots', to=settings.AUTH_USER_MODEL)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='auction_lots', to='auction_api.category')),
            ],
        ),
        migrations.CreateModel(
            name='AuctionLotImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(blank=True, null=True, upload_to='lot_images/')),
                ('uploaded_at', models.DateTimeField(auto_now_add=True)),
                ('lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='images', to='auction_api.auctionlot')),
            ],
        ),
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offered_price', models.DecimalField(decimal_places=2, max_digits=10)),
                ('bid_time', models.DateTimeField(auto_now_add=True)),
                ('auction_lot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='auction_api.auctionlot')),
                ('bidder', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
