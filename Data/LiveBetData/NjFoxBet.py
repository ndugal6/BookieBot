"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib.parse
import requests

def getNJFOX_Lines():
    host = 'http://sports.nj.foxbet.com'
    path = '/sportsbook/v1/api/getCompetitionEvents'
    params = {
        'competitionId': 4700094,  # id of comp from other api call
        'includeOutrights': 'false',  # unknown meaning
        'channelId': 14,  # unknown meaning
        'locale': 'en-us'
    }
    url = host + path + '?' + urllib.parse.urlencode(params)
    response = requests.get(url)
    print(response.status_code)
    return response


def getEventNames():
    events = getNJFOX_Lines().json()['event']
    names = []
    for event in events:
        names.append(event['name'])
    return names
