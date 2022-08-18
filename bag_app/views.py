""" import modules """
from django.shortcuts import (
    render, redirect, reverse, HttpResponse, get_object_or_404
    )
from django.contrib import messages

from products_app.models import Product

# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    # product = Product.objects.get(pk=item_id)
    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']  # set size to equal request.POST if it exists

    # session until client and server are done communicating
    # allows shopping bag to persist until session is closed.
    # Trys to get this variable if it already exists or 
    # initializing it to an empty dictionary if it doesn't.
    bag = request.session.get('bag', {})

    # adjust the add_to_bag structure
    # If a product with sizes is being added, 
    if size:
        # If item is in bag
        if item_id in list(bag.keys()):
            # check if another item w/ same size & id already exists
            if size in bag[item_id]['items_by_size'].keys():
                # increment quantity for that size
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f"Updated size {size.upper()} {product.name} quantity to {bag[item_id]['items_by_size'][size]}")
            else:
                # or just add it to the bag with the defined quantity
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Added size {size.upper()} {product.name} to your shopping bag')
        else:
            # If not in bag, add it as a dictionary. 
            # This allows us to structure the bags so we can have a single item_id for each item.
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Added size {size.upper()} {product.name} to your shopping bag')
    else:
        # if no size, can place product and quantity in the bag dictionary {}
        # and increment it by quantity orderd if it is already in the bag
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Added {product.name} to your shopping bag')
    
    # update the bag variable into the session [ a python dictionary ].
    request.session['bag'] = bag

    # Redirect the user back to the redirect URL
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """Adjust the quantity of the specified product to the specified amount"""

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']  # set size to equal request.POST if it exists

    # Trys to get this variable if it already exists or initializing it to an empty dictionary if it doesn't.
    bag = request.session.get('bag', {})

    # If a product with sizes is being added
    if size:
        # If item is in bag, set the items quantity accordingly, otherwise remove the item.
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f"Updated size {size.upper()} {product.name} quantity to {bag[item_id]['items_by_size'][size]}")
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Removed size {size.upper()} {product.name} from your shopping bag')
    # if no size
    else:
        # if no size, remove the item entirely by using the .pop function.
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Updated {product.name} quantity to {bag[item_id]}')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your shopping bag')
    
    request.session['bag'] = bag  # update the bag variable into the session [ a python dictionary ]
    return redirect(reverse('view_bag'))  # Redirect the user back view_bag URL


def remove_from_bag(request, item_id):
    """Remove the item from the shopping bag"""
    # In a try block to catch any exceptions that occur
    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        # if the user is removing a product with sizes, we only want to remove the specific size they requested.
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)  # remove the entire item_id size dictionary prevent it evaluating to false.
            messages.success(request, f'Removed size {size.upper()} {product.name} from your shopping bag')
        else:
            bag.pop(item_id)
            messages.success(request, f'Removed {product.name} from your shopping bag')

        request.session['bag'] = bag

        # Because view is posted to from a Js function, return an actual 200 HTTP response.
        return HttpResponse(status=200)

    except Exception as error:
        messages.error(request, f'Error receiving item: {error}')
        return HttpResponse(status=500)
