# Generated by Django 4.2.6 on 2023-10-23 19:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0008_alter_bid_bid_amount_alter_listing_starting_bid_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.CharField(choices=[('electronics', 'Electronics'), ('clothing', 'Clothing'), ('books', 'Books'), ('gadgets', 'Gadgets'), ('others', 'Others')], default='other', max_length=64),
        ),
    ]
