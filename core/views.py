from django.shortcuts import render
from rest_framework import generics
from .models import Product
from .serializers import ProductSerializer
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Order, OrderItem
import requests
from django.conf import settings
from django.http import HttpResponse



class ProductListAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all()
        category_id = self.request.GET.get('category')  # URL'dan kategoriya ID olish
        
        if category_id:
            queryset = queryset.filter(category_id=category_id)  # Kategoriya bo‘yicha filter
        return queryset
    
    def get_serializer_context(self):
        """Serializer uchun request obyektini qo‘shish"""
        return {'request': self.request}


@csrf_exempt
def create_order(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            first_name = data.get("first_name")
            phone = data.get("phone")
            region = data.get("region")
            district = data.get("district")
            cart_items = data.get("cart_items", [])

            if not first_name or not phone or not region or not district:
                return JsonResponse({"error": "Barcha maydonlar talab qilinadi!"}, status=400)

            order = Order.objects.create(
                first_name=first_name,
                phone=phone,
                region=region,
                district=district
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product_name=item["name"],
                    quantity=item["quantity"],
                    price=item["price"]
                )

            return JsonResponse({"message": "Buyurtma qabul qilindi!"}, status=201)

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)
    
    return JsonResponse({"error": "Yaroqsiz so‘rov"}, status=400)
