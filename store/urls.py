from django.urls import path
from . import views

urlpatterns = [
    path('item/<int:item_id>', views.item_page, name='item'),
    path('buy/<int:item_id>', views.buy_item, name='buy'),
]
