from django.shortcuts import render, get_object_or_404
from django.db.models import Count,Avg
from django.http import HttpResponse
from taggit.models import Tag
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
    products = Product.objects.filter(category = product.category).exclude(p_id=p_id)
    
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    avrage_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    total_five_reviews = ProductReview.objects.filter(rating=5).count()
    total_four_reviews = ProductReview.objects.filter(rating=4).count()
    total_tree_reviews = ProductReview.objects.filter(rating=3).count()
    total_two_reviews = ProductReview.objects.filter(rating=2).count()
    total_one_reviews = ProductReview.objects.filter(rating=1).count()
    p_image = product.p_images.all()
    context = {
        "product":product,
        "p_image":p_image,
        "reviews" : reviews,
        "avrage_rating": avrage_rating,
        "total_five_reviews" :total_five_reviews,
        "total_four_reviews":total_four_reviews,                
        "total_tree_reviews":total_tree_reviews,
        "total_two_reviews":total_two_reviews,
        "total_one_reviews":total_one_reviews,
        "products":products,
    }
    return render(request,'core/product-detail.html',context)

def tag_list (request , tag_slug=None):
    products = Product.objects.filter(product_status="published").order_by("-id")
    tag = None
    if tag_slug : 
        tag = get_object_or_404(Tag, slug=tag_slug)
        products = products.filter(tags__in=[tag])
    context = {
        "products":products,
        "tag":tag,
    }
    return render(request,'core/tags.html',context)