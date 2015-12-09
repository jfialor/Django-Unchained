import gensim
from gensim import corpora, models, similarities
import numpy as np
#import logging
#logging.basicConfig(format = '%(asctime)s: %(levelname)s : %(message)s', level=logging.INFO)

def QueryTransform(token_list, popularity, releaseyear):

	dot_vector = [-4.239773*float(10^8), -2.797686*float(10^8), -4.409403*float(10^8), -4.383773*float(10^8), -4.104946*float(10^8)]
	dot_vector.append(-4.551056*float(10^8)) 
	dot_vector.append(-4.419971*float(10^8))
	dot_vector.append(-4.284668*float(10^8)) 
	dot_vector.append(-4.637652*float(10^8)) 
	dot_vector.append(-3.811235*float(10^8))
	dot_vector.append(-4.618372*float(10^8))
	dot_vector.append(-4.551732*float(10^8)) 
	dot_vector.append(-4.173811*float(10^8))
	dot_vector.append(-5.078649*float(10^8)) 
	dot_vector.append(-4.414488*float(10^8)) 
	dot_vector.append(-4.977699*float(10^8)) 
	dot_vector.append(-4.564601*float(10^8))
	dot_vector.append(-4.419537*float(10^8)) 
	dot_vector.append(-4.059751*float(10^8)) 
	dot_vector.append(-4.772299*float(10^8)) 
	dot_vector.append(-4.554852*float(10^8)) 
	dot_vector.append(-3.631895*float(10^8)) 
	dot_vector.append(-3.942197*float(10^8)) 
	dot_vector.append(-4.477149*float(10^8))
	dot_vector.append(-4.295874*float(10^8))
	dot_vector.append(-4.518272*float(10^8)) 
	dot_vector.append(-4.051294*float(10^8))
	dot_vector.append(-4.281917*float(10^8))
	dot_vector.append(-4.865829*float(10^8)) 
	dot_vector.append(-4.518636*float(10^8))
	dot_vector.append(-4.648017*float(10^8))
	dot_vector.append(-4.764891*float(10^8)) 
	dot_vector.append(-4.251621*float(10^8)) 
	dot_vector.append(-4.438942*float(10^8)) 
	dot_vector.append(-4.121625*float(10^7)) 
	dot_vector.append(-3.224219*float(10^8))
	dot_vector.append(-4.425289*float(10^8)) 
	dot_vector.append(-4.306247*float(10^8))
	dot_vector.append(-3.975808*float(10^8))
	dot_vector.append(-4.662431*float(10^8)) 
	dot_vector.append(-4.443816*float(10^8))
	dot_vector.append(-4.867457*float(10^8))
	dot_vector.append(-3.851656*float(10^8)) 
	dot_vector.append(-4.658303*float(10^8)) 
	dot_vector.append(-4.271102*float(10^8))
	dot_vector.append(-4.150053*float(10^8)) 
	dot_vector.append(-4.428452*float(10^8))
	dot_vector.append(-4.521024*float(10^8))
	dot_vector.append(-4.679255*float(10^8)) 
	dot_vector.append(-3.739185*float(10^8))
	dot_vector.append(6.529148*float(10^7))
	dot_vector.append(3.827013*float(10^5))

	#projdict = corpora.Dictionary.load('C:\\Users\\Kevin\\Desktop\\CIS550\\CIS550projectDict.dict')
	#tfidf = models.tfidfmodel.TfidfModel.load("C:\\Users\\Kevin\\Desktop\\CIS550\\CIS550projectModelTfidf")
	#lda = models.ldamodel.LdaModel.load("C:\\Users\\Kevin\\Desktop\\CIS550\\CIS550projectModel")
	projdict = corpora.Dictionary.load('CIS550projectDict.dict')
	tfidf = models.tfidfmodel.TfidfModel.load("CIS550projectModelTfidf")
	lda = models.ldamodel.LdaModel.load("CIS550projectModel")
	vector = gensim.corpora.dictionary.Dictionary.doc2bow(projdict, token_list)
	tfidf_vector = tfidf[vector]
	trans_vec = lda[tfidf_vector]

	final_vec = [0]*52

	for i in trans_vec:
		final_vec[i[0]] = i[1]

	final_vec[50] = popularity
	final_vec[51] = releaseyear
	result = np.dot(dot_vector, trans_vec) - 3.490797*float(10^8)
	return result

