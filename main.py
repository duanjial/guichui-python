import requests
from bs4 import BeautifulSoup


def fetchHome(url):
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    book_title = soup.find_all(class_="title")
    book_list = soup.find_all(class_='book-list')
    for index, book in enumerate(book_list):
        chapter_list = book.find_all('a')
        # chapter_list = book.find_all('li').find_children()
        title = book_title[index].h3.a.string
        f = open(title + '.txt', 'a')
        for chapter in chapter_list:
            f.write(chapter.string + "\n")
            # fetchChapter(f, chapter.get('href'))
        print(f"Write {title} successfully!")
        f.close()


def fetchChapter(file, url):
    book_source = requests.get(url)
    soup = BeautifulSoup(book_source.text, 'html.parser')
    chapter_title = soup.find(id='nr_title').string

    file.write(chapter_title + "\n")
    # p_list = soup.find(id='nr1').find_all('p')
    # writeToTxt(file, chapter_title, p_list)


def writeToTxt(file, title, paragraphs):
    for p in paragraphs:
        if p.string is not None:
            file.write(p.string + "\n")


if __name__ == '__main__':
    homeUrl = "https://www.luoxia.com/guichui/"
    fetchHome(homeUrl)