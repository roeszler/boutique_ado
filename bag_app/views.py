from django.shortcuts import render


def view_bag(request):
    """ View that renders the shopping bag contents page """
    return render(request, 'bag/bag.html')  # looks within the current directory bag_app/templates/bag/bag.html
