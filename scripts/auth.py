import oauth2 as oauth
import requests
from requests_oauthlib import OAuth1
import json

CONSUMER_KEY = 'sjjy1qiurkig'
CONSUMER_SECRET = 'hiS7IQizThEHqkIZ'
OAUTH_TOKEN = '7790c0fa-8aed-4a9e-9373-f29d36225e0d'
OAUTH_TOKEN_SECRET = '723f556c-5803-44c2-a62e-71015eeda040'

CONNECTIONS_URL = 'http://api.linkedin.com/v1/people/~/connections'
AUTHORIZATION_URL = 'https://www.linkedin.com/uas/oauth2/authorization'
ACCESS_TOKEN_URL = 'https://www.linkedin.com/uas/oauth2/accessToken'

url = "http://api.linkedin.com/v1/people/~"

consumer = oauth.Consumer(key=CONSUMER_KEY, secret=CONSUMER_SECRET)
token = oauth.Token(key=OAUTH_TOKEN, secret=OAUTH_TOKEN_SECRET)

# print consumer # oauth_consumer_key=sjjy1qiurkig&oauth_consumer_secret=hiS7IQizThEHqkIZ
# print token # oauth_token_secret=723f556c-5803-44c2-a62e-71015eeda040&oauth_token=7790c0fa-8aed-4a9e-9373-f29d36225e0d

oauth1 = OAuth1(CONSUMER_KEY, client_secret=CONSUMER_SECRET, resource_owner_key=OAUTH_TOKEN, resource_owner_secret=OAUTH_TOKEN_SECRET)
client = oauth.Client(consumer, token)

resp, content = client.request(url)
print resp
print content
r = requests.get(url=CONNECTIONS_URL, auth=oauth1)
print r.content
