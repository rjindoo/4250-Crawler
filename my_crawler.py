from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup

unvisited_urls = ['https://www.delish.com/']
visited_urls = []
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

def add_path_to_unvisited(path):
    '''
    Add url to queue if it has not been seen 
    and queue capacity is not reached
    '''
    if(len(visited_urls) + len(unvisited_urls) > 10):
        # CRAWL CAPACITY REACHED
        pass
    elif(path not in visited_urls and path not in unvisited_urls):
        unvisited_urls.append(path)

def crawl(url):
    '''
    Get everything within <html></html>
    and iterate over all <a> elements to get links
    '''
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    # !!! Get text and links into a .csv
    for link in soup.find_all('a'):
        path = link.get('href')
        if path.startswith('/'):
            path = urljoin(url, path)
        add_path_to_unvisited(path)

def run():
    '''
    Crawl urls until $unvisited_urls is empty
    Appends crawled urls to $visted_urls
    '''
    while unvisited_urls:
        url = unvisited_urls.pop(0)
        print(f'Crawling {url}')
        try:
            crawl(url)
        except Exception as e:
            print(f'Could not crawl {url}, {e}')
        finally:
            visited_urls.append(url)

run()