from grobid_client import grobid_client

# Inicializar el cliente Grobid
client = grobid_client.GrobidClient("http://localhost:8080/api", batch=True)

# Obtener los 10 artículos de Grobid
def get_grobid_articles():
    articles = []
    for i in range(10):
        url = f"https://doi.org/10.5068/D1{1000 + i:03d}"
        article = client.process("processFulltextDocument", {"input": url})
        articles.append(article)
    return articles

# Extraer palabras clave del resumen
def extract_keywords(article):
    return article['abstract']

# Crear un WordCloud de palabras clave
def create_wordcloud(keywords):
    from wordcloud import WordCloud
    import matplotlib.pyplot as plt
    
    wordcloud = WordCloud(width=800, height=400, background_color ='white').generate(' '.join(keywords))
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Contar el número de figuras por artículo
def count_figures(article):
    return len(article['figures'])

# Obtener los enlaces de un artículo
def get_links(article):
    return article['links']

# Proceso principal
def main():
    articles = get_grobid_articles()

    # Analizar palabras clave
    all_keywords = []
    for article in articles:
        keywords = extract_keywords(article)
        all_keywords.extend(keywords)
    create_wordcloud(all_keywords)

    # Visualizar el número de figuras por artículo
    figures_count = [count_figures(article) for article in articles]
    import matplotlib.pyplot as plt
    plt.bar(range(1, 11), figures_count)
    plt.xlabel('Article')
    plt.ylabel('Number of Figures')
    plt.title('Number of Figures per Article')
    plt.show()

    # Listar enlaces por artículo
    for i, article in enumerate(articles, 1):
        print(f"Links for Article {i}:")
        links = get_links(article)
        for link in links:
            print(link)
        print()

if __name__ == "__main__":
    main()
