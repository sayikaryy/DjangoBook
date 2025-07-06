from django.shortcuts import render, get_object_or_404
from .models import Book, Category

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
