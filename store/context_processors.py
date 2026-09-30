from .cart import Cart
def cart_count(request):
    return {'cart_item_count':len(Cart(request))}
