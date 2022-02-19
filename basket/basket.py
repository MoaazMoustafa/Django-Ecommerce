from decimal import Decimal

from store.models import Product


class Basket():
    def __init__(self, request):
        self.session = request.session
        basket = self.session.get('skey')
        if 'skey' not in self.session:
            basket = self.session['skey'] = {}
        self.basket = basket

    def add(self, product, qty):
        product_id = str(product.id)
        if product_id in self.basket:
            self.basket[product_id]['qty'] += qty
        else:
            self.basket[product_id] = {'price': str(product.price), 'qty': qty}

        self.save()

    def __len__(self):
        """
        Get the basket data and count the qty of items
        """
        return sum(item['qty'] for item in self.basket.values())

    def __iter__(self):
        products_ids = self.basket.keys()
        products = Product.products.filter(id__in=products_ids)
        # print("🌹🌹🌹🌹", products, "🌹🌹🌹🌹")
        basket = self.basket.copy()
        for product in products:
            basket[str(product.id)]['product'] = product
        for item in basket.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['qty']
            yield item

    def get_total_price(self):
        return sum(float(item['price']) * item['qty'] for item in self.basket.values())

    def update(self, product_id, product_qty):
        product = str(product_id)
        if product in self.basket:
            self.basket[product]['qty'] = int(product_qty)
        self.save()

    def delete(self, productid):
        if str(productid) in self.basket:
            del self.basket[str(productid)]
        self.save()

    def save(self):
        self.session.modified = True
