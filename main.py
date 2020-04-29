import requests
from bs4 import BeautifulSoup
import os


def fetchHome(url):
    source = requests.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    book_title = soup.find_all(class_="title")
    book_list = soup.find_all(class_='book-list')
    current_dir = os.getcwd()

    for index, book in enumerate(book_list):
        chapter_list = book.find_all('a')
        title = book_title[index].h3.a.string
        os.mkdir(title)
        dir = os.path.join(current_dir, title)
        index = 0
        for chapter in chapter_list:
            f = open(os.path.join(dir, str(index) + '.txt'), 'a')
            # f.write(chapter.string + "\n")
            fetchChapter(f, chapter.get('href'))
            index += 1
        print(f"Write {title} successfully!")
        f.close()


def fetchChapter(file, url):
    book_source = requests.get(url)
    soup = BeautifulSoup(book_source.text, 'html.parser')
    chapter_title = soup.find(id='nr_title').string
    print(chapter_title + "\n")
    # file.write(chapter_title + "\n")
    p_list = soup.find(id='nr1').find_all('p')
    writeToTxt(file, p_list)


def writeToTxt(file, paragraphs):
    for p in paragraphs:
        if p.string is not None:
            file.write(p.string + "\n")


if __name__ == '__main__':
    homeUrl = "https://www.luoxia.com/guichui/"
    fetchHome(homeUrl)
