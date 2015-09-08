# -*- coding: utf-8 -*-
#レビュー文抽出
from BeautifulSoup import BeautifulSoup
import sys
import urllib
import urllib2
import unicodedata
import re
import codecs
import csv


def CheckUrl(soup):
    comic_data = soup.find("h2")
    comic_id = comic_data.find("a",href=True)
    pattern = re.compile("/mannga/(.+)/")
    m = pattern.search(comic_id["href"])
    return m.group(1)

def SelectComicId():
    select_comic_id = []
    for i in range(3000,10000):
        url = "http://www.manngareview.com/comics/show/" + str(i) + "/page:1/limit:5/u_sort:modified/netabare:yes"
        htmldata = urllib2.urlopen(url)
        soup = BeautifulSoup(htmldata)
        try:
            pagecount   = soup.find('div',{'id':'comic_data_area'})
            plist = pagecount.findAll('p')
            pattern = re.compile("レビュー数:(.+)人")
            m = pattern.search(str(plist[0]))
            if m:
                review_point = m.group(1)
                if int(review_point) > 20:
                    check_url = CheckUrl(soup)
                    print check_url
                    select_comic_id.append(check_url)

        except AttributeError,e:
            print e
    return select_comic_id

def main():

    select_comic_id_list = SelectComicId()
    f = open("select_comic_id.csv","w")
    csvWriter = csv.writer(f,lineterminator = "\n")
    csvWriter.writerow(select_comic_id_list)
    f.close()

if __name__ == "__main__":
    main()


