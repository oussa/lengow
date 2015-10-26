from django.db.models import Q
from django.shortcuts import render, redirect

from .models import Order
from .utils import json_response, parse_url


def index(request):
    if request.method == 'GET':
        latest_orders = Order.objects.order_by('id')[:15]
        return render(request, 'orders/orders.html', {'latest_orders': latest_orders})
    elif request.method == 'POST':
        result = parse_url(request)
        if result['success']:
            for order in result['orders_to_save']:
                order.save()
            latest_orders = Order.objects.order_by('id')[:15]
            return render(request, 'orders/orders.html', {'latest_orders': latest_orders,
                                                          'saved': len(result['orders_to_save']),
                                                          'skipped': len(result['orders_invalid']
                                                                         )})
            # return json_response({'saved': len(result['orders_to_save']), 'skipped': len(result['orders_invalid'])})
        else:
            latest_orders = Order.objects.order_by('id')[:15]
            return render(request, 'orders/orders.html', {'latest_orders': latest_orders,
                                                          'error': result['data']
                                                          })
            # return json_response(result['data'], 400)
    else:
        latest_orders = Order.objects.order_by('id')[:15]
        return render(request, 'orders/orders.html', {'latest_orders': latest_orders})
        # json_response('forbidden', 403)


def search(request):
    if 'q' in request.GET:
        querystring = request.GET.get('q').strip()
        if len(querystring) == 0:
            return redirect('/search/')

        results = Order.objects.filter(Q(marketplace__icontains=querystring) |
                                       Q(order_purchase_date__icontains=querystring) |
                                       Q(order_purchase_heure__icontains=querystring) |
                                       Q(order_amount=querystring))
        count = results.count()

        return render(request, 'orders/search.html', {
            'hide_search': True,
            'querystring': querystring,
            'count': count,
            'results': results,
        })
    else:
        return render(request, 'orders/search.html', {'hide_search': True})