# -*- coding: utf-8 -*-
import mechanize
import cookielib
import argparse
import random
import time
import os
import io
import re
import csv
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from bs4 import BeautifulSoup

urlAutoHome="https://club.autohome.com.cn"

def config():
    """基本判断配置"""
    if os.path.exists("cc.html"):
        os.remove("cc.html")
    if os.path.exists("cc-picon.html"):
        os.remove("cc-piconv.html")
    if os.path.exists("end.xlsx"):
        os.remove("end.xlsx")

def getOptions():
    """解析获取输入参数"""
    parser = argparse.ArgumentParser()
    parser.add_argument("--page", help="获取前多少页的数据;例如获取10页的内容: --page 10", default="1")
    args = parser.parse_args()

    return args

def autoHomePageInfo(page):
    """汽车之家：连接获取分析页面内容，返回soup格式内容"""
    time.sleep(random.randint(1,6))

    br = mechanize.Browser()
    br.set_cookiejar(cookielib.LWPCookieJar())
    br.set_handle_equiv(True)
    br.set_handle_gzip(True)
    br.set_handle_redirect(True)
    br.set_handle_referer(True)
    br.set_handle_robots(False)
    br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
    br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]

    autohomeurl="""https://club.autohome.com.cn/bbs/forum-c-3204-%i.html?orderby=dateline&qaType=-1""" % (int(page))
#    r = br.open("https://club.autohome.com.cn/bbs/forum-c-3204-1.html?orderby=dateline&qaType=-1")
    r = br.open(autohomeurl)
    html = r.read()

    fh = open('cc.html','w')
    fh.write(html)
    fh.close()
 
    os.system("piconv -f \"gbk\" -t \"utf-8\" <cc.html >cc-piconv.html")
    response = open('cc-piconv.html','r+')
    soup = BeautifulSoup(response)
    response.close()

    os.remove("cc.html")
    os.remove("cc-piconv.html")

    return soup

def getAutoHomePostInfo(soup):
    """汽车之家：解析soup格式的网页内容，获取帖子相关信息"""
    dl_c=soup.find_all('dl',lang=re.compile("\|3204\|"))
    for dl in dl_c:
        #print dl.get('lang')
        lang=dl.get('lang')
        huifu_num=lang.split('|')[3]
        time=lang.split('|')[4]
        user_id=lang.split('|')[5]
        user_name=lang.split('|')[10]
        a=lang.split('|')[7]
        b=lang.split('|')[8]
        c=lang.split('|')[9]
        if b == "18":
            class_post="问题贴"
        elif a == "0" and c == "1":
            class_post="图片贴"
        elif a == "3" and c == "1":
            class_post="精华贴"
        elif a == "0" and c == "0":
            class_post="普通贴"
        else:
            class_post="其他"
        url=dl.find('a',href=re.compile("thread"))
        title=url.get_text()
        title_end="".join(title.split())
#        print "帖子链接:" + urlAutoHome + url['href']
#        print "发帖人："+ user_name
#        print "发帖人ID:" + user_id
#        print "发帖时间：" + time
#        print "帖子回复数：" + huifu_num
#        print "帖子标题:" + title_end
        if class_post != "问题贴" and "上海" in title_end and "车友会" in title_end  and "75" in title_end:
            print time + "\t" + title_end + "\t" + urlAutoHome + url['href'] + "\t" + class_post + "\t" + user_name +"\t" + user_id + "\t" + huifu_num
            line =time + "\t" + title_end + "\t" + urlAutoHome + url['href'] + "\t" + class_post + "\t" + user_name +"\t" + user_id + "\t" + huifu_num + "\n"
            ff=io.open('end.xlsx','a', encoding = 'utf-8')
            ff.write(line)
            ff.close()


if __name__=='__main__':
    config()
    args = getOptions()
    numpage = 1
    while numpage <= int(args.page):
        soup = autoHomePageInfo(numpage)
        getAutoHomePostInfo(soup)
        numpage = numpage + 1
