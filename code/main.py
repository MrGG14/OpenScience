from grobid_client.grobid_client import GrobidClient
import xml.etree.ElementTree as ET        
import matplotlib.pyplot as plt
import os
import xml.etree.ElementTree as ET
from grobid_client.grobid_client import GrobidClient
from wordcloud import WordCloud
import re 
import shutil


#FUNCS TO OBTAIN WORDCLOUD
def get_abstract(root):
    abstract = root.find('.//{http://www.tei-c.org/ns/1.0}abstract')

    ET.tostring(abstract, encoding='utf8').decode('utf8')
    paragraph = abstract.find('.//{http://www.tei-c.org/ns/1.0}p')
    abstract = paragraph.text
    return abstract

def wordcloud(root):
    abstract = get_abstract(root)
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(abstract)
    return wordcloud
        

# FUNCS TO OBTAIN FIGURE HISTOGRAM    
def count_figs(root):
    figs = root.findall(".//{http://www.tei-c.org/ns/1.0}figure")
    count = len(figs)
    file = file_path.replace("output\\", "")[2:-15]
    file_nfigs = [file, count]
    return file_nfigs

def figs_hist(file_nfigs):
    docs = [item[0] for item in file_nfigs]
    counts = [item[1] for item in file_nfigs]
    plt.figure(figsize=(10, 6))
    plt.bar(docs, counts)

    plt.xlabel('Archivo XML')
    plt.ylabel('Número de Figuras')
    plt.title('Número de Figuras por Archivo XML')
    plt.xticks(rotation=60) 
    plt.xticks(fontsize=6)
    plt.tight_layout()  
    if counts != []:
        plt.savefig("./output/imgs/FigHist/" + 'hist' + ".png")


# FUNCS TO GET LINKS FROM EACH PAPER    
def get_paper_links(root):
    links = []
    if root.text:
        links.extend(re.findall(r'https://\S+', root.text))
    for child in root:
        links.extend(get_paper_links(child))
        if child.tail:
            links.extend(re.findall(r'https://\S+', child.tail))
    return links

# FUNC TO REMOVE DATA FROM PREVIOUS EXECUTIONS
def remove_files(ruta):
    for root, dirs, files in os.walk(ruta):
        for archivo in files:
            ruta_completa = os.path.join(root, archivo)
            os.remove(ruta_completa)


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
            file_nfigs.append(count_figs(root))

            # 3. Get links from each paper
            file_links[file_name] = get_paper_links(root)


    figs_hist(file_nfigs)
    print(file_links)
