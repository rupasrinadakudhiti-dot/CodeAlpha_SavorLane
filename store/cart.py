from decimal import Decimal
from .models import Product

class Cart:
    def __init__(self,request):
        self.session=request.session
        self.cart=self.session.setdefault('cart',{})
    def add(self,product,quantity=1,override=False):
        pid=str(product.id)
        if pid not in self.cart: self.cart[pid]={'quantity':0}
        new_quantity=quantity if override else self.cart[pid]['quantity']+quantity
        self.cart[pid]['quantity']=min(new_quantity,product.stock)
        if self.cart[pid]['quantity']<=0: self.cart.pop(pid,None)
        self.save()
    def remove(self,product):
        self.cart.pop(str(product.id),None); self.save()
    def save(self): self.session.modified=True
    def clear(self): self.session['cart']={}; self.cart=self.session['cart']; self.save()
    def __len__(self): return sum(i['quantity'] for i in self)
    def __iter__(self):
        products=Product.objects.filter(id__in=self.cart.keys(),is_active=True)
        lookup={str(p.id):p for p in products}
        for pid,item in self.cart.items():
            product=lookup.get(pid)
            if not product: continue
            row=item.copy(); row['product']=product; row['price']=product.price; row['total_price']=product.price*row['quantity']; yield row
    def total(self): return sum((i['total_price'] for i in self),Decimal('0'))
