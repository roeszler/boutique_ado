"""boutique URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings  # to link up our static and media files
from django.conf.urls.static import static  # to link up our static and media files

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', include('home_app.urls')),  # tells it to look in the app dir home_app/urls.py
    path('products/', include('products_app.urls')),  # look in the app dir products_app/urls.py
    path('bag/', include('bag_app.urls')),  # look in the app dir products_app/urls.py
    path('checkout/', include('checkout_app.urls')),  # look in the app dir checkout_app/urls.py
    path('profile/', include('profiles_app.urls')),  # look in the app dir profiles_app/urls.py
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
