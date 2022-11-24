from django.shortcuts import render, redirect
from phones.models import Phone


def index(request):
    return redirect('catalog')


def show_catalog(request):
    template = 'catalog.html'
    sort = request.GET.get('sort')
    phones_list = Phone.objects.all()
    
    match sort:
        case "min_price":
            phones_list = phones_list.order_by('price')
        case "max_price":
            phones_list = phones_list.order_by('price').reverse()
        case _:
            phones_list = phones_list.order_by('name')

    
    context = {
        'phones' : phones_list
    }
    return render(request, template, context)

def show_product(request, slug):
    template = 'product.html'
    phone_item = Phone.objects.filter(slug=slug)
    
    context = {
        'phone':phone_item.first()
    }
    return render(request, template, context)
