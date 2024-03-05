from grobid_client.grobid_client import GrobidClient

import os
import xml.etree.ElementTree as ET
from grobid_client.grobid_client import GrobidClient
# from utils import utils

# Directorio donde se encuentran los archivos XML
directorio = './output'

numero_figuras_paper = []
listado_archivos = []

path = os.getcwd()
# os.chdir('./' + path)

print(path)


# client = GrobidClient(config_path="code/config.json")
# client.process("processFulltextDocument", "./papers", output="./output/", consolidate_citations=True, tei_coordinates=True, n=20)

for file in os.listdir(directorio):
    if file[-3:] == 'xml':
        
# #if __name__ == "__main__":