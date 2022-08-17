

def bag_contents(request):
    """
    Does not return a template, rather a dictionary called 'context'
    Known as a context processor, it makes this dictionary available
    to all templates across the entire bag_app application via adding
    it to the TEMPLATES variable in settings.py
    """
    bag_contents = []
    total = 0
    product_count = 0

    

    context = {}

    return context
