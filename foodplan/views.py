from django.shortcuts import render

def index(request):
    context = {
        'is_index_page': True,
    }
    return render(request, 'index.html', context)

def order(request):
    return render(request, 'order.html', {})
