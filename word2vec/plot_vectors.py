import gensim, logging, pymysql
from nltk.tokenize import TweetTokenizer
import re,time,sys,operator
from sklearn.decomposition import PCA
import pylab as plt
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.manifold import TSNE
from tsne import bh_sne

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

fname = 'models/model_001bt.w2v'
model = gensim.models.Word2Vec.load(fname)

ss = StandardScaler()
_tsne = TSNE(n_components=2,random_state=0, learning_rate=1000, method='exact')
_pca = PCA(n_components=50)

# print type(model.vocab)
X = []
for key in ['chill','party','workout','hangout']:
	X.append(model[key])

for key in ['sleep','relax','focus','pregame','danceparty','late_night','warm_up','gym','cardio','dinner','feel_good','bbq']:
	X.append(model[key])

k = 0	
for key in model.vocab:
	X.append(model[key])
	k += 1
	if k == 2500:
		break
	# print model.vocab[key].index

X = np.array(X,dtype=float)
X = ss.fit_transform(X)
X = _pca.fit_transform(X)
X = _tsne.fit_transform(X)
# print X

# print np.mean(X,axis=0)	
# X = np.array([[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]],dtype=float)

fig = plt.figure()
ax = fig.add_subplot(111)

k = 0
offset = .2
for activity in ['chill']:
	x,y = X[k,:]
	print activity,x,y
	ax.annotate(activity, xy=(x, y), xytext=(x+offset, y+offset))
	k += 1
	ax.plot(x,y,'o',color="#0000FE",markersize=15)

for activity in ['party']:
	x,y = X[k,:]
	print activity,x,y
	ax.annotate(activity, xy=(x, y), xytext=(x+offset, y+offset))
	k += 1
	ax.plot(x,y,'o',color="#FFAA01",markersize=15)

for activity in ['workout']:
	x,y = X[k,:]
	print activity,x,y
	ax.annotate(activity, xy=(x, y), xytext=(x+offset, y+offset))
	k += 1
	ax.plot(x,y,'o',color="#FF00FF",markersize=15)

for activity in ['hangout']:
	x,y = X[k,:]
	print activity,x,y
	ax.annotate(activity, xy=(x, y), xytext=(x+offset, y+offset))
	k += 1
	ax.plot(x,y,'o',color="#00C98A",markersize=15)

for activity in ['sleep','relax','focus']:
	x,y = X[k,:]
	print activity,x,y
	ax.annotate(activity, xy=(x, y), xytext=(x+offset, y+offset))
	k += 1
	ax.plot(x,y,'o',color="#0066FF",markersize=10)

for activity in ['pregame','danceparty','late_night']:
	x,y = X[k,:]
	print activity,x,y
	ax.annotate(activity, xy=(x, y), xytext=(x+offset, y+offset))
	k += 1
	ax.plot(x,y,'o',color="#FFE001",markersize=10)

for activity in ['warm_up','gym','cardio']:
	x,y = X[k,:]
	print activity,x,y
	ax.annotate(activity, xy=(x, y), xytext=(x+offset, y+offset))
	k += 1
	ax.plot(x,y,'o',color="#FF73FF",markersize=10)

for activity in ['dinner','feel_good','bbq']:
	x,y = X[k,:]
	print activity,x,y
	ax.annotate(activity, xy=(x, y), xytext=(x+offset, y+offset))
	k += 1
	ax.plot(x,y,'o',color="#2FE7B1",markersize=10)		
plt.show()

