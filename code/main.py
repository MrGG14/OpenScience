from grobid_client.grobid_client import GrobidClient
import xml.etree.ElementTree as ET        
import matplotlib.pyplot as plt
import os
from wordcloud import WordCloud
import re 
import re 
import sys
sys.path.append(os.path.abspath(os.getcwd())) #si no hace bien los imports descomenta esta linea

from utils import remove_files, wordcloud,count_figs, get_paper_links, figs_hist




if __name__ == "__main__":

    xml_dir = './output'

    remove_files(xml_dir)

    client = GrobidClient(config_path="code/config.json")
    client.process("processFulltextDocument", "./papers", output="./output/", consolidate_citations=True, tei_coordinates=True, n=20)
  

    file_nfigs = []
    file_links = {}

    for file in os.listdir(xml_dir):
        if file[-3:] == 'xml':
            file_path = os.path.join(xml_dir, file)
            tree = ET.parse(file_path)
            root = tree.getroot()
            file_name = file_path.replace("output\\", "")[2:-15]

            # 1. Plot WordCloud
            wcloudimg = wordcloud(root)
            wcloudimg.to_file("./output/imgs/WordCloud/" + file_name + ".png")

            # 2. Count figures for each paper
            file_nfigs.append(count_figs(root,file_path))

            # 3. Get links from each paper
            file_links[file_name] = get_paper_links(root)


    figs_hist(file_nfigs)
    print(file_links)
