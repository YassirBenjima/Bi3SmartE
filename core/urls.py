from django.urls import path
from core.views import index,chat,update_item_from_cart,delete_item_from_cart,cart_view,add_to_cart,filter_product,search_view,ajax_add_review,tag_list,product_list_view,category_list_view,category_product_list_view, vendor_detail_view,vendor_list_view,product_detail_view
app_name= "core"

urlpatterns = [
    #chatbot
    path('chat/', chat, name='chat'),

    #HomePage
    path("",index , name="index"),
    #Product
    path("products/" , product_list_view , name="product_list"),
    path("product/<p_id>/" , product_detail_view , name="product_detail"),
    #category
    path("category/" , category_list_view , name="category_list"),
    path("category/<C_id>/" , category_product_list_view , name="category_product_list"),
    #Vendor
    path("vendors/", vendor_list_view,name="vendors-list"),
    path("vendor/<v_id>/" , vendor_detail_view , name="vendor-list"),
    #Tags
    path("products/tag/<slug:tag_slug>/" , tag_list , name="tag"),
    #Review
    path("ajax-add-review/<p_id>/" , ajax_add_review , name="ajax-add-review"),
    #Search
    path("search/" , search_view , name="search"),
    #Filter
    path("filter-products/" , filter_product , name="filter-product"),
    #Add To Cart
    path("add-to-cart/" , add_to_cart , name="add-to-cart" ),
    #Cart PAGE
    path('cart/', cart_view, name='cart'),
    #Delete Product From Cart
    path('delete-item-from-cart/', delete_item_from_cart, name='delete-item-from-cart'),
    #Update Product From Cart
    path('update-item-from-cart/', update_item_from_cart, name='update-item-from-cart'),
]

