import pickle, csv, pandas, regex as re, time
from requests import get
from bs4 import BeautifulSoup

TEST = True

def clean_author(raw):
    parts = re.findall(r'([a-zA-Z.-]+)+', raw)
    for removel in ['Goodreads', 'Author']:
        try:
            parts.remove(removel)
        except Exception as e:
            pass

    return ' '.join(parts)


def clean_isbn(raw):
    num = re.findall(r'(\b[0-9]{10}\b)', raw)
    return num[0]

def clean_pages(raw):
    pages = re.findall(r'([0-9]+) pages',raw)
    return pages[0]

def scrape_detailed_page(url):
    try:
        response = get(url)
    except Exception as e:
        print('Failed to get detailed page.')
        return None


    soup = BeautifulSoup(response.text, 'html.parser')
    item_dict = {}

    try:
        items2 = soup.find_all('div', class_='infoBoxRowItem')
        items1 = soup.find_all('div', class_='infoBoxRowTitle')

        if len(items1) == len(items2):
            for i in range(0,len(items1)):
                    try:
                        if items1[i].text in ['ISBN']:
                            item_dict['ISBN'] = clean_isbn(items2[i].text)
                    except Exception as e:
                        print('failed ISBN')
                        item_dict['ISBN'] = None


                    try:
                        if items1[i].text in ['Edition Language']:
                            item_dict['language'] = items2[i].text
                    except Exception as e:
                        print('failed langguage')
                        item_dict['language'] = None

    except Exception as e:
        print('Failed ISBN or Language')
        item_dict['ISBN'] = None
        item_dict['language'] = None


    try:
        item_dict['format'] = soup.find('span', itemprop='bookFormat').text
    except Exception as e:
        print('Failed book format.')
        item_dict['format'] = None

    try:
        item_dict['pages'] = clean_pages(soup.find('span', itemprop='numberOfPages').text)
    except Exception as e:
        print('Failed pages')
        item_dict['pages'] = None

    return item_dict








def scrape_list_page(url):
    try:
        response = get(url)
    except Exception as e:
        print('Cannot access website.')

    soup = BeautifulSoup(response.text, 'html.parser')

    book_list = []

    book_container = soup.find('div', id='all_votes')

    books = book_container.find_all('tr')

    for book in books:
        book_dict = {}

        try:
            book_dict['title'] = book.find('span', itemprop='name').text
        except Exception as e:
            print('Failed to get book name.')
            book_dict['title'] = None

        try:
            book_dict['author'] = clean_author(book.find('span', itemprop='author').text)
        except Exception as e:
            print('Failed to get book author.')
            book_dict['author'] = None


        try:
            detailedurl = book.find('a', class_='bookTitle', itemprop='url')['href']
            connector = 'https://www.goodreads.com'
            book_dict.update(scrape_detailed_page(connector+detailedurl))

        except Exception as e:
            print('boobs')

        book_list.append(book_dict)
        print('sleeping for 3')
        time.sleep(3)

    return book_list



if __name__ == '__main__':


        url_begin = 'https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page='
        page_val = 198
        book_list_layered = []

        for j in range(1,page_val+1):
            book_list_layered.append(scrape_list_page(url_begin+str(j)))


        pickle.dump(book_list_layered, open('layered_list.pickle', 'wb'))

        
