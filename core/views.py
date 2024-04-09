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