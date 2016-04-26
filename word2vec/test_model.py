import gensim, logging, pymysql
from nltk.tokenize import TweetTokenizer
import re

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)


fname = 'models/sample_shuffle.w2v'
model = gensim.models.Word2Vec.load(fname)


print [w for w in model.most_similar(positive=['running','T_2Ze0YvSXz8CnC81hw5rXNo'],topn=100) if (re.match('T_',w[0]))]