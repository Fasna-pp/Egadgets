from .models import Cart,Order

def cart_count(request):
    if request.user.is_authenticated:
        cnt=Cart.objects.filter(user=request.user,status="cart").count()
        return {"count":cnt}
    else:
        return {"count":0}
    
def order_count(request):
    if request.user.is_authenticated:
        cnt=Order.objects.filter(user=request.user,status="order").count()
        return {"cont":cnt}
    else:
        return {"cont":0}
    
