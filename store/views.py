import stripe
import os
from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Item, Order, OrderItem
from django.views.decorators.http import require_POST
import json
from django.http import JsonResponse

stripe.api_key = settings.STRIPE_SECRET_KEY

def item_page(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'store/item.html', {
        'item': item,
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })

def buy_item(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[{ 'price_data': {
            'currency': 'usd',
            'product_data': {
                'name': item.name,
                'description': item.description,
            },
            'unit_amount': item.price,
        }, 'quantity': 1
    }],
        mode='payment',
        success_url='http://127.0.0.1:8000/success',
        cancel_url='http://127.0.0.1:8000/cancel',
    )
    return JsonResponse({'url': session.url})


@require_POST
def add_to_order(request, item_id):
    item = get_object_or_404(Item, id=item_id)

    # Создаём новый заказ
    order = Order.objects.create(status='pending')

    # Добавляем позицию
    OrderItem.objects.create(
        order=order,
        item=item,
        quantity=1,
        price_at_purchase=item.price
    )

    # Пересчитываем итог и сохраняем
    order.calculate_total()
    # Перекидываем на страницу оформления
    return redirect('order_checkout', order_id=order.id)


#Оформление заказа
def order_checkout(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Если нажали "Оплатить" (POST)
    if request.method == 'POST':
        line_items = []

        # Формируем список товаров для Stripe из состава заказа
        for order_item in order.items.all():
            line_items.append({
                'price_data': {
                    'currency': 'usd',
                    'product_data': {
                        'name': order_item.item.name,
                        'description': order_item.item.description,
                    },
                    'unit_amount': order_item.price_at_purchase,
                },
                'quantity': order_item.quantity,
            })

        # Создаём сессию
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url='http://127.0.0.1:8000/order/success/',
            cancel_url='http://127.0.0.1:8000/order/cancel/',
            metadata={'order_id': order.id}  # Сохраняем ID заказа в Stripe
        )

        # Сохраняем ID сессии в заказ
        order.stripe_payment_intent_id = session.id
        order.save()

        return JsonResponse({'url': session.url})

    #Если просто открыли страницу (GET)
    return render(request, 'store/order_checkout.html', {
        'order': order,
        'publishable_key': settings.STRIPE_PUBLISHABLE_KEY
    })


# Страницы успеха/отмены
def order_success(request):
    return render(request, 'store/order_success.html')


def order_cancel(request):
    return render(request, 'store/order_cancel.html')
