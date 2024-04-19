from django.urls import path
from core.views import index,product_list_view,category_list_view,category_product_list_view
app_name= "core"
urlpatterns = [
    path("",index , name="index"),
    path("products/" , product_list_view , name="product_list"),
    path("category/" , category_list_view , name="category_list"),
    path("category/<C_id>/" , category_product_list_view , name="category_product_list"),
]