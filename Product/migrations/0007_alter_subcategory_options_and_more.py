# Generated by Django 4.2.10 on 2024-03-06 17:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("Product", "0006_subcategory"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="subcategory",
            options={"ordering": ["ref", "created_at", "updated_at"]},
        ),
        migrations.RenameField(
            model_name="brand",
            old_name="create_at",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="category",
            old_name="create_at",
            new_name="created_at",
        ),
        migrations.RenameField(
            model_name="subcategory",
            old_name="create_at",
            new_name="created_at",
        ),
    ]