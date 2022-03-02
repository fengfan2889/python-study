#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Date    : 2019-08-29 21:17:36
# @Author  : Kaiyan Zhang (kaiyanzh@outlook.com)
# @Link    : https://github.com/iseesaw
# @Version : v1.0
"""
将csdn博客导出为markdown
方法：
1. 编辑博客，抓包
2. 获取博客markdown格式链接
https://mp.csdn.net/mdeditor/getArticle?id=100125817
3. 模拟请求
Request Headers
:authority: mp.csdn.net
:method: GET
:path: /mdeditor/getArticle?id=100125817
:scheme: https
accept: */*
accept-encoding: gzip, deflate, br
accept-language: zh-CN,zh;q=0.9,zh-TW;q=0.8
cookie: uuid_tt_dd=10_7363320700-1563628438907-864526; dc_session_id=10_1563628438907.833516; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_7363320700-1563628438907-864526!5744*1*qq_36962569!1788*1*PC_VC; UN=qq_36962569; smidV2=20190712194742cdeda8c033ea9ef003a9a0003c79154a00358928f445b7b50; UserName=qq_36962569; UserInfo=3a33c991856940a79235b113cb42ff0d; UserToken=3a33c991856940a79235b113cb42ff0d; UserNick=%E5%AD%90%E8%80%B6; AU=5A5; BT=1566296770044; p_uid=U000000; TINGYUN_DATA=%7B%22id%22%3A%22-sf2Cni530g%23HL5wvli0FZI%22%2C%22n%22%3A%22WebAction%2FCI%2FpostList%252Flist%22%2C%22tid%22%3A%22e0a1148715d862%22%2C%22q%22%3A0%2C%22a%22%3A42%7D; ViewMode=list; aliyun_webUmidToken=T9204DD7B1A1971E571EFE43913410386D4C2C9D905BA336A2BEDBC206D; hasSub=true; c_adb=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1567074771,1567083797,1567083801,1567084099; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1567084279; dc_tos=px01z9
referer: https://mp.csdn.net/mdeditor/100125817
sec-fetch-mode: cors
sec-fetch-site: same-origin
user-agent: 
Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.87 Safari/537.36
Query String Parameters
id=100125817
"""
import json
from operator import concat
import uuid
import time
import requests
import datetime
from bs4 import BeautifulSoup
from os.path import join,exists
import os
from utils import Parser


def request_blog_list(page=1):
    """获取博客列表
    主要包括博客的id以及发表时间等
    """
    url = f'https://blog.csdn.net/fengfan/article/list/{page}'

    headers = {
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0',
        'Host':'blog.csdn.net',
        'Accept':'*/*'

    }
    
    print(url)
    reply = requests.get(url,headers=headers)
    print(reply.text)
    f = open('test.txt', 'w')
    f.write(reply.text)
    f.close()
    parse = BeautifulSoup(reply.content, "html.parser")
    spans = parse.find_all('div', attrs={'class':'article-item-box csdn-tracking-statistics'})
    blogs = []
    for span in spans:
        try:
            href = span.find('a', attrs={'target':'_blank'})['href']
            #read_num = span.find('span', attrs={'class':'num'}).get_text()
            date = span.find('span', attrs={'class':'date'}).get_text()
            blog_id = href.split("/")[-1]
            blogs.append([blog_id, date, 0])
        except:
            print('Wrong, ' + href)
    return blogs

def request_md(blog_id, date):
    """获取博客包含markdown文本的json数据"""
    url = f"https://blog.csdn.net/fengfan/article/details/{blog_id}"
    headers = {
        #"cookie": "uuid_tt_dd=10_7363320700-1563628438907-864526; dc_session_id=10_1563628438907.833516; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_7363320700-1563628438907-864526!5744*1*qq_36962569!1788*1*PC_VC; UN=qq_36962569; smidV2=20190712194742cdeda8c033ea9ef003a9a0003c79154a00358928f445b7b50; UserName=qq_36962569; UserInfo=3a33c991856940a79235b113cb42ff0d; UserToken=3a33c991856940a79235b113cb42ff0d; UserNick=%E5%AD%90%E8%80%B6; AU=5A5; BT=1566296770044; p_uid=U000000; TINGYUN_DATA=%7B%22id%22%3A%22-sf2Cni530g%23HL5wvli0FZI%22%2C%22n%22%3A%22WebAction%2FCI%2FpostList%252Flist%22%2C%22tid%22%3A%22e0a1148715d862%22%2C%22q%22%3A0%2C%22a%22%3A42%7D; ViewMode=list; aliyun_webUmidToken=T9204DD7B1A1971E571EFE43913410386D4C2C9D905BA336A2BEDBC206D; hasSub=true; c_adb=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1567074771,1567083797,1567083801,1567084099; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1567084279; dc_tos=px01z9",
        #"cookie": "uuid_tt_dd=10_7363320700-1563628438907-864526; dc_session_id=10_1563628438907.833516; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_7363320700-1563628438907-864526!5744*1*qq_36962569!1788*1*PC_VC; UN=qq_36962569; smidV2=20190712194742cdeda8c033ea9ef003a9a0003c79154a00358928f445b7b50; UserName=qq_36962569; UserInfo=3a33c991856940a79235b113cb42ff0d; UserToken=3a33c991856940a79235b113cb42ff0d; UserNick=%E5%AD%90%E8%80%B6; AU=5A5; BT=1566296770044; p_uid=U000000; hasSub=true; c_adb=1; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1567171221,1567173255,1567173925,1567173939; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1567174790; dc_tos=px1ztc",
        "cookie": "uuid_tt_dd=10_18727735060-1642656776191-866137; log_Id_pv=81; log_Id_view=295; Hm_lvt_6bcd52f51e9b3dce32bec4a3997715ac=1646116353,1646116448,1646116958,1646118985; Hm_up_6bcd52f51e9b3dce32bec4a3997715ac=%7B%22islogin%22%3A%7B%22value%22%3A%221%22%2C%22scope%22%3A1%7D%2C%22isonline%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22isvip%22%3A%7B%22value%22%3A%220%22%2C%22scope%22%3A1%7D%2C%22uid_%22%3A%7B%22value%22%3A%22fengfan%22%2C%22scope%22%3A1%7D%7D; Hm_ct_6bcd52f51e9b3dce32bec4a3997715ac=6525*1*10_18727735060-1642656776191-866137!5744*1*fengfan; __gads=ID=a9c482c0d67278c9-22d6e47708d00054:T=1642656822:S=ALNI_MaFINBuuncooBaifclxMUb0-PAiPw; log_Id_click=48; ssxmod_itna=GqIx9Qi=D=9tDXFG7GTH4Du0mbqDOIDRx4Qqe3xGXEPYDZDiqAPGhDC4+/oq8e0=1RDCpK4Ft77p0xLAm2BEanCFc4eDHxY=DUrYcdDxhq0rD74irDDxD3DbfdDSDWKD9D0RSBc6yKGWDmR8DGeDe6FODY5DhxDCRjPDwx0CL6iKOjIhkEY1b35xKt2eLxG1W40HomfItf3LOeB3px0kc40O9ryz1ooDUBKsyPAodj4YX0aHDiF6DCvpBDDaL=rKVIxDMj9Rt0=DBgDe/epNGQbKeQiKdCi3K7Dixh4ioGpNamxDi11PrD4iYD==; ssxmod_itna2=GqIx9Qi=D=9tDXFG7GTH4Du0mbqDOIDRx4QqeA6nP0rD/YRKxFO83wIGBg1+tymP/D8k0diPXGmKGF/=gBXGo7/nKGkzpMSe6oq808bXeqXcoW6Tu+tg4zU6ot5h9xXTwj9SuscQoMF4XA/M5ReM3xTl5xNS3e=mIP8T23qnNDcoTQdWuZ/M63VxLdyC+f83xktLoMAnub2oTOh3rOqbLIKGc3dpyR8RD8KzE1ErF1d67pvjb3HlXhPWH3wWTkVTFw/wRCct6QLrBQvZoAzlInFc7zkfIGH6oOsQoH6E3UG=rMOHys84jBTB3qHRIxEr4YGm/W/4yoiuZtiexP45WBtDQbRf04FQDQjqxzuiGel/5Rj2emW2DrAYK//TYs9EbmcQPOb5=rw8meMB53dYiNg/mTigOt+WtlEO8qW8qOlw10OQW+FFcOUfsR8O3aHn4pl8eaT3D07G0DTApubeDdqpSjEc5533jbFGA3ubm03qW8eBiUSDeMPFAR5xgxKhQGDddW14x7hYpO00uO84hKqBx+22K0RW3eD7=DY9mui5YDQR0=8QYFAf=0mraEHu40M594tKRKj6WKG3a1jHGUuQzTLUprfPRI=DLu5Yl6DD; _ga_VHSCGE70LW=GS1.1.1643363159.5.0.1643363159.0; _ga=GA1.1.1227394529.1643264084; UN=fengfan; BT=1645086571094; p_uid=U010000; c_dl_prid=1645148334230_756604; c_dl_rid=1645604187033_357975; c_dl_fref=https://www.csdn.net/tags/Mtjagg3sMzEwMjItYmxvZwO0O0OO0O0O.html; c_dl_fpage=/download/weixin_38679233/14090634; c_dl_um=-; FCNEC=[[\"AKsRol-5n4twxBwug5JlqC4Z_gs2u6iAM1_xnYGieSTPpQckvvQ4MoVxCMvcjXYhLXYiBluSjxtp427zhC0Z_QXHi22HYsv6ZVg-eaj9ZXBMrP2zdalOzCvDTpN5VNojOybhasPCKSntojF9fsAKcqoJYhRfdxYGkA==\"],null,[]]; dc_session_id=10_1646115109584.932804; dc_sid=e01ad2906f2e24862d4e1622f406b992; c_pref=default; c_ref=default; c_first_ref=www.baidu.com; c_first_page=https%3A//blog.csdn.net/weixin_42218582/category_8993774.html; c_segment=9; dc_tos=r821qe; Hm_lpvt_6bcd52f51e9b3dce32bec4a3997715ac=1646119238; SESSION=bf48005f-6616-4a2f-b6c6-e611f6f993e4; c_page_id=default",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:97.0) Gecko/20100101 Firefox/97.0"
    }
    reply = requests.get(url, headers=headers)

    soup = BeautifulSoup(reply.content, 'html.parser', from_encoding="utf-8")
    title = soup.find_all('h1', {'class': 'title-article'})[0].string  ## 使用 html 的 title 作为 md 文件名
    title = '_'.join(title.replace('*', '').strip().split())
    if not exists("doc"):
        os.makedirs("doc")    
    md_file = join("doc", title + '.md')
    print('Export Markdown File To {}'.format(md_file))
    for child in soup.find_all('svg'):
        child.extract()
    html = "" 
    for c in soup.find_all('div', {'class': 'article-title-box'}):
        html += str(c)
    for c in soup.find_all('div', {'id': 'content_views'}):
        html += str(c)

    parser = Parser(html)
    with open(md_file, 'w',encoding="utf-8") as f:
        f.write('{}\n'.format(''.join(parser.outputs)))
        f.write('tag:csdn\n')
        f.write('{}{}-{}-{}-\n'.format('date:' , date[0],date[1],date[2]))

def main(total_pages=7):
    """
    获取博客列表，包括id，时间
    获取博客markdown数据
    保存hexo格式markdown
    """
    blogs = []
    #for page in range(1, total_pages + 1):
    blogs.extend(request_blog_list(1))
    print(blogs)
    for blog in blogs:
        blog_id = blog[0]
        date = blog[1].split(" ")[0].split("-")
        request_md(blog_id, date)
        time.sleep(1)

if __name__ == '__main__':
    main()