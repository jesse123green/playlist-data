import requests
import simplejson as json
import pymysql
import time,sys

def refresh_token():
	user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
	url = 'https://accounts.spotify.com/api/token'
	values = {'grant_type' : 'client_credentials'}
	headers = {'Authorization':'Basic YmM5YzJiYjdhZDU0NDQ2ZjkyZGVhYjNkZDA0MGZkMTE6NmI2ZjdhODZmYjYzNDMxN2FlMTJhNDBlODA1MDA1MTk='}
	r = requests.post(url, data=values, headers=headers)
	print r.url
	r.raise_for_status()
	return json.loads(r.text)['access_token']




### database
db = pymysql.connect("localhost","spotify","","myrunningsongs",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)
c = db.cursor()

### api token
token_clock = time.time()
token = refresh_token()
# token = 'BQASRM2_p-GIkRD3y0U2P3ljvtWE8A0W84aTNFGzRPlC1hR-hl-KXpbapmM39oUKIbZieQMPUfLu1h80yS5HQA'
print token

### api call
url = 'https://api.spotify.com/v1/search'
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'q' : 'a',
          'type' : 'playlist',
          'limit' : '50',
          'offset':0}
headers = { 'User-Agent' : user_agent ,'Authorization':'Bearer '+token}


f = open('search_terms.txt','rb')
terms = [word.strip() for word in f.readlines()]

# terms = [letter for letter in 'ghijklmnopqrstuvwxyz']

for word in terms:
	next = True
	values['offset'] = 0
	while next:
		values['q'] = word
		try:
			r = requests.get(url, params=values, headers=headers)
			results = json.loads(r.text)
			for playlist in results['playlists']['items']:
				c.execute("""INSERT IGNORE INTO playlists (id,name,user) VALUES (%s,%s,%s)""",(playlist['id'],playlist['name'],playlist['owner']['id']))
			db.commit()
		except:
			print '*'*30
			print r.text
			print '*'*30
			break
		if (time.time() - token_clock) > 3595:
			token_clock = time.time()
			token = refresh_token()
			headers['Authorization'] = 'Bearer '+token
		print values['q'],values['offset'],results['playlists']['total']
		time.sleep(.5)
		next = results['playlists']['next']
		values['offset'] += 50
		

