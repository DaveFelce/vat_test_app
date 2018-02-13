from django.test import TestCase
from .models import Product, Country, Region

class ProductTestCase(TestCase):
    fixtures = ['latest.json']

    def test_product_countries(self):
        all_eggs = Product.objects.filter(name='Eggs')
        self.assertEqual(len(all_eggs), 2)


