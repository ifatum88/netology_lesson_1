from django.shortcuts import render, redirect
from django.urls import reverse
from pagination.settings import BUS_STATION_CSV
import csv
from django.core.paginator import Paginator

def index(request):
    return redirect(reverse('bus_stations'))

def bus_stations(request):
    page_items = 10
    page_number = int(request.GET.get("page",1))
    bus_stations = list()
    
    with open(BUS_STATION_CSV,"r",encoding='utf-8') as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            bus_stations.append({
                "Name":row['Name'],
                "Street":row['Street'],
                "District":row['District']
                })
    
    pagi = Paginator(bus_stations,page_items)
    page = pagi.get_page(page_number)

    context = {
        'bus_stations': page.object_list,
        'page': page,
    }
    return render(request, 'stations/index.html', context)
