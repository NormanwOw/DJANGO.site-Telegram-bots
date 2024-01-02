from django.shortcuts import render


def my_orders(request):
    pages = ['1', '2', '3', '4']
    context = {
        'pages': pages,
    }
    return render(request, 'users/my-orders.html', context)
