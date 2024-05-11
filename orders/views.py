from django.shortcuts import render

from django.shortcuts import render

def create_order(request):
    return render(request, 'orders/create-order.html')
