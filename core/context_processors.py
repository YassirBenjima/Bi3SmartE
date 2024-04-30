from core.models import Category,Address,Vendor

def default(request):
    categories = Category.objects.all()
    vendors = Vendor.objects.all()
    try:
        address = Address.objects.get(user=request.user)
    except:
        address =None
    return {
        'categories' : categories,
        'address':address,
        'vendors':vendors,
    }