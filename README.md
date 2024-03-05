# OpenScience
[![DOI](https://zenodo.org/badge/762679154.svg)](https://zenodo.org/doi/10.5281/zenodo.10702188)

 ## Description

Repository for Artificial Intelligence And Open Science. The aim of this repository is to create a Gobrid client which will perform an analysis over 10
open-access articles and will:

- Draw a keyword cloud based on the words found in the abstract of your papers.
  
- Create a visualization showing the number of ﬁgures per article.
  
- Create a list of the links found in each paper.



 ## Requirements
- Python >= 3.5

- Gobrid library (uses requests as dependency beyond the Standard Python Library).
 
 ## Installation instructions
First of all you need to install Gobrid from Docker as specified in [Gobrid´s containers documentation](https://grobid.readthedocs.io/en/latest/Grobid-docker/). CRF-only image is recomended.

To install initialize the docker daemon and execute: 
```
docker pull lfoppiano/grobid:0.8.0
```


 
 ## Execution instructions
Initilize Gobrid (Docker must be running): 
```
docker run --rm --init --ulimit core=0 -p 8070:8070 lfoppiano/grobid:0.8.0
```

Once Gobrid is up and running you just need to execute the 'main.py' file. 
 ## Running example(s)
 ## Preferred citation 
 Read CFF
 ## Where to get help
Gobrid´s documentation [here](https://github.com/kermitt2/grobid_client_python)
 ## Acknowledgements (if any)
