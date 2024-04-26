from django.urls import path
from core.views import index,product_list_view,category_list_view,category_product_list_view, vendor_detail_view,vendor_list_view,product_detail_view
app_name= "core"
urlpatterns = [
    path("",index , name="index"),
    path("products/" , product_list_view , name="product_list"),
    path("product/<p_id>/" , product_detail_view , name="product_detail"),
    path("category/" , category_list_view , name="category_list"),
    path("category/<C_id>/" , category_product_list_view , name="category_product_list"),
    path("vendors/", vendor_list_view,name="vendors-list"),
    path("vendor/<v_id>/" , vendor_detail_view , name="vendor-list"),
]