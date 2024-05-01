from django.shortcuts import render, get_object_or_404
from django.db.models import Count,Avg
from django.http import HttpResponse,JsonResponse
from taggit.models import Tag
from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,ProductReview,Wishlist,Address
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
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
    p_image = product.p_images.all()
    #Getting all reviews related to a product
    reviews = ProductReview.objects.filter(product=product).order_by("-date")
    #Getting average review 
    avrage_rating = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))

    review_form = ProductReviewForm()
    
    context = {
        "product":product,
        "p_image":p_image,
        "reviews" : reviews,
        "avrage_rating": avrage_rating,
        "review_form":review_form,
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

def ajax_add_review(request,p_id):
    product = Product.objects.get(pk=p_id)
    user = request.user
    review = ProductReview.objects.create(
        user=user,
        product=product,
        review = request.POST['review'],
        rating = request.POST['rating'],
    )
    context = {
       'user': user.username,
       'review': request.POST['review'],
       'rating': request.POST['rating'],
    }
    avrage_reviews = ProductReview.objects.filter(product=product).aggregate(rating=Avg('rating'))
    return JsonResponse(
        {
            'bool' : True,
            'context':context,
            'avrage_reviews':avrage_reviews,
        }
    )
    
def search_view(request):
    query = request.GET.get("q")
    products = Product.objects.filter(title__icontains=query,description__icontains=query).order_by("-date")
    context = {
        "products":products,
        "query":query,
    }
    return render(request,"core/search.html",context)

def filter_product(request):
    categories = request.GET.getlist("category[]")
    vendors = request.GET.getlist("vendor[]")
    products = Product.objects.filter(product_status="published").order_by("-id").distinct()
    if len(categories) > 0 :
        products = products.filter(category__id__in = categories).distinct()
        
    if len(vendors) > 0:
        products = products.filter(vendor__id__in = vendors).distinct()

    data =  render_to_string("core/async/product-list.html", {"products": products })
    return JsonResponse({"data":data})

def add_to_cart(request):
    # Initialize an empty dictionary to hold information about the product to be added to the cart
    cart_product = {}
    # Populate the cart_product dictionary with information about the product from the GET request
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'p_id': request.GET['p_id'],

    }
    # Check if 'cart_data_obj' exists in the session
    if 'cart_data_obj' in request.session:
        # Check if the product ID already exists in the cart data
        if str(request.GET['id']) in request.session['cart_data_obj']:
            # If the product ID exists, update the quantity of the existing product in the cart
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            cart_data.update(cart_data)  # This line seems redundant or incorrect
            request.session['cart_data_obj'] = cart_data
        else:
            # If the product ID does not exist, add the new product to the cart data
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        # If 'cart_data_obj' does not exist in the session, create it and add the product
        request.session['cart_data_obj'] = cart_product
    # Return JSON response containing updated cart data and total number of items in the cart
    return JsonResponse({"data": request.session['cart_data_obj'], 'TotalCartItem': len(request.session['cart_data_obj'])})

