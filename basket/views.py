from django.shortcuts import render
from django.http import JsonResponse
from store.models import Product
from django.shortcuts import get_object_or_404
from .basket import Basket
# from django.contrib.sessions.models import Session


def basket_summary(request):
    basket = Basket(request)
    return render(request, 'store/basket/summary.html', {'basket': basket})


def basket_add(request):
    basket = Basket(request)
    if request.method == 'POST':
        product_id = int(request.POST.get('productid'))
        product_qty = int(request.POST.get('productqty'))
        print(product_id, '🌹🌹🌹🌹🌹')
        product = get_object_or_404(Product, pk=product_id)
        print(product, '🌹🌹🌹🌹🌹')
        basket.add(product, product_qty)
        bastketqty = basket.__len__()
        response = JsonResponse({'qty': bastketqty})
        return response


def basket_delete(request):
    basket = Basket(request)
    if request.method == 'POST':
        product_id = request.POST.get('productid')
        basket.delete(product_id)

        sub_total = basket.get_total_price()
        qty = basket.__len__()
        response = JsonResponse({'sub_total': sub_total, 'qty': qty})
        return response


def basket_update(request):
    basket = Basket(request)
    if request.method == 'POST':
        product_id = request.POST.get('productid')
        product_qty = request.POST.get('productqty')
        basket.update(product_id, product_qty)

        sub_total = basket.get_total_price()
        qty = basket.__len__()
        response = JsonResponse({'sub_total': sub_total, 'qty': qty})
        return response
