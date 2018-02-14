from django.views import View
from django.shortcuts import render
from .models import Product

class TestPage(View):
    """Test page class-based view

    Args:
        View (:obj:Django View base class, required)

    """

    def get(self, request):

        product = Product.objects.get(name='Wine', country__name='Germany')
        vat = product.vat_for_product_by_country(price=200)
        currency_symbol = product.country.currency
        return render(request, 'shop/index.html', {'currency_symbol': currency_symbol, 'price': 200, 'vat': vat})
