"""Example of Python client calling Fox Bet Sports World."""
# https://nj.foxbet.com/#/basketball/competitions/4700094
import json
import urllib.parse
import requests
host = 'http://sports.nj.foxbet.com'
basePath = '/sportsbook/v1/api'

def getNJFOX_Lines():
    path = '/getCompetitionEvents'
    params = {
        'competitionId': get_nba_id(),  # id of comp from other api call
        'includeOutrights': 'false',  # unknown meaning
        'channelId': 14,  # unknown meaning
        'locale': 'en-us'
    }
    url = host + basePath + path + '?' + urllib.parse.urlencode(params)
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
    path = '/getSportTree'
    params = {
        'sport': 'BASKETBALL',
        'includeOutrights': False,  # unknown meaning
        'includeEvents': False,  # unknown meaning
        'channelId': 14,  # unknown meaning
        'locale': 'en-us'
    }
    url = host + basePath + path + '?' + urllib.parse.urlencode(params)
    response = requests.get(url)
    print(response.status_code)
    return response


def get_event_details(event_id = 8346742):
    path = '/getEvent'
    params = {
        'eventId': event_id,
        'channelId': 14,  # unknown meaning
        'locale': 'en-us'
    }
    url = host + basePath + path + '?' + urllib.parse.urlencode(params)
    response = requests.get(url)
    print(response.status_code)
    return response



def main():
    print(get_nba_id())
    print(getEventNames())
    print(get_event_details().json()['name'])

if __name__ == '__main__':
    main()


# A MAPPING OF SPORTSTREE
