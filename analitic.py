from login import driver
from bs4 import BeautifulSoup
import json


url_models = 'https://3ddd.ru/user/models'
url_module = 'https://3ddd.ru/user/sell_rating'


def get_count_page(url):
    driver.get(url)
    html_file = driver.page_source
    soup = BeautifulSoup(html_file, "html.parser")
    count = str() # Check words in string
    try:
        count_text = soup.find('div', attrs={'class': 'count'}).text
    except Exception as exc:
        count = 1
    
    if(count != 1):
        for c in count_text:
            if c.isdigit():
                count += c
    return int(count)

def module_parse(url): # Read module info
    pages_count = get_count_page(url)
    links_text = []
    for page in range(1, pages_count + 1):
        driver.get(url + '?page=' + str(page))
        html_file2 = driver.page_source
        soup2 = BeautifulSoup(html_file2, "html.parser")
        table_sell = soup2.find('tbody')
        links = table_sell.find_all('a')
        

    for link in links:
        links_text.append(link.text.replace('\n', '').strip())
    return links_text

links_text = module_parse(url_module)

def take_hrefs(url):
    driver.get(url)
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    items = soup.find_all('div', attrs={'class': 'item'})

    links_items = []
    for l in items:
        links_items.append('https://3ddd.ru/3dmodels/show/' + l['data-slug'])

    with open(f'__pycache__/earlier_sells.json') as file:
        data = json.load(file)
        data['models'] = len(links_items)
        with open(f'__pycache__/earlier_sells.json', 'w') as file:
            json.dump(data, file, indent=3)

    return links_items

hrefs = take_hrefs(url_models)

def sort_model(hrefs, links_text): 
    links_items = [''] * len(links_text)
    for h in hrefs:
        driver.get(h)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        name = soup.find('h1').text.replace('\n', '').strip()
        name = name[0:-3]
        j = 0
        while j < len(links_text):
            if(name == links_text[j]):
                links_items[j] = h
            j+=1
    print(links_items)
    return links_items

model_sorted = sort_model(hrefs, links_text)


def dict_models(hrefs):

    dict_m = {
        'make_data': [],
        'render': [],
        'size': []
    }
    for h in hrefs:
        driver.get(h)
        html = driver.page_source
        soup = BeautifulSoup(html, "html.parser")
        table = soup.find('tbody')

        dict_m['make_data'].append(f" {table.find_all('tr')[3].find_all('td')[1].text} ")
        dict_m['render'].append(table.find_all('tr')[1].find_all('td')[1].text)
        dict_m['size'].append(table.find_all('tr')[2].find_all('td')[1].text)

    return dict_m

models_info = dict_models(model_sorted)