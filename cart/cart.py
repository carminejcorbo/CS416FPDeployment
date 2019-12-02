"""Cart class will allow us to manage the shopping cart. We store the current session using
self.session=request.session to make it accessible to the other methods of the Cart Class.
If not other cart is present  in the session we create an empty cart by setting an empty
dictionary in the session."""


from decimal import Decimal
from django.conf import settings
from shop.models import Product


class Cart(object):
    def __init__(self, request):
        """Initilaize the cart"""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    """ quantity by default is 1, and update qty boolean indicates if qty needs to be update """
    def add(self, product, quantity=1, update_quantity=False):
        """add product to the cart or update its qty"""
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {'quantity': 0, 'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
        self.session.modified = True

    """removes given product from cart dictionary and call save method"""
    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    """Iterate over the items in the cart and get the products  from the database."""
    def __iter__(self):
        product_ids = self.cart.keys()

        """get products objects and add them to the cart"""
        products = Product.objects.filter(id__in=product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    """Count all items in the cart."""
    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    """Calculates total cost of the items in the cart"""
    def get_total_price(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def clear(self):
        """remove cart from session"""
        del self.session[settings.CART_SESSION_ID]
        self.save()
