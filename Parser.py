import requests
from bs4 import BeautifulSoup
import re

mails = set()
phones = set()
pages = set()
pagesTwo = set()
allPages = set()

def getHref():
    print("Начинаю обрабатывать стартовую страницу!\n")
    global pages
    global pagesTwo
    global allPages
    size = 0
    sizeTwo = 0
    session = requests.Session()
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome","Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}
    url = "https://ru.wikipedia.org"
    req = session.get(url, headers=headers)  
    bsObj = BeautifulSoup(req.content, 'html.parser')
    for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:                
                newPage = link.attrs['href']
                pages.add(newPage)
    print("На стартовой странице обнаружено ссылок: ",len(pages))
    print("Начинаю обход ссылок....")
    for i in pages:        
        urlRange = "https://ru.wikipedia.org"+i
        req = session.get(urlRange, headers=headers)  
        bsObj = BeautifulSoup(req.content, 'html.parser')
        for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages:                
                    newPage = link.attrs['href']
                    pagesTwo.add(newPage)
    unionPage()

def unionPage():
    global pages
    global pagesTwo
    global allPages
    allPages = pages.union(pagesTwo)
    print("Общее колличество ссылок: ",len(allPages))
    parse()

def parse():
    global mails
    global phones
    global allPages
    print("Начинаю обработку информации: ")
    session = requests.Session()
    headers = {"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5)AppleWebKit 537.36 (KHTML, like Gecko) Chrome","Accept":"text/html,application/xhtml+xml,application/xml; q=0.9,image/webp,*/*;q=0.8"}
    for i in allPages:
        url = "https://ru.wikipedia.org"+i
        req = session.get(url, headers=headers)
        bsObj = BeautifulSoup(req.content, 'html.parser')
        try:
            textPage = bsObj.find("div", id="bodyContent").text
        except AttributeError:
            print("This page is missing something!")
        try:
            for email in re.findall("([A-Za-z0-9\._+-]+@[A-Za-z]+\.+[a-z]{2,6})",textPage):
                if not email==None:
                    if email not in mails:
                        mails.add(email)
                        print("Email: ",email)        
        except AttributeError:
            print("This page is missing something!")
        try:
            for phone in re.findall("\d{0,1}[- ]\d{3}[- ]\d{3}[- ]\d{4}",textPage):
                if not phone==None:
                    if phone not in phones:
                        phones.add(phone)
                        print("Phone: ",phone)
        except AttributeError:
            print("This page is missing something!")
    print("The end!")

getHref() 