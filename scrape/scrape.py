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

    try:
        item_dict['cover_pic'] = soup.find('img', id='coverImage')['src']
    except Exception as e:
        print('imgurl error')
        item_dict['cover_pic'] = None

    try:
        genres = soup.find_all('div', class_='elementList')
        list = []
        i=0
        j=0
        while i < len(genres) and j < 3:
            if genres[i].find('a', class_='actionLinkLite bookPageGenreLink') is not None:
                list.append(genres[i].find('a', class_='actionLinkLite bookPageGenreLink').text)
                i += 1
                j += 1
            else:
                i += 1
        item_dict['genres'] = list

    except Exception as e:
        print(e)
        print('genre error')
        item_dict['genres'] = None

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

def to_csv(list,fname,cols):

    df = pandas.DataFrame(list)
    f = open(fname, 'w')
    df.to_csv(f, sep=',', encoding='utf-8',columns=cols, index=False)



def start_scraping():
    url_begin = 'https://www.goodreads.com/list/show/264.Books_That_Everyone_Should_Read_At_Least_Once?page='
    page_val = 198
    book_list_layered = []

    for j in range(1,page_val+1):
        book_list_layered.append(scrape_list_page(url_begin+str(j)))


    print(book_list_layered)
    pickle.dump(book_list_layered, open('layered_list.pickle', 'wb'))


def layered_to_csv():
    list = pickle.load(open('layered_list.pickle', 'rb'))
    fin_list = [l[i] for l in list for i in range(0,len(l))]
    to_csv(fin_list, 'books.csv', ['title', 'author', 'ISBN', 'language', 'pages', 'cover_pic', 'genres'])


if __name__ == '__main__':


    list = pickle.load(open('layered_list.pickle', 'rb'))
    fin_list = [l[i] for l in list for i in range(0,len(l))]

    genres = []
    titles = []
    for thing in fin_list:
        titles.append(thing['title'])
        for genre in thing['genres']:
            genres.append(genre)

    genre_set = set(genres)
    title_set = set(titles)
    for tit in title_set:
        #clean titles "" -> ''
        tit = tit.replace('"',"'")


    with open('titles.txt','w') as f:
        for tit in title_set:
            f.write('"' + tit + '"' + '\t:\tnull,\n')
