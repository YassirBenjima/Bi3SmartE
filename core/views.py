from django.shortcuts import render
from django.http import HttpResponse
from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,ProductReview,Wishlist,Address
# Create your views here.
def index(request):
    # product = Product.objects.all()
    product = Product.objects.filter(product_status="published" , featured=True)
    category = Category.objects.all()
    context = {
        "products":product,
        "categories":category,
    }
    return render(request,'core/index.html',context)

def product_list_view(request):
    product = Product.objects.filter(product_status="published")
    context = {
        "products":product,
    }
    return render(request,'core/product-list.html',context) 

def category_list_view(request):
    categories = Category.objects.all()
    context = {
        "categories":categories,
    }
    return render(request,'core/category-list.html',context) 

def category_product_list_view(request,C_id):
    category = Category.objects.get(C_id=C_id)
    products = Product.objects.filter(product_status="published" , category=category)
    context = {
        "category":category,
        "products":products,
    }
    return render(request,"core/category-product-list.html",context)