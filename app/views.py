from django.http import HttpResponse

from array import array as ar

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

import json
import urllib2

def bids(request):
    btcusd = json.load(urllib2.urlopen("https://api.bitfinex.com/v1/book/BTCUSD"))
    bids = btcusd['bids']
    asks = btcusd['asks']

    bids_len = len(bids)
#    bids100 = bids[(bids_len-100):bids_len]
    bids100 = bids[0:100]
    #rate = calc_rate(bids100)
    #rate = calc_rate(bids[0:100])
    rateBids = calc_rate(bids)
    rateAsks = calc_rate(asks)

    data = []

    # data.append(bids100)
    # data.append(bids_len)
    data.append(rateBids)
    data.append(rateAsks)

    return HttpResponse(data)

from decimal import *

def calc_rate(array):
    rates_sum = 0
    rates_sumF = 0
    sumP = 0
    sumA = 0
    sum2 = 0;
    rates_arr = []
    getcontext().prec = 6
    getcontext().traps[DivisionByZero] = 1
    for rate in array:
        price = rate['price']
        amount = rate['amount']
        priceD = Decimal(price)
        amountD = Decimal(amount)
        rates_sum += (priceD/amountD)
        rates_sumF = rates_sumF + (float(price)/float(amount))
        #rates_arr.append([price, amount, priceD, amountD, priceD/amountD])
        sumP += priceD
        sumA += amountD
        rates_arr.append(Decimal(priceD/amountD))

        # rates_arr.append(Decimal(rate['price'])/Decimal(rate['amount']))
    print rates_sum,' ',len(array),' ',(rates_sum/len(array)),' ',(sumP/len(array))

    return [rates_sum/len(array)]
    #return rates_sum/Decimal(len(array))
    #return [rates_sum, len(array), rates_sum/len(array)]
    #return [(sumP/len(array)), (rates_sum/len(array))]
