# -*-coding:utf-8-*-
import sys
from multiprocessing.dummy import Pool as ThreadPool

import requests
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')

base_url = "https://translate.google.cn/m?hl={}&sl={}&ie=UTF-8&q={}"


def get_html(url):
    try:
        r = requests.get(url, timeout=30)
        r.raise_for_status()
        return r.text
    except:
        print("Get HTML Text Failed!")
        return 0


def translate_en_to_zh(to_translate, from_language="en", to_language="ch-CN"):
    url = base_url.format(to_language, from_language, to_translate[1])  # to_translate要翻译的文本
    if html := get_html(url):
        soup = BeautifulSoup(html, "html.parser")
    try:
        result1 = soup.find_all("div", {"class": "t0"})[0].text  # 解析网页
    except:
        print("Translation Failed!")
        result1 = ""
    print (result1)
    return result1


if __name__ == '__main__':
    sentences = [line.split('   ') for line in open('data_part.txt', 'r')]
    print (len(sentences))

    pool = ThreadPool(9)  # 设置线程池大小，cpu频繁为N+1，IO频繁为2N+1,N为cpu逻辑核数目。
    results = pool.map(translate_en_to_zh, sentences)  # map 线程池
    print (len(results))
    fw = open('train_cn.txt', 'w')
    for item in results:  # 存放结果
        fw.write(item + '\n')
