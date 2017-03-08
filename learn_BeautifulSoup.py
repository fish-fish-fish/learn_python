#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import urlparse
import bs4
from bs4 import BeautifulSoup
from bs4 import UnicodeDammit
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def takeSummary(url):
    html = requests.get(url)
    if not html:
        return
    soup = BeautifulSoup(html.text, "html.parser")
    title = soup.title.string
    summary = soup.select_one('.x-wiki-content').find(name="h3",string="小结")
    if not summary:
        return None
    content = ""
    for line in summary.next_siblings:
        if line.name == "h3":
            break;
        if isinstance(line,bs4.element.Tag):
            for txt in line.strings:
                content += txt
            content += "\n"
    return title + "小结:\n" + content

host = "http://www.liaoxuefeng.com"
mainUrl = "http://www.liaoxuefeng.com/wiki/0013739516305929606dd18361248578c67b8067c8c017b000"
mainPage = requests.get(mainUrl)
soup = BeautifulSoup(mainPage.text,"html.parser")
lis = soup.select(".x-sidebar-left-content ul li a")
for li in lis:
    newUrl = urlparse.urljoin(host, li["href"])
    print(takeSummary(newUrl))
print("提取完毕")