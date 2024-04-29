from grobid_client.grobid_client import GrobidClient
import xml.etree.ElementTree as ET        
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud
import re 
import sys
import gensim
from gensim import corpora, models, similarities
import os
from stop_words import get_stop_words

#si no hace bien los imports de utilsdescomenta esta linea
sys.path.append(os.path.abspath(os.getcwd())) 
from utils import remove_files, get_abstract



if __name__ == "__main__":

    xml_dir = './output'

    remove_files(xml_dir)

    client = GrobidClient(config_path="code_KG/config.json")
    client.process("processFulltextDocument", "./papers", output="./output/", consolidate_citations=True, tei_coordinates=True, n=20)
    
# GET ABSTRACTS
    abstracts = []
    for file in os.listdir(xml_dir):
        if file[-3:] == 'xml':
            file_path = os.path.join(xml_dir, file)
            tree = ET.parse(file_path)
            root = tree.getroot()
            abstract = get_abstract(root)           
            abstracts.append(abstract)

    # print(abstracts)  



# SIMILARITY
textos = [resumen.split() for resumen in abstracts]

diccionario = corpora.Dictionary(textos)

corpus=[diccionario.doc2bow(texto) for texto in textos]

tfidf = models.TfidfModel(corpus)

index = similarities.MatrixSimilarity(tfidf[corpus])

for i in range(len(textos)):
    for j in range(i+1, len(textos)):
        vec_i = diccionario.doc2bow(textos[i])
        vec_j = diccionario.doc2bow(textos[j])
        sim_ij = index[tfidf[vec_i]][j]
        print(f'La similitud entre el documento {i+1} y el documento {j+1} es sim {sim_ij}')


# TOPIC MODELLING

stop_words = get_stop_words('english')
keywords = [[word for word in resumen.lower().split() if word.isalpha() and word not in stop_words] for resumen in abstracts]
dictionary = corpora.Dictionary(keywords)
doc_term_matrix = [dictionary.doc2bow(title) for title in keywords]

LDA = gensim.models.ldamodel.LdaModel

lda_model = LDA(corpus = doc_term_matrix, id2word=dictionary, num_topics=7, random_state=100, chunksize=1000, passes=50)

temas = lda_model.print_topics(num_words=5)
for tema in temas:
    print(tema)