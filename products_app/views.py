from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q  # object to generate a search query
from django.db.models.functions import Lower

from .models import Product, Category
from .forms import ProductForm


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


# @decorators are special functions that wrap around another function
# and return a new one with some additional functionality. Used on the 
# line immediately above the view we wish to decorate:

@login_required
def add_product(request):
    """ Adds a product to the store """

    # To authorize that only superusers to have access to the add, edit, and delete views:
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    # If the request method is post, instantiates a new instance of 
    # the ProductForm and request the image of the product if submitted.
    if request.method == 'POST':
        form = ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save()
            messages.success(request, 'Successfully added product!')
            # return redirect(reverse('add_product'))

            # instead of redirecting to the add_product page once the product is added
            # instead redirect to that products_detail page like the edit view does:
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to add product. Please ensure the form is valid.')
    else:
        form = ProductForm()
        
    template = 'products/add_product.html'
    context = {
        'form': form,
    }

    return render(request, template, context)

@login_required
def edit_product(request, product_id):
    """ Edit a product in the store """

    # To authorize that only superusers to have access to the add, edit, and delete views:
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        # prefill form with instance of product obtained above
        form = ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, 'Successfully updated product!')

            # redirect back to the product detail page using the product id:
            return redirect(reverse('product_detail', args=[product.id]))
        else:
            messages.error(request, 'Failed to update product. Please ensure\
                your entries in the form are valid.')
    else:
        # instantiating product form and notifying user of editing capacity:
        form = ProductForm(instance=product)
        messages.info(request, f'You are editing {product.name}')

    # Tell it which template to use and render statement
    template = 'products/edit_product.html'
    context = {
        'form': form,
        'product': product,
    }

    return render(request, template, context)

@login_required
def delete_product(request, product_id):
    """ Delete a product from the store """

    # To authorize that only superusers to have access to the add, edit, and delete views:
    if not request.user.is_superuser:
        messages.error(request, 'Sorry, only store owners can do that.')
        return redirect(reverse('home'))

    product = get_object_or_404(Product, pk=product_id)
    product.delete()
    messages.success(request, 'Product deleted!')
    return redirect(reverse('products'))
