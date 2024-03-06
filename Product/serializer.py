from rest_framework import serializers

from .models import Brand, Category, SubCategory


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        exclude = ["id"]


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        exclude = ["id"]

class SubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubCategory
        exclude = ["id"]

    category = serializers.CharField()
