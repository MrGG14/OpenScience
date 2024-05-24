## Installation instructions
First of all you need to install Gobrid from Docker as specified in [Gobrid´s containers documentation](https://grobid.readthedocs.io/en/latest/Grobid-docker/). CRF-only image is recomended.

To install initialize the docker daemon and execute: 
```
docker pull lfoppiano/grobid:0.8.0
```

Then you should clone this repository locally with:
```
git clone
```

Finally, you may need to install the necessary packages to run the code. In order to do this go to the github cloned repo through the CMD and go to the '/docs' folder (cd docs). Now just run:

```
pip install -r requirements.txt
```

 You can also install Gobrid´s client for python following the [instructions](https://github.com/kermitt2/grobid_client_python).
