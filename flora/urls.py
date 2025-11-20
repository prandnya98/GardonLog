from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),   # Homepage
    path('show/',views.show,name='show'),
    path('login/',views.login_view,name='login'),
    path('register/',views.register_view,name='register'),
    path('add/',views.add_view,name='add'),
    path('features/',views.features,name='features'),
    path('update/<int:id>',views.edit,name='update'),
    path('delete/<int:id>',views.delete,name='delete'),
    path('search/', views.search, name="search"),
    path('logout_view/',views.logout_view,name='logout'),
    path("cart/", views.cart_view, name="cart"),
    path("cart/add/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
    path("cart/remove/<int:item_id>/", views.remove_from_cart, name="remove_from_cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("cart/increase/<int:item_id>/", views.increase_quantity, name="increase_quantity"),
    path("cart/decrease/<int:item_id>/", views.decrease_quantity, name="decrease_quantity"),
    path("support/", views.support_page, name="support"),
    path("my-orders/", views.my_orders, name="my_orders"),
    path("order/<int:order_id>/", views.order_detail, name="order_detail"),
    

]