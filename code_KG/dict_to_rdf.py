from rdflib import Graph, URIRef, Literal, Namespace
from rdflib.namespace import RDF, OWL
import pickle
import os
import requests

def get_orcid_uri(nombre):
    url = "https://pub.orcid.org/v3.0/search"
    headers = {
        "Accept": "application/json"
    }
    params = {
        "q": f"given-names:{nombre} OR family-name:{nombre}"
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    if 'result' in data:
        return data['result'][0]['orcid-identifier']['uri']
    else:
        return None
    
def get_wikidata_uri(nombre):
    url = "https://www.wikidata.org/w/api.php"
    params = {
        "action": "wbsearchentities",
        "search": nombre,
        "language": "en",
        "format": "json"
    }
    response = requests.get(url, params=params)
    data = response.json()
    if len(data['search']) > 0:
        return 'https:' + data['search'][0]['url']
    return None

def quitar_espacios(cadena):
    return cadena.replace(' ', '_')
    

# Obtener el directorio del archivo actual
current_directory = os.path.dirname(os.path.abspath(__file__))
os.chdir(current_directory)

# Cargar el diccionario desde el archivo
with open('./papers_metadata.pickle', 'rb') as f:
    papers = pickle.load(f)


# Definir namespaces
SCHEMA = Namespace("http://schema.org/")
EXAMPLE = Namespace("http://example.org/")

# Crear grafo RDF
g = Graph()

# Iterar sobre el diccionario
for paper_title, paper_info in papers.items():
    # Crear URI para el paper
    paper_uri = EXAMPLE[quitar_espacios(paper_title)]

    # Agregar triples para el paper
    g.add((paper_uri, RDF.type, SCHEMA.Paper))
    g.add((paper_uri, SCHEMA.Title, Literal(paper_title)))
    g.add((paper_uri, SCHEMA.abstract, Literal(paper_info['abstract'])))
    g.add((paper_uri, SCHEMA["ID"], Literal(paper_info['id'])))
    if paper_info.get('published_date'):
        g.add((paper_uri, SCHEMA["Publication_Date"], Literal(paper_info['published_date'])))

    # Agregar relaciones para los autores
    for author_name in paper_info['written_by']:
        author_uri = EXAMPLE[quitar_espacios(author_name)]
        g.add((paper_uri, SCHEMA.author, author_uri))
        g.add((author_uri, RDF.type, SCHEMA.Person))
        g.add((author_uri, SCHEMA.name, Literal(author_name)))
        author_wikidata = get_wikidata_uri(author_name)
        author_orcid = get_orcid_uri(author_name)
        if author_wikidata:
            g.add((author_uri, OWL.sameAs, URIRef(author_wikidata)))
        #if author_orcid:
            #g.add((author_uri, OWL.sameAs, URIRef(author_orcid)))

    # Agregar relaciones para las organizaciones
    for org_name in paper_info['acknowledgeOrg']:
        org_uri = EXAMPLE[quitar_espacios(org_name)]
        g.add((paper_uri, SCHEMA.acknowledgesOrg, org_uri))
        g.add((org_uri, RDF.type, SCHEMA.Organization))
        g.add((org_uri, SCHEMA.name, Literal(org_name)))
        org_wikidata = get_wikidata_uri(org_name)
        org_orcid = get_orcid_uri(org_name)
        if org_wikidata:
            g.add((org_uri, OWL.sameAs, URIRef(org_wikidata)))
        if org_orcid:
            g.add((org_uri, OWL.sameAs, URIRef(org_orcid)))

    # Agregar relaciones para las las personas reconocidas
    for ack_person in paper_info['acknowledgePerson']:
        ack_person_uri = EXAMPLE[quitar_espacios(ack_person)]
        g.add((paper_uri, SCHEMA.acknowledgesPerson, ack_person_uri))
        g.add((ack_person_uri, RDF.type, SCHEMA.Person))
        g.add((ack_person_uri, SCHEMA.name, Literal(ack_person)))
        """ack_person_wikidata = get_wikidata_uri(ack_person)
        ack_person_orcid = get_orcid_uri(ack_person)
        if ack_person_wikidata:
            g.add((ack_person_uri, OWL.sameAs, URIRef(ack_person_wikidata)))
        if ack_person_orcid:
            g.add((ack_person_uri, OWL.sameAs, URIRef(ack_person_orcid)))"""

    # Agregar relaciones para las probabilidades de temas
    for topic_name, probability_percentage in paper_info['topics_prob'].items():
        if probability_percentage > 0.7:
            topic_uri = EXAMPLE[quitar_espacios(topic_name)]
            g.add((paper_uri, SCHEMA.hasTopic, topic_uri))
            g.add((topic_uri, RDF.type, SCHEMA.Topic))
            g.add((topic_uri, SCHEMA.name, Literal(topic_name)))

    # Agregar relaciones de similitud con otros papers
    try:
        for similar_paper_title, similarity_percentage in paper_info['has_Similarity'].items():
            similar_paper_uri = EXAMPLE[quitar_espacios(similar_paper_title)]
            g.add((paper_uri, SCHEMA.isSimilar, similar_paper_uri))
            g.add((similar_paper_uri, RDF.type, SCHEMA.Paper))
    except:
        print(f'El paper {paper_title} no tiene ningun otro paper que haya superado el umbral de similitud.')

# Serializar y guardar el grafo RDF
g.serialize("knowledge_graph_linked.rdf", format="xml")
