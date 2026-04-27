from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:item_id>', views.item_page, name='item'),
    path('buy/<int:item_id>', views.buy_item, name='buy'),

path('order/add/<int:item_id>', views.add_to_order, name='add_to_order'),
    path('order/<int:order_id>/checkout', views.order_checkout, name='order_checkout'),
    path('order/success/', views.order_success, name='order_success'),
    path('order/cancel/', views.order_cancel, name='order_cancel'),
]
