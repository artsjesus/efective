from orders.apps import OrdersConfig
from orders.views import (
    OrderCreateView,
    OrderDeleteView,
    OrderDetailView,
    OrderUpdateView,
    OrderListView,
    RevenueView,
    OrderListAPIView,
    OrderRetrieveUpdateDestroyAPIView,
    OrderCreateAPIView,
)
from django.urls import path

app_name = OrdersConfig.name

urlpatterns = [
    path("", OrderListView.as_view(), name="order_list"),
    path("create/", OrderCreateView.as_view(), name="order_create"),
    path("orders/revenue/", RevenueView.as_view(), name="revenue"),
    path("<int:pk>/update", OrderUpdateView.as_view(), name="order_update"),
    path("<int:pk>/delete", OrderDeleteView.as_view(), name="order_delete"),
    path("<int:pk>/", OrderDetailView.as_view(), name="order_detail"),
    path("api/orders/", OrderListAPIView.as_view(), name="api_list"),
    path("api/orders/create/", OrderCreateAPIView.as_view(), name="api_create"),
    path(
        "api/orders/<int:pk>/",
        OrderRetrieveUpdateDestroyAPIView.as_view(),
        name="api_RetrieveUpdateDestroy",
    ),
]
