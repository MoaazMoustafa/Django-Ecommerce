from django.shortcuts import render
from .models import Product, Category
from django.shortcuts import get_object_or_404


def home(request):
    products = Product.products.all()
    return render(request, 'store/home.html', {'products': products})


def product_details(request, slug):
    product = get_object_or_404(Product, slug=slug, in_stock=True)
    return render(request, 'store/products/details.html', {'product': product})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    products = Product.objects.filter(category=category)
    return render(request, 'store/products/category.html', {'category': category, 'products': products})
