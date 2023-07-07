from typing import Any, Dict
from django.db.models.query import QuerySet
from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,ListView,DetailView
from store.models import Product
from .models import Cart,Order
from django.contrib import messages
from django.db.models import Sum
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

#auth_decorator

def signin_required(fn):
    def inner(request,*args,**kwargs):
        if request.user.is_authenticated:
            return fn(request,*args,**kwargs)
        else:
            messages.error(request,"Please Login First!!")
            return redirect("log")
    return inner

dec=[signin_required,never_cache]

# Create your views here.

@method_decorator(dec,name="dispatch")
class CustHomeView(ListView):
    template_name="cust-home.html"
    model=Product
    context_object_name="data"
    
# class CustHomeView(TemplateView):
#     template_name="cust-home.html"
#     # def get(self,request):
#     #     return render(request,"cust-home.html")
    
#     def get_context_data(self, **kwargs):
#         context=super().get_context_data(**kwargs)
#         context["data"]=Product.objects.all()
#         return context
 
@method_decorator(dec,name="dispatch")   
class ProductDetailView(DetailView):
    template_name="product-details.html"
    model=Product
    context_object_name="product"
    pk_url_kwarg="pid"

# class ProductDetailView(TemplateView):
#     template_name="product-details.html"

@method_decorator(dec,name="dispatch")
class AddCart(View):
    def get(self,request,*args,**kwargs):
        prod=Product.objects.get(id=kwargs.get("id"))
        user=request.user
        Cart.objects.create(product=prod,user=user)
        messages.success(request,'Product added to cart!!')
        return redirect("home")
    
@method_decorator(dec,name="dispatch")
class CartListView(ListView):
    template_name="cart-list.html"
    model=Cart  
    context_object_name="cartitem"
    
    # def get_queryset(self):
    #     return Cart.objects.filter(user=self.request.user)
    
    def get_queryset(self):
        cart=Cart.objects.filter(user=self.request.user,status="cart")
        total=Cart.objects.filter(user=self.request.user,status="cart").aggregate(tot=Sum("product__price"))
        return ({'items':cart,"total":total})
        

# class DeleteCart(View):
#     def get(self,request,*args,**kwargs):
#         id=kwargs.get("mid")
#         car=Cart.objects.get(id=id)
#         car.delete()
#         return redirect("vcart")  
  
dec
def deletecartitem(request,id):
    cart=Cart.objects.get(id=id)
    cart.delete()
    messages.error(request,"Cart Item removed!!")
    return redirect("vcart")


@method_decorator(dec,name="dispatch")
class CheckoutView(View):
    def get(self,request,*args,**kwargs):
        return render(request,"checkout.html")
    def post(self,request,*args,**kwargs):
        id=kwargs.get("cid")
        cart=Cart.objects.get(id=id)
        prod=cart.product
        user=request.user
        address=request.POST.get("address")
        phone=request.POST.get("phone")
        Order.objects.create(product=prod,user=user,address=address,phone=phone)
        cart.status="Order Placed"
        cart.save()
        messages.success(request,"Order Placed Successfully!!")
        return redirect("home")
     
@method_decorator(dec,name="dispatch")        
class OrderListView(ListView):
    template_name="order-list.html"
    model=Order  
    context_object_name="orderitem"
    
    def get_queryset(self):
        order=Order.objects.filter(user=self.request.user)
        return ({"item":order})

dec
def deleteorderitem(request,id):
    order=Order.objects.get(id=id)
    order.status="Cancel Your Order"
    order.save()
    messages.error(request,"Order Cancelled!!")
    return redirect("vorder")