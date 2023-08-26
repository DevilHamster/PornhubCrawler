import requests
import urllib.request as request
import time
import random
from lxml import etree
from tqdm import tqdm
import os

'''
本爬虫用于抓取pornhub网站上的gif(短视频)
ps:爬虫仅有一定概率成功,取决于vpn联网速度.vpn需开启全局代理
ps:填写好自己的文件存放路径、User-Agent、cookie、代理ip端口,即可使用
'''

#固定参数设置
Filepath = "" #设置自己的文件存放路径
Main_url = "https://www.pornhub.org/gifs?o=tr" #pornhub短视频主页
port = "" #填写代理ip端口，参数在vpn软件中查看
headers = {
    "User-Agent":""
    ,"cookie":""
    ,"Connection": 'close'
    } #自定义请求头伪装，需填写User-Agent和cookie

#以下是代理ip爬虫的固定写法，注意urllib3库的安装版本需要为1.25.7，否则会报错
proxies = {
    'http': 'http://127.0.0.1:' + port
    , 'https': 'https://127.0.0.1:' + port
    }
opener = request.build_opener(request.ProxyHandler(proxies))
s = requests.session()
s.keep_alive = False
request.install_opener(opener)

#通过一个视频链接下载视频至文件路径的方法
def SingleShortDownload(title, url):
    try:
        if os.path.exists(Filepath + "/" + title + ".mp4"):
            return
        time.sleep(random.uniform(1.0, 2.0)) #防封禁
        mp4_file = requests.get(url=url, headers=headers, proxies=proxies)
        with open(Filepath + "/" + title + ".mp4", "wb")as f:
            f.write(mp4_file.content)
    except:
        print("\nFail to download this video, gonna skip that...\n")

#通过主页链接，获取各帖子的标题和链接
def GetPosts(url, pageCount):
    try:
        #存放视频的标题及链接
        title_list = []
        mp4_list = []
        #生成各页面链接
        page_list = []
        for i in range(1, pageCount+1):
            page_list.append(url + "&page=" + str(i))
        #对每个页面的post进行获取
        for j in tqdm(iterable=range(0,len(page_list)), desc="视频链接获取中,请稍后", unit="page"):
            time.sleep(random.uniform(1.0, 2.0)) #防封禁
            page_info = requests.get(url=page_list[j], headers=headers, proxies=proxies)
            html = etree.HTML(page_info.text)

            #获取视频文件链接和视频标题
            mp4_url = html.xpath("/html/body//li[@class='gifVideoBlock js-gifVideoBlock']//video/@data-mp4")
            titles = html.xpath("/html/body//li[@class='gifVideoBlock js-gifVideoBlock']//span/text()")

            #处理视频标题
            for k in range(0,len(titles)):
                titles[k] = titles[k].strip('\/:*?"<>|')

            mp4_list.extend(mp4_url)
            title_list.extend(titles)

        return title_list, mp4_list
    except:
        print("Video links acquisition failed, please check!")

#爬取3页的内容
title_list, mp4_list = GetPosts(Main_url,3) 
print("Video posts got attached, the length of the list is: " + str(len(mp4_list)))
#逐条下载视频，并实时显示进度条
for q in tqdm(iterable=range(0,len(title_list)), desc="Videos are queued for download, please wait...", unit="file"):
    SingleShortDownload(title_list[q], mp4_list[q])
print("This batch is done...")