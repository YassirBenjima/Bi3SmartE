from django.shortcuts import render,redirect
from userauths.forms import UserRegisterForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.conf import settings
# Create your views here.
User = settings.AUTH_USER_MODEL
def register_view(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST or None)
        if form.is_valid():
            newuser = form.save()
            username = form.cleaned_data.get("username")
            messages.success(request,f"Hey {username} , Your Account Was Created Succesfully.")
            newuser = authenticate(
                username=form.cleaned_data['email'],
                password=form.cleaned_data['password1'],                                   
            )
            login(request,newuser)
            return redirect("core:index")
    else :
        form = UserRegisterForm()

    context = {
        'form':form,
    }
    return render(request , "userauths/sign-up.html", context)

def login_view(request):
    if request.user.is_authenticated:
        messages.warning(request,f"Hey you are already logged In.")
        return redirect("core:index")
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        try:
            user = User.objects.get(email=email)
        except:
            messages.warning(request,f"User with {email} does not exist")
        user = authenticate(request, email=email , password=password)
        if user is not None :
            login(request,user)
            messages.success(request,f"Hey You are logged in.")
            return redirect("core:index")
        else:
            messages.warning(request,f"User does not exist. Create an account.")
    context = {
    }
    return render(request, "userauths/sign-in.html", context)

def logout_view(request):
    logout(request)
    messages.success(request,f"You logged out.")
    return redirect("userauths:sign-in")