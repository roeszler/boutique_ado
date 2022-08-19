from django.apps import AppConfig


class CheckoutAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'checkout_app'

    def ready(self):
        """ Overriding the ready method and importing our signals module. """
        import checkout_app.signals
