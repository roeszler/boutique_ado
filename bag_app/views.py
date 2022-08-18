""" import modules """
from django.shortcuts import render, redirect

# Create your views here.
def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specified product to the shopping bag """

    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['size']  # set size to equal request.POST if it exists

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
            else:
                # or just add it to the bag with the defined quantity
                bag[item_id]['items_by_size'][size] = quantity
        else:
            # If not in bag, add it as a dictionary. 
            # This allows us to structure the bags so we can have a single item_id for each item.
            bag[item_id] = {'items_by_size': {size: quantity}}
    else:
        # if no size, can place product and quantity in the bag dictionary {}
        # and increment it by quantity orderd if it is already in the bag
        if item_id in list(bag.keys()):
            bag[item_id] += quantity 
        else:
            bag[item_id] = quantity
    
    # update the bag variable into the session [ a python dictionary ].
    request.session['bag'] = bag

    # Redirect the user back to the redirect URL
    return redirect(redirect_url)

