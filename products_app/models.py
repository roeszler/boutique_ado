from django.db import models

class Category(models.Model):
    """ Category display model for the fixtures in products_app to go in """
    class Meta:
        """ to adjust the verbose name or the plural form from the Django defaults """
        verbose_name_plural = 'Categories'
    
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)  # optional

    def __str__(self):
        """ Takes in category model and returns name """
        return self.name
    
    def get_friendly_name(self):
        """ Takes in category model and returns the friendly_name """
        return self.friendly_name


class Product(models.Model):
    """
    Product display model for the .json fixtures in products_app to go in.
    Foreign key to the category model above, null in DB and blank in forms.
    if a category is deleted, any products that use it will to have null
    for category field rather than deleting the product.
    """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
    # Fields directly from the products.json file
    sku = models.CharField(max_length=254, null=True, blank=True)
    name = models.CharField(max_length=254)
    description = models.TextField()
    price = models.DecimalField(max_digits=6, decimal_places=2)
    rating = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True)
    image_url = models.URLField(max_length=1024, null=True, blank=True)
    image = models.ImageField(null=True, blank=True)

    def __str__(self):
        """ Takes in product display model and returns name """
        return self.name
