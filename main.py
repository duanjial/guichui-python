import requests
from bs4 import BeautifulSoup
import os
import re


def fetchHome(url):
    with requests.Session() as se:
        se.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en"
        }
    source = se.get(url)
    soup = BeautifulSoup(source.text, 'html.parser')
    book_title = soup.find_all(class_="title")
    book_list = soup.find_all(class_='book-list')
    current_dir = os.getcwd()
    result = -1
    for index, book in enumerate(book_list):
        # chapter_list = book.find_all('a')
        chapter_list = book.find_all('b')
        title = book_title[index].h3.a.string
        os.mkdir(title)
        dir = os.path.join(current_dir, title)
        index = 0
        for chapter in chapter_list:
            f = open(os.path.join(dir, str(index) + '.txt'), 'a')
            f.write(chapter.string + "\n")
            try:
                if re.match("window.open", chapter["onclick"]):
                    k = chapter["onclick"]
                    # print(k)
                    # print(re.findall('https.*htm', k))
                    x = re.findall('https.*htm', k)
                    if x:
                        result = fetchChapter(f, x[0], index)
            except:
                pass

            index += 1
            if result == 0:
                break
        print(f"Write {title} successfully!")
        f.close()
        if result == 0:
            print("Return with error!!")
            break


def fetchChapter(file, url, index):
    with requests.Session() as chapter_se:
        chapter_se.headers = {
            "User-Agent":
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36",
            "Accept-Encoding": "gzip, deflate",
            "Accept":
            "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "en"
        }
    book_source = chapter_se.get(url)
    soup = BeautifulSoup(book_source.text, 'html.parser')
    chapter_title = soup.find(id='nr_title')
    if chapter_title is not None:
        chapter_title = chapter_title.string
        # file.write(chapter_title + "\n")
        p_list = soup.find(id='nr1').find_all('p')
        writeToTxt(file, p_list)
        return 1
    else:
        print(f"Reading Chapter {index} error!!!")
        return 0


def writeToTxt(file, paragraphs):
    for p in paragraphs:
        if p.string is not None:
            file.write(p.string + "\n")


if __name__ == '__main__':
    homeUrl = "https://www.luoxia.com/guichui/"
    # homeUrl = "https://www.luoxia.com/qing/"
    fetchHome(homeUrl)
