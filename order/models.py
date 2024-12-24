from django.db import models

from SovaStore import settings
from store.models import Product


class Order(models.Model):
    class StatusChoices(models.TextChoices):
        PROCESSING = "Processing"
        IN_PROCESS = "In process"
        DONE = "Done"

    date = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=100,
        choices=StatusChoices.choices,
        default=StatusChoices.PROCESSING,
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="orders"
    )

    def __str__(self):
        return f"{self.user} - {self.date}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())

    class Meta:
        ordering = ("-date",)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product_id = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="items"
    )
    quantity = models.PositiveIntegerField(default=1)

    @property
    def total_price(self):
        return self.product_id.price * self.quantity

    def __str__(self):
        return f"{self.product_id.name} x {self.quantity} for {self.order}"
