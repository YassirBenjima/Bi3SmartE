from django.db import models
from shortuuid.django_fields import ShortUUIDField
from django.utils.html import mark_safe
from userauths.models import User

STATUS_CHOICE=(
    ("Process", "Processing"),
    ("shipped", "Shipped"),
    ("delivered" , "Delivered"),
)
STATUS=(
    ("draft", "Draft"),
    ("disabled", "Disabled"),
    ("rejected" , "Rejected"),
    ("in_review" , "In Review"),
    ("published" , "Published"),
)
RATING=(
    (1,"★✩✩✩✩"),
    (2,"★★✩✩✩"),
    (3,"★★★✩✩"),
    (4,"★★★★✩"),
    (5,"★★★★★"),
)

def user_directory_path(instance,filename):
    return 'user_{0}/{1}'.format(instance.user.id, filename)    
    
############################################# Category ###########################################################################
############################################# Category ###########################################################################
############################################# Category ###########################################################################

class Category(models.Model):
    C_id= ShortUUIDField(unique=True, length=10, max_length=20,prefix="cat",alphabet="abcdefghijklmnop123456789")
    title = models.CharField(max_length=100,default="Title Category")
    image = models.ImageField(upload_to="category", default="category.jpg")
    class Meta:
        verbose_name_plural = "Categories"
    def category_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))
    def __str__(self):
        return self.title 
    
############################################# Tags ##############################################################################
############################################# Tags ##############################################################################
############################################# Tags ##############################################################################
    
class Tags(models.Model):    
    pass     

############################################# Vendor ############################################################################
############################################# Vendor ############################################################################
############################################# Vendor ############################################################################

class Vendor(models.Model):
    v_id= ShortUUIDField(unique=True, length=10, max_length=20,prefix="ven",alphabet="abcdefghijklmnop123456789")
    title = models.CharField(max_length=100, default="Title Vendor")
    image = models.ImageField(upload_to=user_directory_path , default="vendor.jpg")
    description = models.TextField(null=True, blank=True , default="This is the vendor")
    address = models.CharField(max_length=100, default="Main Street,Marrakech")
    contact = models.CharField(max_length=100, default="+212 659 394 401")
    chat_resp_time = models.CharField(max_length=100, default="100")
    shipping_on_time = models.CharField(max_length=100, default="100")
    authentic_rating = models.CharField(max_length=100, default="100")
    days_return = models.CharField(max_length=100, default="100")
    warranty_period = models.CharField(max_length=100, default="100")

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True,null=True , blank=True)
    
    class Meta:
        verbose_name_plural = "Vendors"
    def vendor_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))
    def __str__(self):
        return self.title 

############################################# Product ###########################################################################
############################################# Product ###########################################################################
############################################# Product ###########################################################################

class Product(models.Model):
    p_id= ShortUUIDField(unique=True, length=10, max_length=20,alphabet="abcdefghijklmnop123456789")
    title = models.CharField(max_length=100, default="Title Product")
    image = models.ImageField(upload_to=user_directory_path , default="product.jpg")
    description = models.TextField(null=True, blank=True , default="This is the product")
    price = models.DecimalField(max_digits=10,decimal_places=2,default="1.99")
    old_price = models.DecimalField(max_digits=10,decimal_places=2, default="2.99")
    specefications = models.TextField(null=True, blank=True)
    # tags = models.ForeignKey(Tags, on_delete=models.SET_NULL, null=True)
    product_status = models.CharField(choices=STATUS, max_length=10, default="in_review")
    status = models.BooleanField(default=True)
    in_stock  = models.BooleanField(default=True)
    featured  = models.BooleanField(default=False)
    digital  = models.BooleanField(default=False)

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True,related_name="category")
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True , related_name="vendor")
    sku = ShortUUIDField(unique=True, length=4, max_length=20,prefix="sku",alphabet="123456789")
    date = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(null=True , blank=True)
    
    class Meta:
        verbose_name_plural = "Products"
    def product_image(self):
        return mark_safe('<img src="%s" width="50" height="50">' % (self.image.url))
    def __str__(self):
        return self.title
    def get_precentage(self):
        new_price = (( self.old_price - self.price) / self.old_price)*100
        return new_price

############################################# ProductImages ######################################################################
############################################# ProductImages ######################################################################
############################################# ProductImages ######################################################################

class ProductImages(models.Model):
    images = models.ImageField(upload_to="product-image", default="product.jpg")
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Product Images"
        
############################################# CartOrder ##########################################################################
############################################# CartOrder ##########################################################################
############################################# CartOrder ##########################################################################

class CartOrder(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.DecimalField(max_digits=10,decimal_places=2,default="1.99")
    paid_status = models.BooleanField(default=False)
    order_date = models.DateTimeField(auto_now_add=True)
    product_status = models.CharField(choices = STATUS_CHOICE , max_length=30 , default="processing")
    class Meta:
        verbose_name_plural = "Cart Order"

############################################# CartOrderItems #####################################################################
############################################# CartOrderItems #####################################################################
############################################# CartOrderItems #####################################################################

class CartOrderItems(models.Model):
    order = models.ForeignKey(CartOrder, on_delete=models.SET_NULL, null=True)
    invoice_no = models.CharField(max_length=200)
    product_status = models.CharField(max_length=200)
    item = models.CharField(max_length=200)
    image= models.CharField(max_length=200)
    qty = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10,decimal_places=2,default="1.99")
    total = models.DecimalField(max_digits=10,decimal_places=2,default="1.99")

    class Meta:
        verbose_name_plural = "Cart Order Items"
    def order_image(self):
        return mark_safe('<img src="/media/%s" width="50" height="50">' % (self.image))

############################################# ProductReview ######################################################################
############################################# ProductReview ######################################################################
############################################# ProductReview ######################################################################

class ProductReview(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    review = models.TextField()
    rating = models.IntegerField(choices=RATING,default=None)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Product Reviews"
    def __str__(self):
        return self.product.title
    def get_rating(self):
        return self.rating
        
############################################# Wishlist ###########################################################################
############################################# Wishlist ###########################################################################
############################################# Wishlist ###########################################################################

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    class Meta:
        verbose_name_plural = "Wishlists"
    def __str__(self):
        return self.product.title

############################################# Address ############################################################################
############################################# Address ############################################################################
############################################# Address ############################################################################

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=100, null=True)
    status = models.BooleanField(default=False)
    class Meta:
        verbose_name_plural = "Address"
