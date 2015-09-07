# -*- coding: utf-8 -*-
#レビュー文抽出
from BeautifulSoup import BeautifulSoup
import sys
import urllib
import urllib2
import unicodedata
import re
import codecs

def GetImage(soup,title):
    for i in soup.findAll("div",{"id":"comic_image"}):
        image = i.find("img")["src"] 
        try:
            urllib.urlretrieve(image,"masterthesis_image/" + title + ".jpg")
        except IOError as error:
            print error

def iteration(url):
    htmldata = urllib2.urlopen(url)
    soup = BeautifulSoup(htmldata)
    
    comic_title = soup.find('div',{'id':'comic_info_module_head'}).text
    pagecount   = soup.find('div',{'id':'comic_data_area'})

    get_image = GetImage(soup,comic_title)
    plist = pagecount.findAll('p')
    pattern = re.compile("レビュー数:(.+)人")
    print comic_title #タイトル名
    m = pattern.search(str(plist[0]))
    if m:
        review_point = m.group(1)
        if int(review_point)%5 == 0:
            return int(review_point),(int(review_point)/5+1),comic_title
        else:
            return int(review_point),(int(review_point)/5+2),comic_title

def abstraction(user_number,iteration_count):
    word  = []
    user_count = []
    print iteration_count #回数
    user_count.append(str(user_number))
    print str(user_number)
    for i in range(1,int(iteration_count)):
        url2 = "http://www.manngareview.com/comics/show/3988/page:"+ str(i) +"/limit:5/u_sort:modified/netabare:yes"
        #"+ str(i) +"
        try:
            htmldata2 = urllib2.urlopen(url2)
            soup = BeautifulSoup(htmldata2)
            for review_sentence in soup('p',{'class':'review_string'}):
                print review_sentence.text #本文
                word.append(review_sentence.text)
        except urllib2.HTTPError,e:
            print e.code,e.msg
        except urllib2.URLError,e:
            print e
    return user_count,word

def main():
    url = "http://www.manngareview.com/comics/show/3988/page:1/limit:5/u_sort:modified/netabare:yes"
    iteration_count = iteration(url)
    review_abstraction = abstraction(iteration_count[0],iteration_count[1])
    s_data = codecs.open("masterthesis_review/"+ iteration_count[2] +".txt","w","utf-8")
    for i in review_abstraction[0]:
        s_data.write(i + "\n")
    for i in review_abstraction[1]:
        s_data.write(i + "\n")
    s_data.close()

if __name__ == "__main__":
    main()




