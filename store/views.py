import stripe
from django.conf import settings
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from .models import Item

stripe.api_key = settings.STRIPE_SECRET_KEY

def item_page(request, item_id):
    item = get_object_or_404(Item, id=item_id)
    return render(request, 'store/item_page.html', {'item': item})

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
        success_url='http://127.0.0.1:8000',
        cancel_url='http://127.0.0.1:8000',
    )

    return JsonResponse({'id': session.id})
