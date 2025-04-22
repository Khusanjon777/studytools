from django.contrib import admin
from django import forms
from .models import Category, Product, Order, OrderItem

# OrderItem modelini inline tarzda qo'shish
class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1  # Bu yangi bo'sh satrni qo'shadi

# Order modelini admin panelda sozlash
class OrderAdminForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = '__all__'

    # Umumiy narxni hisoblash va ko'rsatish
    def clean(self):
        cleaned_data = super().clean()
        total_price = self.instance.get_total_price()  # Umumiy narxni hisoblash
        cleaned_data['total_price'] = total_price  # Bu qiymatni saqlash
        return cleaned_data

class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'first_name', 'phone', 'region', 'district', 'created_at', 'get_cart_items', 'get_total_price')
    inlines = [OrderItemInline]  # OrderItemlarni inline tarzda qo'shish
    readonly_fields = ('get_total_price',)  # Umumiy narxni faqat o'qish uchun maydon qilish
    
    # Buyurtma uchun umumiy narxni hisoblash va ko'rsatish
    def get_total_price(self, obj):
        return obj.get_total_price()

    get_total_price.short_description = 'Umumiy Narx'  # Admin paneli uchun nomi

    def get_cart_items(self, obj):
        # Buyurtma ichidagi barcha mahsulotlar (cart_items)ni chiqarish
        return ", ".join([f"{item.product_name} (x{item.quantity})" for item in obj.items.all()])
    
    get_cart_items.short_description = 'Cart Items'  # Admin paneli uchun nomi

# Category va Product modellarini ro‘yxatdan o‘tkazish
admin.site.register(Category)
admin.site.register(Product)

# Order modelini ro‘yxatdan o‘tkazish
admin.site.register(Order, OrderAdmin)
