from django.shortcuts import render, get_object_or_404,redirect
from django.db.models import Count,Avg
from django.http import HttpResponse,JsonResponse
from taggit.models import Tag
from core.models import Product,Category,Vendor,CartOrder,CartOrderItems,ProductImages,ProductReview,Wishlist,Address
from core.forms import ProductReviewForm
from django.template.loader import render_to_string
from django.contrib import messages
import google.generativeai as genai


def chat(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        # Configure generative AI
        GOOGLE_API_KEY = 'AIzaSyBkeHKZEaz-5N0c3S1B1pU3nw5b4pgeWWM'
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(prompt)
        result = ''.join([p.text for p in response.candidates[0].content.parts])
        return render(request, 'core/chat.html', {'prompt': prompt, 'result': result})
    return render(request, 'core/chat.html', {})

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
    # Initialiser un dictionnaire vide pour contenir les informations sur le produit à ajouter au panier
    cart_product = {}
    # Remplir le dictionnaire cart_product avec les informations sur le produit à partir de la requête GET
    cart_product[str(request.GET['id'])] = {
        'title': request.GET['title'],
        'qty': request.GET['qty'],
        'price': request.GET['price'],
        'image': request.GET['image'],
        'p_id': request.GET['p_id'],
    }
    # Vérifier si 'cart_data_obj' existe dans la session
    if 'cart_data_obj' in request.session:
        # Vérifier si l'identifiant du produit existe déjà dans les données du panier
        if str(request.GET['id']) in request.session['cart_data_obj']:
            # Si l'identifiant du produit existe, mettre à jour la quantité du produit existant dans le panier
            cart_data = request.session['cart_data_obj']
            cart_data[str(request.GET['id'])]['qty'] = int(cart_product[str(request.GET['id'])]['qty'])
            request.session['cart_data_obj'] = cart_data
        else:
            # Si l'identifiant du produit n'existe pas, ajouter le nouveau produit aux données du panier
            cart_data = request.session['cart_data_obj']
            cart_data.update(cart_product)
            request.session['cart_data_obj'] = cart_data
    else:
        # Si 'cart_data_obj' n'existe pas dans la session, le créer et ajouter le produit
        request.session['cart_data_obj'] = cart_product
    # Retourner une réponse JSON contenant les données du panier mises à jour et le nombre total d'articles dans le panier
    return JsonResponse({"data": request.session['cart_data_obj'], 'TotalCartItem': len(request.session['cart_data_obj'])})

def cart_view(request):
    cart_total_amount = 0  # Initialiser le montant total du panier
    
    if 'cart_data_obj' in request.session:  # Vérifier si 'cart_data_obj' existe dans la session
        for p_id, item in request.session['cart_data_obj'].items():  # Itérer sur les articles dans les données du panier
            # Calculer le montant total pour chaque article dans le panier
            cart_total_amount += int(item['qty']) * float(item['price'])
        
        # Rendre le template du panier avec les données du panier, le nombre total d'articles et le montant total du panier
        return render(request, "core/cart.html", {
            "cart_data": request.session['cart_data_obj'],
            'TotalCartItem': len(request.session['cart_data_obj']),
            'cart_total_amount': cart_total_amount
        })
    else:
        # Afficher un message d'avertissement si le panier est vide et rediriger vers la page d'accueil
        messages.warning(request, "Your Cart Is Empty")
        return redirect("core:index")

def delete_item_from_cart(request):
    product_id = str(request.GET['id'])  # Récupérer l'identifiant du produit depuis la requête
    
    if 'cart_data_obj' in request.session:  # Vérifier si 'cart_data_obj' existe dans la session
        if product_id in request.session['cart_data_obj']:  # Vérifier si l'identifiant du produit existe dans les données du panier
            cart_data = request.session['cart_data_obj']  # Récupérer les données du panier depuis la session
            del request.session['cart_data_obj'][product_id]  # Supprimer le produit des données du panier
            # Déplacer l'assignation des données du panier en dehors du bloc if interne
            request.session['cart_data_obj'] = cart_data
        
    cart_total_amount = 0  # Initialiser le montant total du panier
    
    if 'cart_data_obj' in request.session:  # Vérifier si 'cart_data_obj' existe toujours dans la session
        for p_id, item in request.session['cart_data_obj'].items():  # Parcourir les articles dans les données du panier
            # Calculer le montant total pour chaque article dans le panier
            cart_total_amount += int(item['qty']) * float(item['price'])
    
    # Rendre le template de la liste de panier mis à jour avec les données du panier modifiées et le montant total du panier
    context = render_to_string("core/async/cart-list.html", {
        "cart_data": request.session['cart_data_obj'],
        'TotalCartItem': len(request.session['cart_data_obj']),
        'cart_total_amount': cart_total_amount
    })
    
    # Retourner les données du panier mises à jour et le nombre total d'articles au format JSON
    return JsonResponse({"data": context, 'TotalCartItem': len(request.session['cart_data_obj'])})

def update_item_from_cart(request):
    # Extrait l'identifiant du produit et la quantité de la requête
    product_id = str(request.GET.get('id', ''))
    product_qty = request.GET.get('qty', '')

    # Vérifie si les données du panier existent dans la session
    if 'cart_data_obj' in request.session:
        cart_data = request.session['cart_data_obj']

        # Vérifie si le produit existe dans le panier
        if product_id in cart_data:
            # Met à jour la quantité du produit
            cart_data[product_id]['qty'] = product_qty
            request.session['cart_data_obj'] = cart_data

    # Calcule le montant total du panier
    cart_total_amount = 0 
    if 'cart_data_obj' in request.session:
        for p_id, item in request.session['cart_data_obj'].items():
            cart_total_amount += int(item.get('qty', 0)) * float(item.get('price', 0))

    # Rendu du HTML du panier mis à jour
    context = render_to_string("core/async/cart-list.html", {
        "cart_data": request.session.get('cart_data_obj', {}),
        'TotalCartItem': len(request.session.get('cart_data_obj', {})),
        'cart_total_amount': cart_total_amount
    })

    # Retourne une réponse JSON
    return JsonResponse({"data": context, 'TotalCartItem': len(request.session.get('cart_data_obj', {}))})

