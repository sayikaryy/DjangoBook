from django.shortcuts import render, get_object_or_404
from .models import Book, Category
from rest_framework import viewsets
from .models import Category
from .serializers import CategorySerializer, BookSerializer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer   
def home(request):
    books = Book.objects.all()
    categories = Category.objects.all()

    search = request.GET.get('search')
    category_id = request.GET.get('category')
    if search:
        books = books.filter(title__icontains=search)
    if category_id:
        books = books.filter(category_id=category_id)

    return render(request, 'BookAPI/home.html', {
        'books': books,
        'categories': categories,
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    return render(request, 'BookAPI/book_detail.html', {'book': book})
