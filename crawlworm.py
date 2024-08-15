import requests
from bs4 import BeautifulSoup
import argparse
from urllib.parse import urljoin, urlparse
from colorama import init, Fore, Style


init(autoreset=True)

def crawl_url(base_url, output_file=None):
    try:
        
        response = requests.get(base_url)
        response.raise_for_status()  

       
        soup = BeautifulSoup(response.content, 'html.parser')

        
        base_domain = urlparse(base_url).netloc

        
        links = soup.find_all('a', href=True)

    
        results = []

        for link in links:
            link_text = link.get_text(strip=True)
            link_url = urljoin(base_url, link['href']).strip() 

            
            link_domain = urlparse(link_url).netloc

            
            if link_text and link_url and link_domain == base_domain:
                result = f'{Fore.CYAN}Texto: {Style.BRIGHT}{link_text}\n{Fore.GREEN}URL: {Style.BRIGHT}{link_url}\n{Fore.YELLOW}{Style.DIM}---{Style.RESET_ALL}'
                results.append(result)

        
        if results:
            print('\n'.join(results))

        
        if output_file:
            with open(output_file, 'w') as file:
                file.write('\n'.join([r.strip(Style.RESET_ALL) for r in results])) 
            print(f'{Fore.GREEN}Resultados guardados en: {output_file}')
            
    except requests.RequestException as e:
        print(f'{Fore.RED}Error al acceder a la URL: {e}')

def main():
    parser = argparse.ArgumentParser(description='Crawl any URL to extract links from the same domain with colorized output.')
    parser.add_argument('-u', '--url', type=str, required=True, help='URL to crawl')
    parser.add_argument('-o', '--output', type=str, help='File to save the results')
    
    args = parser.parse_args()
    
    crawl_url(args.url, args.output)

if __name__ == '__main__':
    main()
