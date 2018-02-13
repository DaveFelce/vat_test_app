from django.views import View
from django.shortcuts import render
from .models import Product

class TestPage(View):
    """Test page class-based view

    Args:
        View (:obj:Django View base class, required)

    """

    def get(self, request):

        product = Product()
        vat = product.vat_for_product_by_country(product_name='Wine', country_name='UK', price=100)
        return render(request, 'shop/index.html', {'vat': vat})
