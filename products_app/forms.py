""" Import Models """
from django import forms

from .models import Product, Category


class ProductForm(forms.ModelForm):
    """
    To allow store owners defined as those who are superusers
    in Django the ability to add, update, and delete products in the store.
    """

    class Meta:
        """ Defines the model and fields we wish to include """
        model = Product
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        """
        Overrides the __init__ method to make changes to the product form fields.
        """
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()

        # List comprehension for loop to create a list of tuples of the 
        # friendly names associated with their category ids:
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]

        # To update the category field on the form and use those for choices 
        # instead of using the id:
        self.fields['category'].choices = friendly_names
        
        # iterate through the rest of these fields and set
        # classes on them to match the rest of our store theme.
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'border-black rounded-0'
