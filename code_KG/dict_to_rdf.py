from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, FOAF, RDFS
import pickle
import os

# Obtener el directorio del archivo actual
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)


# Cargar el diccionario desde el archivo
with open('./papers_metadata.pickle', 'rb') as f:
    papers = pickle.load(f)


# Crear un grafo RDF. LO HACE AUTOMATICAMENTE Y HAY QUE REFINARLO. NO ESTA BIEN AUN
g = Graph()

# Definir un namespace para los términos específicos del diccionario
vocab = Namespace("http://example.org/vocab/")

# Iterar sobre las claves del diccionario y agregar triples RDF al grafo
for key, value in papers.items():
    # Agregar el título como el sujeto principal
    subject = URIRef(vocab[key.replace(" ", "_")])
    g.add((subject, RDF.type, FOAF.Document))
    g.add((subject, vocab.title, Literal(key)))
    
    # Agregar el abstract como objeto
    g.add((subject, vocab.abstract, Literal(value['abstract'])))
    
    # Agregar los autores como objetos vinculados
    for author in value['written_by']:
        author_uri = URIRef(vocab[author.replace(" ", "_")])
        g.add((subject, vocab.author, author_uri))
        g.add((author_uri, RDF.type, FOAF.Person))
        g.add((author_uri, FOAF.name, Literal(author)))
        
    # Agregar las organizaciones como objetos vinculados
    for org in value['acknowledgeOrg']:
        org_uri = URIRef(vocab[org.replace(" ", "_")])
        g.add((subject, vocab.organization, org_uri))
        g.add((org_uri, RDF.type, FOAF.Organization))
        g.add((org_uri, FOAF.name, Literal(org)))
        
    # Agregar las probabilidades de los temas como objetos vinculados
    for topic, prob in value['topics_prob'].items():
        topic_uri = URIRef(vocab[topic.replace(" ", "_")])
        g.add((subject, vocab.topic, topic_uri))
        g.add((topic_uri, RDF.type, vocab.Topic))
        g.add((topic_uri, RDFS.label, Literal(topic)))
        g.add((topic_uri, vocab.probability, Literal(prob)))

# Serializar y guardar el grafo RDF
g.serialize("knowledge_graph.rdf", format="xml")
