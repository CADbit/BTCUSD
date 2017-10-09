from django.db.models import *
from datetime import datetime
from decimal import Decimal, getcontext
import json

class NewModel(object):
    price = FloatField()
    amount = FloatField()
    timestamp = DateTimeField()

    @staticmethod
    def insertJSONrow(model, jsonObject):
        modelObject = model()
        modelObject.price = jsonObject['price']
        modelObject.amount = jsonObject['amount']
        modelObject.timestamp = datetime.fromtimestamp(int(Decimal(jsonObject['timestamp']))).strftime('%Y-%m-%d %H:%M:%S')
        modelObject.save()

    @staticmethod
    def insertJSONs(model, jsonObjects):
        for row in jsonObjects:
            model.insertJSONrow(model, row)

    @staticmethod
    def convert(model, jsonObject):
        modelObject = model()
        for key in jsonObject:
            if hasattr(modelObject, key):
                setattr(modelObject, key, jsonObject[key])

        return modelObject

    @staticmethod
    def rangeLimit(model, limit=50):
        from models import Purchase, Settings
        getcontext().prec = 8
        results = model.objects.all().order_by('timestamp').values('price', 'amount')[0:limit]
        value = Settings.getValue()
        data = [ ]
        for row in results:
            if isinstance(model, Purchase):
                row['price_with_commision'] = str(Decimal(row['price']) + value)
            else:
                row['price_with_commision'] = str(Decimal(row['price']) - value)
            data.append(row)

        return json.dumps(list(data))