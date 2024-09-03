from rest_framework import serializers, exceptions, permissions
from django.contrib.auth.models import User
from .models import Product, Category
from uuid import UUID

#create catergorySerializer
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ("id", "label")

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()

    class Meta:
        model = Product
        fields =  ('id', 'label', 'brand', 'price', 'reference', 'description','tva', 'category')


class CreateProductSerializer(serializers.ModelSerializer):

    category_id = serializers.CharField()
    class Meta:
        model = Product
        fields = ( 'label', 'brand', 'price', 'reference', 'description', 'tva', 'category_id')
        read_only_fields = ['created_at', 'updated_at']

    # validation methods for category_id fields
    def validate_category_id(self, value):
        try:
            return Category.objects.get(id=value)
        except Category.DoesNotExist:
            raise serializers.ValidationError("The category does not exist.")

    def create(self, validated_data):
        # get category_id from validated_data using .get

        category = validated_data.pop('category_id')
        product = Product.objects.create(category=category, **validated_data)
        product_data = super().to_representation(product)
        product_data['category_id'] = category.id
        return product_data




