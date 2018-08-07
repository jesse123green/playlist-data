import gensim, logging, pymysql
from nltk.tokenize import TweetTokenizer
import re,time,sys,operator
import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


fname = 'models/bbq_002.w2v'
model = gensim.models.Word2Vec.load(fname)
# model.sort_vocab()
# # sys.exit()
# # print type(model.vocab)
# print model.estimate_memory()
# sorted_x = sorted(model.vocab.items(), key=operator.itemgetter(1),reverse=True)
# for k,v in sorted_x:
# 	if not(re.match('T_',k)):
# 		# print k,'\t',v
# 		del model.vocab[k]

fname = 'models/bbq_002t.w2v'
# model.finalize_vocab()
print type(model.syn0)
# model.syn0 = np.array([])
# model.syn1neg = np.array([])
model.syn1neg = None
# print model.vocab['dance']
# model.init_sims(replace=True)
# print model.estimate_memory()
# model.save_word2vec_format(fname, fvocab=None, binary=True)
# model.scale_vocab()
print model.estimate_memory()
model.save(fname)