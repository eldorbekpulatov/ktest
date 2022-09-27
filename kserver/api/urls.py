"""api URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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


from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views



urlpatterns = [
    path("login", views.GetAuthToken.as_view(), name="loginApi"),
    path('stations', views.StationsAPI.as_view(), name='stationApi'),
    path('products', views.ProductsAPI.as_view(), name='productApi'),
    path('models', views.ModelsAPI.as_view(), name='modelApi'),
    path('scripts', views.ScriptsAPI.as_view(), name='scriptApi'),
    path('reload', views.ReloadAPI.as_view(), name="reloadApi"),
    path('card', views.CardAPI.as_view(), name='cardApi')
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)