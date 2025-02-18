from orders.models import Order
from django import forms


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ["table_number", "status", "items"]
