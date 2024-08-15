import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin

def crawl_url(url):
    try:
        # Realiza una solicitud GET a la URL
        response = requests.get(url)
        response.raise_for_status()  # Lanza un error si la solicitud falla

        # Usa BeautifulSoup para parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Encuentra todos los enlaces en la página
        links = soup.find_all('a', href=True)

        # Itera sobre cada enlace y muestra la información
        for link in links:
            link_text = link.get_text(strip=True)
            link_url = urljoin(url, link['href'])  # Resuelve enlaces relativos
            print(f'Texto: {link_text}')
            print(f'URL: {link_url}')
            print('---')
    except requests.RequestException as e:
        print(f'Error al acceder a la URL: {e}')

def main():
    # Configura el parser de argumentos
    parser = argparse.ArgumentParser(description='Crawl any URL to extract links.')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL to crawl')
    
    # Parsea los argumentos
    args = parser.parse_args()
    
    # Llama a la función de crawling con la URL proporcionada
    crawl_url(args.url)

if __name__ == '__main__':
    main()
