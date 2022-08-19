""" Import Modules """
from django import forms

from .models import Order


class OrderForm(forms.ModelForm):
    """ To customize the imported django form to our needs """
    class Meta:
        """ Tell Django its associations and editable user input fields """
        model = Order
        fields = (
            'full_name', 'email', 'phone_number',
            'street_address1', 'street_address2',
            'town_or_city', 'postcode', 'country',
            'county',
        )
    
    #  to override the init method of the form, allowing us to customize it
    def __init__(self, *args, **kwargs):
        """
        Add placeholders and classes, remove auto-generated
        labels and set autofocus on first field
        """
        # To call the default init method to set the form up as it would be by default:
        super().__init__(*args, **kwargs)

        # To create a dictionary of placeholders which will show up in the form fields
        # rather than having clunky looking labels and empty text boxes in the template:
        placeholders = {
            'full_name': 'Full Name',
            'email': 'Email Address',
            'phone_number': 'Phone Number',
            'country': 'Country',
            'postcode': 'Postal Code',
            'town_or_city': 'Town or City',
            'street_address1': 'Street Address 1',
            'street_address2': 'Street Address 2',
            'county': 'County',
        }

        # setting the autofocus attribute on the full name field to true so the
        # cursor starts in the full name field when the user loads the page:
        self.fields['full_name'].widget.attrs['autofocus'] = True

        # To iterate through the forms fields adding a star to the placeholder
        # if it's a required field on the model:
        for field in self.fields:
            if self.fields[field].required:
                placeholder = f'{placeholders[field]} *' # '*' if it's a required field on the model
            else:
                placeholder = placeholders[field]
            self.fields[field].widget.attrs['placeholder'] = placeholder # Setting all the placeholder attributes to their values in the above dictionary
            self.fields[field].widget.attrs['class'] = 'stripe-style-input'  # adding a css class
            self.fields[field].label = False  # removing form fields labels as now placeholders are set
