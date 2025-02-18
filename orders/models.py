from django.db import models
from django.core.exceptions import ValidationError


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "В ожидании"),
        ("ready", "Готово"),
        ("paid", "Оплачено"),
    ]
    table_number = models.IntegerField(verbose_name="Номер столика")
    items = models.JSONField(verbose_name="Список блюд с ценами")
    total_price = models.DecimalField(
        max_digits=10, decimal_places=2, verbose_name="Общая стоимость", default=0
    )
    status = models.CharField(
        max_length=10, choices=STATUS_CHOICES, default="pending", verbose_name="Статус"
    )

    def save(self, *args, **kwargs):
        """Сохраняем заказ и обновляем общую стоимость."""
        self.total_price = self.calculate_total_price()
        super().save(*args, **kwargs)

    def calculate_total_price(self) -> float:
        """Метод для расчета общей стоимости заказа."""
        return sum(item.get("price", 0) for item in self.items)

    def clean(self) -> None:
        """Метод для валидации элементов заказа."""
        for item in self.items:
            if "price" not in item:
                raise ValidationError("Каждый элемент должен содержать цену.")

    def __str__(self):
        return f"Заказ {self.id} - Стол {self.table_number}"

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
