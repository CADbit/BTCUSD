"""btcusd2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from app.controllesrs import ExchangeController

exchange = ExchangeController()

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^orderbook/$', exchange.orderbook, name='orderbook'),
    url(r'^orderbook/(?P<limit>[0-9]+)/$', exchange.orderbook, name='orderbook'),
    url(r'^history/$', exchange.history, name='history'),
    url(r'^history/(?P<dateFrom>\d{4}-\d{2}-\d{2})/(?P<dateTo>\d{4}-\d{2}-\d{2})/$', exchange.history, name='history'),
    url(r'^set_commision/(?P<value>[0-9].[0-9]+)/$', exchange.value, name='set_commision'),
]
