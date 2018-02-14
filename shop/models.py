import decimal
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
    country = models.ForeignKey(Country)
    name = models.CharField(max_length=100)
    base_vat = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
    flat_vat = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    first_tax_free_amount = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    band1_vat = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
    band2_vat = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
    band3_vat = models.DecimalField(decimal_places=2, max_digits=4, blank=True, null=True)
    band1_price_range = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)
    band2_price_range = models.DecimalField(decimal_places=2, max_digits=7, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        managed = True
        db_table = 'product'
        verbose_name_plural = "products"

    def vat_for_product_by_country(self, price):
        """
        :param price: the total price for the product
        :return: calculated VAT
        """

        # Business logic is:
        # - if there's a flat VAT charge then return that
        # - if there's a first tax free amount, take that off the price
        # - if there are bands to be applied, apply them, calculate and return
        # - if there is a product specific base VAT, apply that and return
        # - finally, apply any local (country) base rate if it exists, or use the regional one otherwise
        # - N.B.: max rate or value for VAT is not implemented
        if self.flat_vat:
            return self.flat_vat

        if self.first_tax_free_amount:
            price = price - self.first_tax_free_amount

        # VAT bands
        if self.band1_price_range and (1 <= price <= self.band1_price_range+1):
            return self._percentage(self.band1_vat, price)
        if self.band2_price_range and (self.band1_price_range <= price <= self.band2_price_range+1):
            # TODO: Put these repeated calcs in method
            price = price - self.band1_price_range
            band1_vat = self._percentage(self.band1_vat, self.band1_price_range)
            band2_vat = self._percentage(self.band2_vat, price)
            return band1_vat + band2_vat
        # Assume, for the test, that there will always be lower bands than the current
        if self.band3_vat and price >= self.band2_price_range:
            band1_vat = self._percentage(self.band1_vat, self.band1_price_range)
            band2_vat = self._percentage(self.band2_vat, self.band2_price_range - self.band1_price_range)
            price = price - self.band2_price_range
            band3_vat = self._percentage(self.band3_vat, price)
            return band1_vat + band2_vat + band3_vat

        # Base VATs
        if self.base_vat:
            return self._percentage(self.base_vat, price)
        if self.country.base_vat:
            return self._percentage(self.country.base_vat, price)
        else:
            return self._percentage(self.country.region.base_vat, price)

    def _percentage(self, percent, whole):
        percent = float(percent)
        whole = float(whole)
        return round(((percent * whole) / 100.0), 2)

