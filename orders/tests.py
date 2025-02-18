from django.test import TestCase
from orders.models import Order
from django.core.exceptions import ValidationError


# Create your tests here.
class OrderModelTest(TestCase):
    def setUp(self):
        """Создаем базовые данные для тестов."""
        self.order_data = {
            "table_number": 1,
            "items": [{"name": "Паста", "price": 200}, {"name": "Пицца", "price": 300}],
            "status": "pending",
        }
        self.order = Order.objects.create(**self.order_data)

    def test_order_creation(self):
        """Тестируем создание заказа."""
        self.assertEqual(self.order.table_number, 1)
        self.assertEqual(len(self.order.items), 2)
        self.assertEqual(self.order.total_price, 500)
        self.assertEqual(self.order.status, "pending")

    def test_calculate_total_price(self):
        """Тестируем метод подсчета общей стоимости."""
        self.assertEqual(self.order.calculate_total_price(), 500)

    def test_validate_items(self):
        """Тестируем валидацию элементов заказа."""
        # Корректный список
        valid_order = Order(
            items=[{"name": "Бургер", "price": 150}, {"name": "Салат", "price": 100}]
        )
        try:
            valid_order.clean()
        except ValidationError:
            self.fail("ValidationError raised for valid items.")

        # Некорректный список
        invalid_order = Order(items=[{"name": "Бургер"}])  # Без 'price'
        with self.assertRaises(ValidationError):
            invalid_order.clean()

    def test_str_method(self):
        """Тестируем строковое представление заказа."""
        self.assertEqual(
            str(self.order), f"Заказ {self.order.id} - Стол {self.order.table_number}"
        )

    def test_order_status_choices(self):
        """Тестируем доступные статусы заказа."""
        self.assertIn(self.order.status, dict(Order.STATUS_CHOICES))
