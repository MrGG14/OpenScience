from grobid_client.grobid_client import GrobidClient

import os
import xml.etree.ElementTree as ET
from grobid_client.grobid_client import GrobidClient
from utils import utils

# Directorio donde se encuentran los archivos XML
directorio = './output/papers'
numero_figuras_paper = []
listado_archivos = []

client = GrobidClient(config_path="./config.json")
client.process("processFulltextDocument", ".", output="./output/", consolidate_citations=True, tei_coordinates=True, n=20)
#if __name__ == "__main__":