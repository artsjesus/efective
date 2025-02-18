from django.views.generic import (
    TemplateView,
    ListView,
    UpdateView,
    CreateView,
    DetailView,
    DeleteView,
)
from orders.models import Order
from orders.forms import OrderForm
from django.urls import reverse_lazy
from django.db.models import Sum
from rest_framework.generics import (
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    ListAPIView,
)
from orders.serializers import OrderSerializer
from django.shortcuts import get_object_or_404


class OrderListView(ListView):
    """Список заказов"""

    model = Order
    template_name = "orders/order_list.html"
    context_object_name = "orders"

    def get_queryset(self):
        """Фильтрация только по статусу через GET-параметр"""

        # Получаем параметр статуса из GET-запроса
        status_filter = self.request.GET.get("status", "")

        queryset = Order.objects.all()  # Начинаем с всех заказов

        # Фильтрация по статусу
        if status_filter:
            queryset = queryset.filter(status=status_filter)

        return queryset


class OrderCreateView(CreateView):
    """Создание заказа"""

    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("orders:order_list")


class OrderDeleteView(DeleteView):
    """Удаление заказа"""

    model = Order
    template_name = "orders/order_confirm_delete.html"
    success_url = reverse_lazy("orders:order_list")

    def get_object(self, queryset=None):
        return get_object_or_404(Order, pk=self.kwargs["pk"])


class OrderUpdateView(UpdateView):
    """Изменение заказа"""

    model = Order
    form_class = OrderForm
    success_url = reverse_lazy("orders:order_list")


class OrderDetailView(DetailView):
    """Детальная страница заказа"""

    model = Order
    template_name = "orders/order_detail.html"
    context_object_name = "order"


class RevenueView(TemplateView):
    """Выручка за смену"""

    template_name = "orders/revenue.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получаем все заказы с статусом "оплачено"
        paid_orders = Order.objects.filter(status="paid")

        # Считаем общую выручку
        total_revenue = (
            paid_orders.aggregate(Sum("total_price"))["total_price__sum"] or 0
        )

        # Добавляем выручку в контекст
        context["total_revenue"] = total_revenue
        return context


class OrderListAPIView(ListAPIView):
    """
    Список всех заказов или создание нового заказа.
    """

    serializer_class = OrderSerializer
    queryset = Order.objects.all()


class OrderCreateAPIView(CreateAPIView):
    """
    Создание нового заказа.
    """

    serializer_class = OrderSerializer


class OrderRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    """
    Получение, обновление или удаление заказа по ID.
    """

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        return get_object_or_404(Order, pk=self.kwargs["pk"])
