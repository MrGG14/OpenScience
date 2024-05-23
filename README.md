# OpenScience
[![DOI](https://zenodo.org/badge/762679154.svg)](https://zenodo.org/doi/10.5281/zenodo.10702188)
[![Documentation Status](https://readthedocs.org/projects/openscience/badge/?version=latest)](https://openscience.readthedocs.io/en/latest/?badge=latest)


 ## Description

Repository for Artificial Intelligence And Open Science. The aim of this repository is to create a Gobrid client which will perform an analysis over 30
open-access articles and:

- Extract metadata such as abstract, authors, publication date, referenced authors and organizactions.
  
- Compare papers assigning a similitude metric between them.
  
- Topic modelling using LDA.

-  Make local Knlowledge Graph in RDF.

-  Expanding our Knowledge Graph with external information.




 ## Requirements
- Python >= 3.5

- Gobrid library (uses requests as dependency beyond the Standard Python Library).

- Docker
 ## Installation instructions
First of all you need to install Gobrid from Docker as specified in [Gobrid´s containers documentation](https://grobid.readthedocs.io/en/latest/Grobid-docker/). CRF-only image is recomended.

To install initialize the docker daemon and execute: 
```
docker pull lfoppiano/grobid:0.8.0
```

Then you should clone this repository locally.

Finally, you may need to install the necessary packages to run the code. In order to do this go to the github cloned repo through the CMD and go to the '/docs' folder (cd docs). Now just run:

```
pip install -r requirements.txt
```

 You can also install Gobrid´s client for python following the [instructions](https://github.com/kermitt2/grobid_client_python).
 
 ## Execution instructions

 ### LOCALLY
Initilize Gobrid: 

Once Gobrid is up and running you just need to place the papers you want to analyze in the 'papers' folder.

Finally just execute the 'main.py' file. The outputs generated will be in the 'output' folder.

After doing that we have to run the 'modelling.ipynb', which would collect and process all the data we need to create our KG, storing it in 'papers_metadata.pickle'file.

Once you have the dictionary created you have to run the 'dict_to_rdf.py' file, this file will convert all the information collected in the previous part to rdf format, it will also enrich our KG with information from Wikidata and ORCID, using their APIs, storing the KG in the 'knowledge_graph_linked.rdf' file.

Lastly you need to use the 'querys.ipynb' program to run queries from any SPARQL query web.


 ## Running example 
We will run an example using [10 Deep Learning papers](https://github.com/MrGG14/OpenScience/tree/main/papers) in PDF format located in the 'papers' folder.

We just need to execute the main.py file and we obtain: 

- [XMLs generated](https://github.com/MrGG14/OpenScience/tree/main/output)

After doing that we have to run the 'modelling.ipynb', whic
 
 ## Preferred citation 
 Read [CFF](https://github.com/MrGG14/OpenScience/blob/main/CITATION.cff)
 ## Where to get help
Gobrid´s documentation [here](https://github.com/kermitt2/grobid_client_python)
Docker´s documentation [here](https://docs.docker.com/manuals/)
 ## Problems
There seems to be a problem to install Gobrid´s python client from Docker. In the Dockerfile we try to install it following Gobrid´s steps (setup.py install) and directly with pip and neither of them seem to install it correctly. However locally works with both, we dont know where this error must come from. 
