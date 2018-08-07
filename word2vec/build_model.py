import gensim, logging, pymysql, re, sys
from nltk.tokenize import TweetTokenizer,word_tokenize
from random import shuffle,sample
from nltk.stem.snowball import EnglishStemmer
from tweetokenize import Tokenizer
import time
import cython
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)
# print gensim.models.doc2vec.FAST_VERSION
# sys.exit()

class PlaylistTracks(object):
	def __init__(self,n_lists=1e10):
		self.db = pymysql.connect("localhost","spotify","","myrunningsongs",charset="utf8mb4",cursorclass=pymysql.cursors.DictCursor)
		self.n_lists = n_lists
		self.playlist_ids = self.playlist_init()
		# self.tknzr = TweetTokenizer(preserve_case=False,reduce_len=True)
		self.tknzr = Tokenizer()
		self.bigram = None

	def random_insert_seq(self,lst, seq):
		insert_locations = sample(xrange(len(lst) + len(seq)), len(seq))
		inserts = dict(zip(insert_locations, seq))
		input = iter(lst)
		lst[:] = [inserts[pos] if pos in inserts else next(input) for pos in xrange(len(lst) + len(seq))]
		return lst

	def playlist_init(self):
		c = self.db.cursor()
		n = c.execute("""SELECT DISTINCT(playlist) p FROM tracks LIMIT %s""",(self.n_lists,))
		# t = time.time()
		# playlist_ids = np.empty(n, dtype="S22")
		# for i,k in enumerate(c.fetchall()):
			# playlist_ids[i] = k
		playlist_ids = [r['p'] for r in c.fetchall()]
		# print 'INIT TIME:',time.time() - t
		# print sys.getsizeof(playlist_ids)
		return playlist_ids

	def preprocess(self,s):
		# return s
		return s.lower().replace('dance party','danceparty').replace('feelgood','feel good').replace('warmup','warm up').replace('barbecue','bbq').replace('barbeque','bbq')

	def text(self):
		c = self.db.cursor()
		for playlist_id in self.playlist_ids:
			c.execute("""SELECT name,description FROM playlists WHERE id=%s""",(playlist_id,))
			plist = []
			r = c.fetchone()
			if r['name']:
				for word in self.tknzr.tokenize(self.preprocess(r['name'].encode('utf8'))):
					plist.append(word)
			if r['description']:
				for word in self.tknzr.tokenize(self.preprocess(r['description'].encode('utf8'))):
					plist.append(word)
			if plist:
				yield plist

	def __iter__(self):
		c = self.db.cursor()
		for playlist_id in self.playlist_ids:
			# t = time.time()
			c.execute("""SELECT name,description,track FROM tracks JOIN playlists ON playlists.id=tracks.playlist WHERE playlist=%s and track > '' ORDER BY playlist,track_num""",(playlist_id,))
			# c.execute("""SELECT track FROM tracks WHERE playlist=%s ORDER BY track_num""",(playlist_id,))
			# print 'QUERY TIME:',time.time()-t
			plist = []
			for r in c.fetchall():					
				plist.append('T_'+r['track'])
			
			# t = time.time()
			if r['name']:
				plist = self.random_insert_seq(plist,self.bigram[self.tknzr.tokenize(self.preprocess(r['name'].encode('utf8')))])
			if r['description']:
				plist = self.random_insert_seq(plist,self.bigram[self.tknzr.tokenize(self.preprocess(r['description'].encode('utf8')))])
			# print 'PROCESS TIME:',time.time()-t
			yield plist

playlists = PlaylistTracks(1e10)
playlists.bigram = gensim.models.Phrases(playlists.text())

# for plist in playlists.text():
	# print playlists.bigram[plist]
# sys.exit()
t = time.time()
model = gensim.models.Word2Vec(playlists, size=100, window=15, min_count=40, workers=4, iter=8)
print 'TOTAL TIME:',time.time()-t
fname = 'models/bbq_002.w2v'
# model.init_sims(replace=True)
model.save(fname)

print model.most_similar(positive=['bbq'])

