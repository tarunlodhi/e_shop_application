from django.db import models
from .catagories import Catagories


class Product(models.Model):
    name = models.CharField(max_length=50, blank=False)
    price = models.IntegerField(default=0, null=False)
    catagory = models.ForeignKey(
        Catagories, on_delete=models.CASCADE, default = 1)
    description = models.CharField(max_length=200)
    image = models.ImageField(upload_to='products')

    @staticmethod
    def get_all_products():
        return Product.objects.all()

    @staticmethod
    def get_product_by_id(catagory_id):
        if catagory_id:
            return Product.objects.filter(catagory=catagory_id)
        else:
            return Product.objects.all()

    @staticmethod
    def get_product_by_ids(ids):
        return Product.objects.filter(id__in=ids)
