from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

from django.db import models

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='products/', blank=True, null=True)

    MEASUREMENT_CHOICES = [
        ('metr', 'Metr'),
        ('dona', 'Dona'),
        ('kg', 'Kilogramm'),
    ]
    measurement_unit = models.CharField(
        max_length=10,
        choices=MEASUREMENT_CHOICES,
        default='dona'
    )

    isTop = models.BooleanField(default=False)  # ✅ YANGI QO‘SHILGAN QATOR

    def __str__(self):
        return self.name

class Order(models.Model):
    first_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(max_length=20, null=True, blank=True)
    region = models.CharField(max_length=100, null=True, blank=True)
    district = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_total_price(self):
        total_price = sum(item.price * item.quantity for item in self.items.all())
        return total_price

    def __str__(self):
        return f"Buyurtma {self.id} - {self.first_name}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items", null=True, blank=True)
    product_name = models.CharField(max_length=200, null=True, blank=True)
    quantity = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def __str__(self):
        return f"{self.product_name} ({self.quantity})"