from django.shortcuts import render, redirect
from books.models import Book
from datetime import datetime
from django.core.paginator import Paginator, Page
from django.db.models import Count

class PaginatorExtension(Paginator):
    def _get_page(self, *args, **kwargs):
        """
        Return an instance of a single page.

        This hook can be used by subclasses to use an alternative to the
        standard :cls:`Page` object.
        """
        return PageExtension(*args, **kwargs)

class PageExtension(Page):
    
    def next_page_value(self):
        if self.has_next():
            return self.paginator.object_list[self.next_page_number()-1]
        
        return None
    
    def previous_page_value(self):
        if self.has_previous():
            return self.paginator.object_list[self.previous_page_number()-1]
            
        return None
    

def find_page_num(list_ : list, to_find : datetime.date):
    i = 1
    for date in list_:
        if date == to_find:
            return i
        i += 1
        
    return 0 

def index(request):
    return redirect('books')

def books_view(request):
    template = 'books/books_list.html'
    books_list = Book.objects.all()
    context = {
        'books_list':books_list
    }
    return render(request, template, context)

def books_view_by_date(request,pub_date):
    template = 'books/books_list.html'
    books_list = Book.objects.filter(pub_date=pub_date)
    books_pub_date_list = [ d['pub_date'] for d in Book.objects.values('pub_date').annotate(dcount=Count('pub_date')).order_by()]
    
    pagi = PaginatorExtension(books_pub_date_list,1)
    page_num = find_page_num(books_pub_date_list,datetime.date(pub_date))
    page_obj = pagi.get_page(page_num)
    
    context = {
        'books_list':books_list,
        'books_pub_date_list':books_pub_date_list,
        'page':page_obj,
        'page_num':page_num
    }
    return render(request, template, context)
    