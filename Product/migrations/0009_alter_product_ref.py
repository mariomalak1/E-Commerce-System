# Generated by Django 4.2.10 on 2024-03-06 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("Product", "0008_product_alter_brand_options_alter_category_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="ref",
            field=models.SlugField(
                allow_unicode=True, blank=True, max_length=200, unique=True
            ),
        ),
    ]
