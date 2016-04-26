import gensim, logging, pymysql
from nltk.tokenize import TweetTokenizer
from random import shuffle

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


class PlaylistTracks(object):
	def __init__(self,n_lists=1e10):
		self.db = pymysql.connect("localhost","spotify","","myrunningsongs",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)
		self.n_lists = n_lists
		self.playlist_ids = self.playlist_init()
		self.tknzr = TweetTokenizer()

	def playlist_init(self):
		c = self.db.cursor()
		c.execute("""SELECT DISTINCT(playlist) p FROM tracks LIMIT %s""",(self.n_lists,))
		return [r['p'] for r in c.fetchall()]

	def __iter__(self):
		c = self.db.cursor()
		for playlist_id in self.playlist_ids:
			c.execute("""SELECT name,description,track,track_num FROM tracks,playlists WHERE playlists.id=playlist and playlist=%s ORDER BY playlist,track_num""",(playlist_id,))
			plist = []
			first = True
			for r in c.fetchall():
				if first:
					first = False
					if r['name']:
						plist.extend(self.tknzr.tokenize(r['name'].lower()))
					if r['description']:
						plist.extend(self.tknzr.tokenize(r['description'].lower()))
					plist.append('T_'+r['track'])
					
				else:
					plist.append('T_'+r['track'])
			shuffle(plist)
			yield plist

playlists = PlaylistTracks()

model = gensim.models.Word2Vec(playlists, size=100, window=10, min_count=30, workers=6)

fname = 'models/sample_shuffle.w2v'
model.init_sims(replace=True)
model.save(fname)

print model.most_similar(positive=['running'])