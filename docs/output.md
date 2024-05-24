We will run an example using [30 Research papers](https://github.com/MrGG14/OpenScience/tree/main/papers) in PDF format.

We just need to execute the 'main.py' file and we obtain: 

- [XMLs generated](https://github.com/MrGG14/OpenScience/tree/main/output)

Then we need to execute 'modelling.ipynb', this program output will be the papers metadata we need in form of a dictionary in the 'papers_metadata.pickle':
- Need information
- Topic modelling
- Similarity score

Once we have the metadata we will use the 'dic_to_rdf.py' program to transform our dictionary into rdf format, and to call the Wikidata API and the ORCID API to enrich our KG.
The output will be save in the 'knowledge_graph_linked.rdf' file. Finally we can use the 'querys.ipynb' to make SPARQL queries to the enrichted KG.
