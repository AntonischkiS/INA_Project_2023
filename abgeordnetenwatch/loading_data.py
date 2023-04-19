import requests
import json

BASE_URL = 'https://www.abgeordnetenwatch.de/api/v2/'
BUNDESTAG_ID = 5


def get_parliament_periods(parliament_id):
    params = {'parliament': parliament_id, 'type': 'legislature'}
    resp = requests.get(BASE_URL+'parliament-periods', params)
    return resp.json()

def get_polls(legislature_id):
    params = {'field_legislature': legislature_id, 'range_end': 500}
    resp = requests.get(BASE_URL+'polls', params)
    return resp.json()

def get_votes(poll_id):
    params = {'poll': poll_id, 'range_end': 1000}
    resp = requests.get(BASE_URL+'votes', params)
    return resp.json()

def get_mandates(legislature_id):
    params = {'parliament_period': legislature_id, 'range_end': 1000}
    resp = requests.get(BASE_URL+'candidacies-mandates', params)
    return resp.json()

def get_fractions(legislature_id):
    params = {'legislature': legislature_id}
    resp = requests.get(BASE_URL+'fractions', params)
    return resp.json()

def load_legislature(legislature_id, base_path):
    # mandate data
    mandates_data = get_mandates(legislature_id)
    fractions_data = get_fractions(legislature_id)
    fm_data = dict()
    fractions = []
    for fraction in fractions_data['data']:
        fractions.append({
            'id': fraction['id'],
            'name': fraction['full_name']
        })
    mandates = []
    for mandate in mandates_data['data']:
        if len(mandate['fraction_membership']) != 1:
            print('PROBLEM')
        mandates.append({
            'id': mandate['id'],
            'name': mandate['politician']['label'],
            'fraction_id': mandate['fraction_membership'][0]['fraction']['id']
        })
    fm_data['fractions'] = fractions
    fm_data['mandates'] = mandates
    with open(f'{base_path}mandates.json', 'w', encoding='utf8') as f:
        json.dump(fm_data, f, ensure_ascii=False)  # ensure_ascii=False für Umlaute etc.
    # poll data
    polls_data = get_polls(legislature_id)
    for poll in polls_data['data']:
        poll_data = dict()
        poll_data['id'] = poll['id']
        poll_data['date'] = poll['field_poll_date']
        votes = []
        votes_data = get_votes(poll['id'])
        for vote in votes_data['data']:
            votes.append({
                'mandate_id': vote['mandate']['id'],
                'vote': vote['vote']
            })
        poll_data['votes'] = votes
        with open(f'{base_path}poll_{poll["id"]}.json', 'w', encoding='utf8') as f:
            f.write(json.dumps(poll_data))


if __name__ == '__main__':
    load_legislature(132, 'data/Bundestag/2021-2025/')