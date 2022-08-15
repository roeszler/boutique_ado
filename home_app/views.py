from django.shortcuts import render


def index(request):
    """
    View to return the index page
    """
    return render(request, 'home/index.html')  # looks within the current directory home_app/templates/home/index.html
