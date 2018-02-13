from django.db import models

class Region(models.Model):
    id = models.AutoField(primary_key=True)
    base_vat = models.DecimalField(decimal_places=2, max_digits=4)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'region'
        verbose_name_plural = "regions"


class Country(models.Model):
    id = models.AutoField(primary_key=True)
    base_vat = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
    currency = models.CharField(max_length=1)
    name = models.CharField(max_length=100)
    region = models.ForeignKey(Region)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'country'
        verbose_name_plural = "countries"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    country = models.ManyToManyField(Country)
    name = models.CharField(max_length=100)
    base_vat = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
    band1_vat = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
    band2_vat = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
    band3_vat = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
    band1_price_range = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    band2_price_range = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    price = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'product'
        verbose_name_plural = "products"

    def vat_for_product_by_country(self, product_name, country_name, price):
        """

        :param product_name: e.g. 'Wine'
        :param country_name: e.g. 'UK'
        :param price: the total price for the product/s
        :return: calculated VAT
        """

        """ Obviously here we do the DB calls to fetch the data and calculate VAT in the real app """
        return 10
