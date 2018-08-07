import gensim, logging, pymysql
from nltk.tokenize import TweetTokenizer
import re,time,sys,operator

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


fname = 'models/model_001bt.w2v'
model = gensim.models.Word2Vec.load(fname)

# print type(model.vocab)
print model['danceparty']
# sys.exit()
# n = 0
# sorted_x = sorted(model.vocab.items(), key=operator.itemgetter(1),reverse=True)
# for k,v in sorted_x:
# 	if not(re.match('T_',k)):
# 		print k,'\t',v
# 		n += 1

# print 'Total words:',n
# sys.exit()

# t = time.time()
# print [w for w in model.most_similar(positive=['danceparty'],topn=100) if not(re.match('T_',w[0]))]

# print time.time()-t

# t = time.time()
# print [w for w in ['running','toilet']*50 if model.vocab]
# print time.time()-t