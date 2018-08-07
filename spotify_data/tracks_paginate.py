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

c.execute("""SELECT user,id from playlists left join tracks on playlists.id=playlist WHERE track_num=100 and playlist NOT IN (select playlist from tracks where track_num=101)""")

### api token
token_clock = time.time()
token = refresh_token()
# token = 'BQCd-TrXAg_Bs5BYBaeF9uOr-CA9xxaxCoOPkuu9KD459VYUZ2xz5Np-04ZbZuWWnRtRjfIhMeuhdLHXUY3V3w'

### api call
user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64)'
values = {'limit' : '100',
          'offset': '100'}
headers = { 'User-Agent' : user_agent ,'Authorization':'Bearer '+token, 'Accept': 'application/json'}

k = 0

for playlist in c.fetchall():
	url = 'https://api.spotify.com/v1/users/%s/playlists/%s'%(playlist['user'],playlist['id'])
	# next = True
	# values['offset'] = 0
	tnum = 101

	try:
		r = requests.get(url, params=values, headers=headers)
		results = json.loads(r.text)
		# print results
		for track in results['tracks']['items']:
			# print playlist['id'],track['track']['id'],track['track']['artists'][0]['id'],tnum
			c.execute("""INSERT IGNORE INTO tracks (playlist,track,artist,track_num) VALUES (%s,%s,%s,%s)""",(playlist['id'],track['track']['id'],track['track']['artists'][0]['id'],tnum))
			tnum += 1
		if results['description'] == None:
			c.execute("""UPDATE playlists SET description=%s where id=%s""",('',playlist['id']))	
		else:
			c.execute("""UPDATE playlists SET description=%s where id=%s""",(results['description'],playlist['id']))
		db.commit()
		print k,playlist['user'],playlist['id'],results['tracks']['total']
		k += 1
		pass
	except:
		print '*'*30
		print url
		# print r.text
		print '*'*30
	if (time.time() - token_clock) > 3595:
		token_clock = time.time()
		token = refresh_token()
		headers['Authorization'] = 'Bearer '+token
	# next = results['tracks']['next']
		# values['offset'] += 100
		

