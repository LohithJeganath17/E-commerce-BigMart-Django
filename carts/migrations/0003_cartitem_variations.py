# Generated by Django 5.2.3 on 2025-07-16 11:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_rename_item_cartitem_cart'),
        ('store', '0002_variationmodel'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitem',
            name='variations',
            field=models.ManyToManyField(blank=True, to='store.variationmodel'),
        ),
    ]
