from bs4 import BeautifulSoup as bs
from collections import namedtuple
from requests import get


ATRIBUTOS = {
    "base_url": "http://pyjobs.com.br/",
    "jobs": "http://pyjobs.com.br/#oportunidades",
    "jobs_page": "http://pyjobs.com.br/?page="
}


# definindo uma namedtuple
vaga = namedtuple('Vaga', 'title')


def get_last_page(url:str)-> str:
    """
    :param url: referente a pagina inicial do site pyjobs
    :return: o numero maximo de paginas do site, com base na referencia da paginação;
    """
    pyjobs = get(url)
    pyjobs_page = bs(pyjobs.text, 'html.parser')
    links = pyjobs_page.find('ul', {'class': 'pagination'}).find_all('a')
    return max([link.get('href') for link in links])


def format_strs(string:str)->str:
    """
    :param string: string referente a determinados atributos do scrapping page
    :return: string sem espaços.
    """
    # remove o ':' e também os espaçoes, a partir do indice 1
    # return string.split(':')[1].strip()
    return string.strip()


def gen_jobs(url: str)-> namedtuple:
    """
    :param url: determinada url referente
    :return: generator contendo determinadas namedtiples e seus titulos....
    """
    pyjobs = get(url)   #realizada determinada requisição, conforme método http: get.
    pyjobs_page = bs(pyjobs.text, 'html.parser')
    boxes = pyjobs_page.find_all('div', {'class': 'card-body'})

    # capturando os titulos
    for box in boxes:
        title = box.find('h4', {'class': 'card-title'}).text
        yield vaga(format_strs(title))

def get_urls():
    last_page = int(get_last_page(ATRIBUTOS['jobs'])[-1])   # captura o ultimo elemento da lista.
    return ['{}{}'.format(ATRIBUTOS['jobs_page'], n) for n in range(1, last_page + 1)]


for url in get_urls():
    #print(url)
    print(list(gen_jobs(url)))

