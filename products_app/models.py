from django.db import models

class Category(models.Model):
    """ Model for the fixtures in products_app to go in """
    name = models.CharField(max_length=254)
    friendly_name = models.CharField(max_length=254, null=True, blank=True)  # friendly name is optional

    def __str__(self):
        """ Takes in category model and returns name """
        return self.name
    
    def get_friendly_name(self):
        """ Takes in category model and returns the friendly_name """
        return self.friendly_name

class Product(models.Model):
    """ 
    Model for the fixtures in products_app to go in.
    Foreign key to the category model above, null in DB and blank in forms.
    if a category is deleted, any products that use it will to have null 
    for category field rather than deleting the product.
    """
    category = models.ForeignKey('Category', null=True, blank=True, on_delete=models.SET_NULL)
