from django.shortcuts import render


# Create your views here.
def my_orders(request):
    return render(request, 'users/my-orders.html')
