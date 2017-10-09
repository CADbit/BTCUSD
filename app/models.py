# -*- coding: utf-8 -*-
from django.db import models
from NewModelTrait import NewModel
from decimal import *

import datetime
# Create your models here.

class Purchase(NewModel, models.Model):
    price = NewModel.price
    amount = NewModel.amount
    timestamp = NewModel.timestamp

class Sale(NewModel, models.Model):
    price = NewModel.price
    amount = NewModel.amount
    timestamp = NewModel.timestamp

class Settings(models.Model):
    value = models.DecimalField(max_digits=4, decimal_places=2)
    url = models.URLField()

    @staticmethod
    def getValue():
        return Settings.objects.first().value

    @staticmethod
    def setValue(value):
        settings = Settings.objects.first()
        settings.value = value
        settings.save()

    @staticmethod
    def getUrl():
        return Settings.objects.first().url

    @staticmethod
    def setUrl(url):
        settings = Settings().objects.first()
        settings.url = url
        settings.save()

class CurrencyExchange(models.Model):
    purchase_rate = models.FloatField()
    sale_rate = models.FloatField()
    timestamp = models.DateTimeField(default=datetime.datetime.today, blank=True)

    @classmethod
    def rangeDate(self, dateFrom, dateTo):
        return self.objects.all().filter(timestamp__range=(dateFrom, dateTo))

    @staticmethod
    def insert(rateBids, rateAsks):
        getcontext().prec = 8
        currencyExchange = CurrencyExchange()
        currencyExchange.purchase_rate = Decimal(rateBids)
        currencyExchange.sale_rate = Decimal(rateAsks)
        currencyExchange.save()