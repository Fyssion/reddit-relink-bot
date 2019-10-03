import requests
base_url = 'https://www.reddit.com/'
data = {'grant_type': 'password', 'username': "reddit-relinkdiscord", 'password': "relinkdiscord"}
auth = requests.auth.HTTPBasicAuth("fRymMJayGXty1g", "xMt_lwbyy6tMDyYyWZ47zdeyVPY")
r = requests.post(base_url + 'api/v1/access_token',
                  data=data,
                  headers={'user-agent': 'APP-NAME by REDDIT-USERNAME'},
		  auth=auth)
d = r.json()
print(d)

token = 'bearer ' + d['access_token']

base_url = 'https://oauth.reddit.com'

headers = {'Authorization': token, 'User-Agent': 'APP-NAME by REDDIT-USERNAME'}
response = requests.get(base_url + '/api/v1/me', headers=headers)

if response.status_code == 200:
    print(response.json()['name'], response.json()['comment_karma'])
    payload = {'q': 'puppies', 'limit': 5, 'sort': 'relevance'}
    response = requests.get(api_url + '/subreddits/search', headers=headers, params=payload)
    print(response.status_code)
    values = response.json()
    print(response.text)
print(r.status_code)