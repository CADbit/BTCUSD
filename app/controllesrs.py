from django.http import HttpResponse, JsonResponse
from django.db import transaction
from decimal import *
from exceptions import Exception
from django.core import serializers

from app.models import *

import json
import urllib2
import datetime

class ExchangeController():
    bids = []
    asks = []
    today = datetime.datetime.now().date()
    tomorrow = today + datetime.timedelta(days=1)

    @classmethod
    def orderbook(self, request, limit=50):
        bids = Purchase.rangeLimit(Purchase, limit)
        asks = Sale.rangeLimit(Sale, limit)
        jsonData =  {'bids': bids, 'asks': asks}

        return HttpResponse(JsonResponse(jsonData), content_type='application/json')

    def history(self, request, dateFrom=today, dateTo=tomorrow):
        currencyExchange = json.dumps(serializers.serialize('json', CurrencyExchange.rangeDate(dateFrom, dateTo)))
        print self.today

        return HttpResponse(currencyExchange, content_type='application/json')

    def value(self, request, value):
        Settings.setValue(value)

        return HttpResponse('Aktualna kwota prwizji wynosi: {0}'.format(Settings.getValue()))

    def calc_rate(self, array):
        getcontext().prec = 8
        rates_sum = 0
        rates_sum_arr = []
        for rate in array:
            price = rate['price']
            amount = rate['amount']
            priceD = Decimal(price)
            amountD = Decimal(amount)
            rates_sum += (priceD/amountD)
            rates_sum_arr.append(Decimal(rates_sum))

        return Decimal(sum(rates_sum_arr)/len(rates_sum_arr))

    def serialize(self, json):
        data = []
        for row in json:
            data.append(serializers.serialize('json', row))

        return data

    @transaction.atomic
    def getData(self):
        status = False
        btcusd = json.load(urllib2.urlopen(Settings.getUrl()))
        bids = btcusd['bids'][0:100]
        asks = btcusd['asks'][0:100]
        rateBids = self.calc_rate(bids)
        rateAsks = self.calc_rate(asks)

        try:
            with transaction.atomic():
                Purchase.insertJSONs(Purchase, bids)
                Sale.insertJSONs(Sale, asks)
                CurrencyExchange.insert(rateBids, rateAsks)
                status = True
        except Exception:
            transaction.rollback()
            return Exception.message

        return status