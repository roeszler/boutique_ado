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

    # session until client and server are done communicating
    # allows shopping bag to persist until session is closed.
    # Trys to get this variable if it already exists or 
    # initializing it to an empty dictionary if it doesn't.
    bag = request.session.get('bag', {})

    # can place the product and quantity in the bag dictionary {}
    # and increment it by quantity orderd if it is already in the bag
    if item_id in list(bag.keys()):
        bag[item_id] += quantity 
    else:
        bag[item_id] = quantity
    
    # update the bag variable into the session [ a python dictionary ].
    request.session['bag'] = bag

    # Redirect the user back to the redirect URL
    return redirect(redirect_url)

