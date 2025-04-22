from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = '__all__'

    def get_image(self, obj):
        """To‘liq rasm URL ni qaytarish"""
        request = self.context.get('request')  # request ni olish
        if obj.image:
            return request.build_absolute_uri(obj.image.url)  # To‘liq URL yaratish
        return None
