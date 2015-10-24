#!/usr/bin/python

import json
import urllib2
import base64
import zlib

# Overall WS Access Variables
dbsAlias = 'xTD150'
wsHost = 'dragon.teradata.ws'
wsPort = '1080'
path = '/tdrest/systems/' + dbsAlias + '/queries'


# noinspection PyPackageRequirements
def rest_request(query, wsUser, wsPass):
    url = 'http://' + wsHost + ':' + wsPort + path

    headers = {}
    headers['Content-Type'] = 'application/json'
    headers['Accept'] = 'application/vnd.com.teradata.rest-v1.0+json'
    headers['Authorization'] = "Basic %s" % base64.encodestring('%s:%s' % (wsUser, wsPass)).replace('\n', '');

    # Set query bands
    queryBands = {}
    queryBands['applicationName'] = 'MyApp'
    queryBands['version'] = '1.0'

    # Set request fields. including SQL
    data = {}
    data['query'] = query
    data['queryBands'] = queryBands
    data['format'] = 'array'

    # Build request.
    request = urllib2.Request(url, json.dumps(data), headers)

    # Submit request
    try:
        response = urllib2.urlopen(request);
        # Check if result have been compressed.
        if response.info().get('Content-Encoding') == 'gzip':
            response = zlib.decompress(response.read(), 16 + zlib.MAX_WBITS)
        else:
            response = response.read();
    except urllib2.HTTPError, e:
        print 'HTTPError = ' + str(e.code)
        response = e.read();
    except urllib2.URLError, e:
        print 'URLError = ' + str(e.reason)
        response = e.read();

    # Parse response to confirm value JSON.
    results = json.loads(response);
    print(type(results))
    print("printing results")
    #results is a dictionary

    print(results['results'])

    data = {}

    with open('countrynames.txt') as file:
        importedfile = file.read().split()

    for i in importedfile:
        data[i] = 0
        # data is now a dict with country names and their values are all 0

    # iterate through results(row data)
    #
    for x in results['results']:
        #x[0]
        """
        print("data x is ")
        print(x)
        for i in importedfile:
            data[i] += x[i+1]
        print(x)
#        data[x] = results.data
        """
        print("THIS IS X")
        print(x[])


    json_data = json.dumps(data)


    print json.dumps(results, indent=4, sort_keys=True)

    return json_data


def perform_query(query, wsUser, wsPass):
    return rest_request(query, wsUser, wsPass)


wsUser = 'hack_user15'
wsPass = 'tdhackathon'

sqlobj = perform_query('select * from homeland_security.refugee_arrivals_by_country', wsUser, wsPass)


print(sqlobj)
#arrivaltotals = {'total': 0}
#idValue = arrivaltotals['data']


