from django.shortcuts import render, redirect, get_object_or_404
from .models import Flora, Cart, CartItem, Order, OrderItem ,SupportComment
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.utils import timezone 



# -------------------------------------------------------------------------------------------------------------------------- 


# FOR HOME PAGE -->>
def home(request):
    return render(request,'home.html') 

# -------------------------------------------------------------------------------------------------------------------------- 


# FOR SHOW PAGE -->>
@login_required
def show(request):
    data=Flora.objects.all()
    context={'data':data}
    return render(request,'show.html',context)

# FOR LOGIN PAGE -->> 
#  with authentication
# def login_view(request):
#     if request.method=="POST":
#         un=request.POST.get('username')
#         password=request.POST.get('password')
#         user = authenticate(request,username=un,password=password)
#         if user is not None:
#             return redirect('show')
#         else:
#             return render(request,'login.html',{'error':'User NOt Found ...Please Register'}) 
#     return render(request,'login.html')  here i want user and 

# -------------------------------------------------------------------------------------------------------------------------- 


def login_view(request):
    if request.method == "POST":
        un = request.POST.get("username")
        password = request.POST.get("password")

        try:
            user_obj = User.objects.get(username=un)
        except User.DoesNotExist:
            return render(request, "login.html", {"error": "❌ Username does not exist!"})

        # Step 2: Check password manually
        if not check_password(password, user_obj.password):
            return render(request, "login.html", {"error": "❌ Wrong password!"})

        # Step 3: If password correct, log in user
        login(request, user_obj)
        return redirect("show")

    return render(request, "login.html")

# -------------------------------------------------------------------------------------------------------------------------- 


# FOR REGISTER PAGE -->> 
def register_view(request):
    if request.method=="POST":
        uname=request.POST.get('username')
        email=request.POST.get('email')
        password=request.POST.get('password')
        # IF USER ALREADY EXISTS
        if User.objects.filter(username=uname).exists():
            return render(request,'register.html' , {'error':'This account already exists !!'})
        else:
            #  OR CREATE NEW ACCOUNT
            User.objects.create_user(username=uname,email=email,password=password)
            return redirect('login')
    return render(request,'register.html',{'message':'Register Successfully..😃'})

# -------------------------------------------------------------------------------------------------------------------------- 

# FOR ADD PAGE -->> 
@login_required
def add_view(request):
    if request.method == "POST":
        f_name = request.POST.get('f_name')
        f_description = request.POST.get('f_description')   
        f_price = request.POST.get('f_price')
        f_category = request.POST.get('f_category')
        f_scientific_name = request.POST.get('f_scientific_name')
        f_color = request.POST.get('f_color')
        f_image = request.FILES.get('f_image')

        # ORM command 
        obj = Flora(
            f_name=f_name,
            f_description=f_description,   
            f_price=f_price,
            f_category=f_category,
            f_scientific_name=f_scientific_name,
            f_color=f_color,
            f_image=f_image
        )
        obj.save()
        return redirect("show")  
    else:
        return render(request, 'add.html')
    
# -------------------------------------------------------------------------------------------------------------------------- 

# FOR FEATURES PAGE -->>
@login_required
def features(request):
    return render(request, 'features.html')

# -------------------------------------------------------------------------------------------------------------------------- 

# FOR EDIT PAGE -->>>

def edit(request, id):
    obj = Flora.objects.get(id=id)
    if request.method == "POST":
        f_name = request.POST.get('f_name')
        f_description = request.POST.get('f_description')   
        f_price = request.POST.get('f_price')
        f_category = request.POST.get('f_category')
        f_scientific_name = request.POST.get('f_scientific_name')
        f_color = request.POST.get('f_color')
        f_image = request.FILES.get('f_image')
        obj.f_name=f_name
        obj.f_description=f_description
        obj.f_price=f_price
        obj.f_category=f_category
        obj.f_scientific_name=f_scientific_name
        obj.f_category=f_category
        obj.f_color=f_color
        obj.f_image=f_image
        obj.save()
        return redirect("show")
    else:
        return render(request, 'edit.html',{'data' :obj})
# -------------------------------------------------------------------------------------------------------------------------- 
# DELETE -->>


def delete(request,id):
    obj = Flora.objects.get(id=id)
    obj.delete()
    return redirect("show")

# -------------------------------------------------------------------------------------------------------------------------- 

# SEARCH -->> 
@login_required
def search(request):
    query = request.GET.get("search", "")
    data = []

    if query:  # if user typed something
        data = Flora.objects.filter(
            Q(f_category__icontains=query) |
            Q(f_name__icontains=query) |
            Q(f_scientific_name__icontains=query) |
            Q(f_color__icontains=query)
        )

    return render(request, "search.html", {"data": data, "query": query})

# -------------------------------------------------------------------------------------------------------------------------- 


# LOGOUT -->> 
def logout_view(request):
    logout(request)
    return redirect('home')

# -------------------------------------------------------------------------------------------------------------------------- 

#  CART -->

@login_required
def add_to_cart(request, product_id):
    product = get_object_or_404(Flora, id=product_id)

    # Get or create a cart for the user
    cart, created = Cart.objects.get_or_create(user=request.user)

    # Check if product already in cart
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

    if not created:
        cart_item.quantity += 1  # increase quantity
    cart_item.save()

    return redirect("cart")
# ---------------------------------------------------------------

# View cart

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)
    return render(request, "cart.html", {"cart": cart})
# ------------------------------------------------------------


# Remove item from cart

@login_required
def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    return redirect("cart")

# -------------------------------------------------------------------------------------------------------------------------- 

#  ORDER --->>>

@login_required
def checkout(request):
    cart = get_object_or_404(Cart, user=request.user)

    if not cart.items.exists():
        return redirect('cart')  # If cart empty, redirect to cart page

    # Create new Order
    order = Order.objects.create(
        user=request.user,
        total=cart.total_price(),
        created_at=timezone.now()
    )

    # Move CartItems → OrderItems
    for item in cart.items.all():
        OrderItem.objects.create(
            order=order,
            product=item.product,
            quantity=item.quantity,
            price=item.product.f_price
        )

    # Clear Cart
    cart.items.all().delete()

    # Render single template with order details
    return render(request, "checkout.html", {"order": order})

# -------------------------------------------------------------------------------------------------------------------------- 

# QUANTITY -->>

def increase_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.quantity += 1
    cart_item.save()
    return redirect('cart')

def decrease_quantity(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')

# -------------------------------------------------------------------------------------------------------------------------- 

#  SUPPORT --->> 

@login_required
def support_page(request):
    if request.method == "POST":
        message = request.POST.get("message")
        if message:
            SupportComment.objects.create(user=request.user, message=message)
            return redirect("support")  # redirect to clear POST

    comments = SupportComment.objects.all().order_by("-created_at")
    return render(request, "support.html", {"comments": comments})


# -------------------------------------------------------------------------------------------------------------------------- 

#  Order -->>

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'my_orders.html', {'orders': orders})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, "order_detail.html", {"order": order})