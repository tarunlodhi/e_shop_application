from django.urls import path
from .views import Index, SignUp, Login,logout,Cart,CheckOut,OrderView

urlpatterns = [
    path("" ,Index.as_view(),name='homepage'),
    path("signup",SignUp.as_view(),name="signup"),
    path("login",Login.as_view(),name="login"),
    path("logout",logout,name="logout"),
    path("cart",Cart.as_view(),name="cart"),
    path("check-out",CheckOut.as_view(),name="checkout"),
    path("orders",OrderView.as_view(),name="orders")
]
