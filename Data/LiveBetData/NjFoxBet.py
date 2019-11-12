"""Example of Python client calling Knowledge Graph Search API."""
import json
import urllib.parse
import requests

def getNJFOX_Lines():
    host = 'http://sports.nj.foxbet.com'
    path = '/sportsbook/v1/api/getCompetitionEvents'
    params = {
        'competitionId': get_nba_id(),  # id of comp from other api call
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


def get_nba_id():
    response = get_sports_tree()
    for category in response.json()['categories']:
        if category['name'].__contains__('USA'):
            for comp in category['competition']:
                if comp['name'].__contains__('USA - NBA'):
                    return comp['id']
    return None


def get_sports_tree():
    path = '/sportsbook/v1/api/getSportTree'
    host = 'http://sports.nj.foxbet.com'
    params = {
        'sport': 'BASKETBALL',  # id of comp from other api call
        'includeOutrights': 'false',  # unknown meaning
        'includeEvents': 'false',  # unknown meaning
        'channelId': 14,  # unknown meaning
        'locale': 'en-us'
    }
    url = host + path + '?' + urllib.parse.urlencode(params)
    response = requests.get(url)
    print(response.status_code)
    return response



def main():
    print(get_nba_id())
    print(getEventNames())

if __name__ == '__main__':
    main()
