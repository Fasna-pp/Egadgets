from django.urls import path
from .views import *
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken import views

router=DefaultRouter()
router.register("prod",ProductVSet,basename="prod")
router.register("productmv",ProductMVSet,basename="pmv")
router.register("userv",UserVset,basename="us")



# localhost:8000/store/prod/
# localhost:8000/store/productmv/
urlpatterns = [
    path('product',ProductView.as_view()),
    path("product/<int:id>",SpecificProductView.as_view()),
    path("token",views.obtain_auth_token)
    
]+router.urls
