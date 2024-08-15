import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin, urlparse
from colorama import init, Fore, Style

# Inicializa colorama
init(autoreset=True)

def crawl_url(base_url, output_file=None):
    try:
        # Realiza una solicitud GET a la URL base
        response = requests.get(base_url)
        response.raise_for_status()  # Lanza un error si la solicitud falla

        # Usa BeautifulSoup para parsear el HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # Obtiene el dominio de la URL base
        base_domain = urlparse(base_url).netloc

        # Encuentra todos los enlaces en la página
        links = soup.find_all('a', href=True)

        # Prepara la salida
        results = []

        # Itera sobre cada enlace y almacena la información si pertenece al mismo dominio y no está vacío
        for link in links:
            link_text = link.get_text(strip=True)
            link_url = urljoin(base_url, link['href']).strip()  # Resuelve enlaces relativos y elimina espacios en blanco

            # Obtiene el dominio del enlace
            link_domain = urlparse(link_url).netloc

            # Solo guarda si el enlace pertenece al mismo dominio y no está vacío
            if link_text and link_url and link_domain == base_domain:
                result = f'{Fore.CYAN}Texto: {Style.BRIGHT}{link_text}\n{Fore.GREEN}URL: {Style.BRIGHT}{link_url}\n{Fore.YELLOW}{Style.DIM}---{Style.RESET_ALL}'
                results.append(result)

        # Muestra los resultados en la consola
        if results:
            print('\n'.join(results))

        # Guarda los resultados en el archivo si se proporciona
        if output_file:
            with open(output_file, 'w') as file:
                file.write('\n'.join([r.strip(Style.RESET_ALL) for r in results]))  # Elimina códigos de color para el archivo
            print(f'{Fore.GREEN}Resultados guardados en: {output_file}')
            
    except requests.RequestException as e:
        print(f'{Fore.RED}Error al acceder a la URL: {e}')

def main():
    # Configura el parser de argumentos
    parser = argparse.ArgumentParser(description='Crawl any URL to extract links from the same domain with colorized output.')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL to crawl')
    parser.add_argument('-o', '--output', type=str, help='File to save the results')
    
    # Parsea los argumentos
    args = parser.parse_args()
    
    # Llama a la función de crawling con la URL proporcionada
    crawl_url(args.url, args.output)

if __name__ == '__main__':
    main()
