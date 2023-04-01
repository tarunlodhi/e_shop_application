from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from .models import Product, Catagories, Customer, Order
from django.contrib.auth.hashers import make_password, check_password
from .middlewares.auth import auth_middleware
from django.utils.decorators import method_decorator


class Index(View):
    def get(self, request):
        cart = request.session.get("cart")
        if not cart:
            request.session['cart'] = {}
        products = None
        catagories = Catagories.get_all_catagories()
        catagoriesID = request.GET.get('catagory')
        if catagoriesID:
            products = Product.get_product_by_id(catagoriesID)
        else:
            products = Product.get_all_products()
        data = {}
        data['products'] = products
        data['catagories'] = catagories
        print("you are :", request.session.get('email'))
        return render(request, 'index.html', data)

    def post(self, request):
        product = request.POST.get("product")
        remove = request.POST.get("remove")
        cart = request.session.get("cart")
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity-1
                else:
                    cart[product] = quantity+1
            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1
        request.session["cart"] = cart
        print("cart :", request.session["cart"])
        return redirect("homepage")


class SignUp(View):
    def get(self, request):
        return render(request, "signup.html")

    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        password2 = postData.get('password2')

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email,
        }
        error_message = None
        customer = Customer(first_name=first_name,
                            last_name=last_name,
                            phone=phone,
                            email=email,
                            password=password)

        error_message = self.validate(customer, password2)

        # saving
        if not error_message:
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('homepage')
        else:
            data = {'error': error_message, 'values': value}
            return render(request, 'signup.html', data)

    def validate(self, customer, password2):
        error_message = None
        if (not customer.first_name):
            error_message = "First Name Required !!"
        elif len(customer.first_name) < 4:
            error_message = 'First Name must be 4 char long or more'
        elif not customer.last_name:
            error_message = 'Last Name Required'
        elif len(customer.last_name) < 4:
            error_message = 'Last Name must be 4 char long or more'
        elif not customer.phone:
            error_message = 'Phone Number required'
        elif len(customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len(customer.password) < 6:
            error_message = 'Password must be 6 char long'
        elif len(customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists():
            error_message = 'Email Address Already Registered..'
        elif customer.password != password2:
            error_message = 'Password Doesnt Match.....'
        return error_message


class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, "login.html")

    def post(self, request):
        email = request.POST.get("email")
        password = request.POST.get("password")
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            verify = check_password(password, customer.password)
            if verify:
                # adding session to the file
                request.session['customer'] = customer.id  # type: ignore
                request.session['email'] = customer.email

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = "Email and Password Doesn't Match"
        else:
            error_message = "Invalid Email"
            return render(request, "login.html", {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class CheckOut(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_product_by_ids(list(cart.keys()))
        for product in products:
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))  # type: ignore
            order.placeOrder()
        request.session['cart'] = {}
        return redirect('cart')


class Cart(View):
    def get(self, request):
        ids = request.session.get("cart").keys()
        products = Product.get_product_by_ids(ids)
        return render(request, "cart.html", {"products": products})


class OrderView(View):
    @method_decorator(auth_middleware)
    def get(self, request):
        customer = request.session.get("customer")
        orders = Order.get_orders_by_customer(customer)
        return render(request, 'orders.html', {"orders": orders})
