from django.urls import path
from .views import *

urlpatterns = [
    path("custh",CustHomeView.as_view(),name="home"),
    path("prod/<int:pid>",ProductDetailView.as_view(),name="pdet"),
    path("acart/<int:id>",AddCart.as_view(),name="acart"),
    path("viecart",CartListView.as_view(),name="vcart"),
    # path("delcar/<int:mid>",DeleteCart.as_view(),name="delcart")
    path("delcart/<int:id>",deletecartitem,name="delcart"),
    path("chkout/<int:cid>",CheckoutView.as_view(),name="checkout"),
    path("ordrlst",OrderListView.as_view(),name="vorder"),
    path("delorder/<int:id>",deleteorderitem,name="delorder"),

]
