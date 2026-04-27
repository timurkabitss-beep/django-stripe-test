from django.db import models

class Item(models.Model):
    name = models.CharField(max_length=200, verbose_name="Название товара")
    price =models.PositiveIntegerField(
        verbose_name="Цена (в центах)",
        help_text="Цена указывается в минорных единицах валюты. Например, 1000 = 10.00 $"
    )
    description = models.TextField(blank=True, default="")

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('cancelled', 'Cancelled'),
    ]

    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    stripe_payment_intent_id = models.CharField(max_length=100, blank=True, null=True)
    total_amount = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Order #{self.id} - {self.status}"

    def calculate_total(self):
        total = sum(item.get_subtotal() for item in self.items.all())
        self.total_amount = total
        self.save()
        return total


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_at_purchase = models.PositiveIntegerField()

    def get_subtotal(self):
        return self.price_at_purchase * self.quantity

    def __str__(self):
        return f"{self.quantity}x {self.item.name}"