import subprocess

import oauth2 as oauth
import requests
import json
from requests_oauthlib import OAuth1

from flask import Flask
from flask import render_template


host = subprocess.check_output('hostname').strip()
try:
    dns = subprocess.check_output('dnsdomainname').strip()
    if dns:
        host = host + '.' + dns
    else:
        host = subprocess.check_output('hostname -i').strip()
except OSError:
    pass  # this happens when you are on a computer not set up as a server
app = Flask(__name__)


CONSUMER_KEY = 'kzdqjxzkp4m1'
CONSUMER_SECRET = 'lrb6PLggZQu65do4'
OAUTH_TOKEN = '9f2ce4d5-d0f9-425d-9531-0b278f667fad'
OAUTH_TOKEN_SECRET = '37990885-d278-4f10-8b1e-3e57227054df'

CONNECTIONS_URL = 'http://api.linkedin.com/v1/people/~/connections?format=json'
AUTHORIZATION_URL = 'https://www.linkedin.com/uas/oauth2/authorization'
ACCESS_TOKEN_URL = 'https://www.linkedin.com/uas/oauth2/accessToken'

url = "http://api.linkedin.com/v1/people/~"
all_friends_company_names = {}
profile_ids = {}

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_TOKEN_SECRET)

# print consumer # oauth_consumer_key=sjjy1qiurkig&oauth_consumer_secret=hiS7IQizThEHqkIZ
# print token # oauth_token_secret=723f556c-5803-44c2-a62e-71015eeda040&oauth_token=7790c0fa-8aed-4a9e-9373-f29d36225e0d

oauth1 = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=OAUTH_TOKEN, resource_owner_secret=OAUTH_TOKEN_SECRET)
client = oauth.Client(consumer, token)
resp, content = client.request(url)

@app.route("/")
def index():
    r = requests.get(url=CONNECTIONS_URL, auth=oauth1)
    profile_ids =  json.loads(r.content)
    return render_template('index.html')

@app.route("/searchCompany/<company>")
def searchCompany(company):
    friends = []
    print "Searching " + company
    r = requests.get(url=CONNECTIONS_URL, auth=oauth1)
    profile_ids =  json.loads(r.content)
    temp_dict = idtoComDic(profile_ids)
    print temp_dict
    for key in temp_dict.iterkeys():
        if temp_dict[key].lower().find(company) >= 0:
            friends.append(key)


    return render_template('index.html')

def idtoComDic(profile_ids):
    #doing only till 25 as we have limit on number of API calls
    for i in range(25):
        identity = profile_ids['values'][i]['id']
        URL = 'http://api.linkedin.com/v1/people/id='+identity+':(positions)?format=json'
        r = requests.get(url=URL, auth=oauth1)
        positions_dict = json.loads(r.content)
        if positions_dict.has_key('positions'):
            if positions_dict['positions']['_total'] >= 1:
                all_friends_company_names[identity] = positions_dict['positions']['values'][0]['company']['name']
        else:
            pass
    return all_friends_company_names

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)