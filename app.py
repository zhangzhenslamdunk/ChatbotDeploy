#!/usr/bin/env python

import urllib
import json
import os
import sys

from flask import Flask
from flask import request
from flask import make_response

# Flask app should start in global layout
app = Flask(__name__)


@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
    
    res = processRequest(req)
    print("Request processed")
    
    res = json.dumps(res, indent=4)
    print(res)
    
    r = make_response(res)
    print(r)
    
    r.headers['Content-Type'] = 'application/json'
    return r


def processRequest(req):
    if req.get("result").get("action") != "createCheckBook":
        return {}
    baseurl = "https://ldcif6u.wdf.sap.corp:44304/sap/opu/odata/sap/ZIVRC_SRV/WorkItems("
    print(baseurl)
    
    yql_query = makeYqlQuery(req)
    print("yql_query1:")
    print(yql_query)
    
    if yql_query is None:
        return {}
    yql_url = baseurl + urllib.urlencode({yql_query}) + "?$format=json"
    print(yql_query)
    
    result = urllib.urlopen(baseurl).read()
    print(result)
    data = json.loads(result)
    print("data1:")
    print(data)
    
    res = makeWebhookResult(data)
    return res


def makeYqlQuery(req):
    result = req.get("result")
    print("result1:")
    print(result)
    parameters = result.get("parameters")
    print("parameters1:")
    print(parameters)
    city = parameters.get("workitemtype")
    print("City1:")
    print(city)
    if city is None:
        return None
        
        return "guid'" + "0005EEE4-48CC-1ED5-B0C9-FA163EA701AC" + "')"
   #return "select * from weather.forecast where woeid in (select woeid from geo.places(1) where text='" + city + "')"


def makeWebhookResult(data):
    print("MakeWebhook method")
    query = data.get('d')
    print("Query1:")
    print(query)
    if query is None:
        return {}

    result = query.get('WORKITEM_ID')
    if result is None:
        return {}

    channel = query.get('DESCRIPTION')
    if channel is None:
        return {}

   # item = channel.get('item')
   # location = channel.get('location')
   # units = channel.get('units')
   # if (location is None) or (item is None) or (units is None):
   #    return {}

   # condition = item.get('condition')
   # if condition is None:
   #     return {}

    # print(json.dumps(item, indent=4))

   # speech = "Today in " + location.get('city') + ": " + condition.get('text') + \
   #         ", the temperature is " + condition.get('temp') + " " + units.get('temperature')
	speech = " The Work Item No. " + result + " has been created for " + channel
    print("Response1:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        # "data": data,
        # "contextOut": [],
        "source": "apiai-weather-webhook-sample"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print "Starting app on port %d" % port

    app.run(debug=False, port=port, host='0.0.0.0')
