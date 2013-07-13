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


CONSUMER_KEY = 'u9ubnpghfe98'
CONSUMER_SECRET = 'FhA54NmEVoOvPGmA'
OAUTH_TOKEN = 'd2e726c5-a06b-44d9-be80-230d8da437fb'
OAUTH_TOKEN_SECRET = '482f85d6-6953-4cf4-b159-710e0b9d74da'

CONNECTIONS_URL = 'http://api.linkedin.com/v1/people/~/connections?format=json'
AUTHORIZATION_URL = 'https://www.linkedin.com/uas/oauth2/authorization'
ACCESS_TOKEN_URL = 'https://www.linkedin.com/uas/oauth2/accessToken'

url = "http://api.linkedin.com/v1/people/~"
all_friends_company_names = {}
all_friends_uni_names =  {}
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
    friends_id = []
    friends_name = []
    result_dict = dict()
    print "Searching " + company
    r = requests.get(url=CONNECTIONS_URL, auth=oauth1)
    profile_ids =  json.loads(r.content)
    temp_dict = idtoComDic(profile_ids)
    print temp_dict
    for key in temp_dict.iterkeys():
        if temp_dict[key].lower().find(company) >= 0:
            if result_dict.has_key(temp_dict[key]):
                result_dict[temp_dict[key]] = result_dict[temp_dict[key]] + "," + key
            else:
                result_dict[temp_dict[key]] = key
    return json.dumps(result_dict)
    #return render_template('index.html')


def idtoComDic(profile_ids):
    #doing only till 25 as we have limit on number of API calls
    for i in range(100):
        identity = profile_ids['values'][i]['id']
        key = profile_ids['values'][i]['firstName'] + " " + profile_ids['values'][i]['lastName']
        URL = 'http://api.linkedin.com/v1/people/id='+identity+':(positions,first-name,last-name)?format=json'
        r = requests.get(url=URL, auth=oauth1)
        positions_dict = json.loads(r.content)
        if positions_dict.has_key('positions'):
            if positions_dict['positions']['_total'] >= 1:
                all_friends_company_names[key] = positions_dict['positions']['values'][0]['company']['name']
        else:
            pass
    return all_friends_company_names

@app.route("/searchUniversity/<university>")
def searchUniversity(university):
    result_uni = dict()
    r = requests.get(url=CONNECTIONS_URL, auth=oauth1)
    profile_ids = json.loads(r.content)
    key = university
    for i in range (profile_ids['_count']):
        if profile_ids['values'][i].has_key('headline') :
            if university.lower() in profile_ids['values'][i]['headline'].lower():
                if result_uni.has_key(key):
                    result_uni[key] = result_uni[key] + ","+ profile_ids['values'][i]['firstName'] + " " + profile_ids['values'][i]['lastName']
                else: 
                    result_uni[key] =  profile_ids['values'][i]['firstName'] + " " + profile_ids['values'][i]['lastName']

    return json.dumps(result_uni)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
