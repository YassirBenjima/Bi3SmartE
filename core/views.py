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

def vendor_list_view(request):
    vendors = Vendor.objects.all()
    context = {
        "vendors": vendors,
    }
    return render(request,"core/vendor-list.html",context)

def vendor_detail_view(request,v_id):
    vendor = Vendor.objects.get(v_id=v_id)
    products = Product.objects.filter(vendor=vendor,product_status="published" )
    context = {
        "vendor":vendor,
        "products":products,
    }
    return render(request,"core/vendor-detail.html",context)

def product_detail_view(request,p_id):
    product = Product.objects.get(p_id=p_id)
    p_image = product.p_images.all()
    context = {
        "product":product,
        "p_image":p_image,
    }
    return render(request,'core/product-detail.html',context)