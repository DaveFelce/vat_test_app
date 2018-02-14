from django.test import TestCase
from .models import Product, Country, Region

class ProductTestCase(TestCase):
    fixtures = ['latest.json']

    def test_product_countries(self):
        all_wine = Product.objects.filter(name='Wine')
        self.assertEqual(len(all_wine), 2)

    def test_vat_for_product_by_country_uk(self):
         product = Product.objects.get(name='Wine', country__name='UK')
         vat = product.vat_for_product_by_country(price=15)
         self.assertEqual(vat, 1.5)

         product = Product.objects.get(name='Bread', country__name='UK')
         vat = product.vat_for_product_by_country(price=15)
         self.assertEqual(vat, 1.88)

         product = Product.objects.get(name='Bread', country__name='UK')
         vat = product.vat_for_product_by_country(price=60)
         self.assertEqual(vat, 8.5)

         product = Product.objects.get(name='Bread', country__name='UK')
         vat = product.vat_for_product_by_country(price=110)
         self.assertEqual(vat, 16.5)

    def test_vat_for_product_by_country_germany(self):
        product = Product.objects.get(name='Wine', country__name='Germany')
        vat = product.vat_for_product_by_country(price=100)
        self.assertEqual(vat, 20)

        product = Product.objects.get(name='Bread', country__name='Germany')
        vat = product.vat_for_product_by_country(price=11)
        self.assertEqual(vat, 1.25)

