from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.db.models import Q  # object to generate a search query
from django.db.models.functions import Lower
from .models import Product, Category


def all_products(request):
    """ A view to show all products, including sorting and search queries """
    products = Product.objects.all()
    query = None  # ensures no error when loading without a search term
    categories = None  # ensures no error when loading without a categories filter
    sort = None  # ensures no error when loading without a sort filter
    direction = None  # ensures no error when loading without a direction filter

# To return results where the query was matched in either the product name OR
# the description. The OR logic is derived through 'Q'.
# If q is in request.get, set q to equal a variable called 'query'
# Django messages framework & redirect, reversely back to the products url
    if request.GET:
        if 'q' in request.GET:
            query = request.GET['q']
            if not query:
                messages.error(request, "You didn't enter any search criteria!")
                return redirect(reverse('products'))
            
            # Where the name contains the query OR the description contains the query
            # and the i makes the case insensitive
            queries = Q(name__icontains=query) | Q(description__icontains=query)
            products = products.filter(queries)
        
        if 'category' in request.GET:
            categories = request.GET['category'].split(',')  # split into a list at the commas
            products = products.filter(category__name__in=categories)  # use list to filter current query to only products whose category 'name' is in the list.
            categories = Category.objects.filter(name__in=categories)  # filter all categories down to the ones whose name is in the list from the URL.
        
        if 'sort' in request.GET:
            sortkey = request.GET['sort']
            sort = sortkey  # sort into sortkey is to preserve the original field we want it to sort on name.
            
            # Now annotate all the products with a new field:
            if sortkey == 'name':
                sortkey = 'lower_name_annotation'
                products = products.annotate(lower_name_annotation=Lower('name'))
            
            # Categories to be sorted by name instead of their ids
            if sortkey == 'category':
                sortkey = 'category__name'
                # double underscore allows us to drill into a related model, effectively changing
                # products = products.order_by(sortkey) to ...order_by(category__name)

            # To check whether direction is descending
            if 'direction' in request.GET:
                direction = request.GET['direction']
                if direction == 'descending':  # if direction=descending...
                    sortkey = f'-{sortkey}'  # using string formatting to reverse the order
            
            products = products.order_by(sortkey)  # to sort the products

    # To return the current sorting methodology to the template
    current_sorting = f'{sort}_{direction}'

    context = {
        'products': products,
        'search_term': query,
        'current_categories': categories,
        'current_sorting': current_sorting,
    }
    return render(request, 'products/products.html', context)


def product_detail(request, product_id):
    """ A view to show individual product details """
    product = get_object_or_404(Product, pk=product_id)
    context = {
        'product': product,
    }
    return render(request, 'products/product-detail.html', context)
