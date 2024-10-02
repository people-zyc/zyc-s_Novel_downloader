import os
from bs4 import BeautifulSoup
import subprocess
def get_url_data(url):
    try:
        result = subprocess.run("curl"+url, capture_output=True, text=True, check=True)
        return result.stdout 
    except subprocess.CalledProcessError:
        return "error"
def get_data_text(data):
    soup = BeautifulSoup(data, 'html.parser')
    chapter_div = soup.find('div', id='chaptercontent')
    if chapter_div:return chapter_div.get_text(strip=True, separator='\n')
    else:print("未找到章节内容")
    return -1
def get_data_title(data):
    soup = BeautifulSoup(data, 'html.parser')
    title_h1 = soup.find('h1', class_='wap_none')
    if title_h1:return title_h1.get_text(strip=True)
    else:print("未找到章节标题")
    return -1
def get_data_last_url(data):
    l=(((data.split('\n')[53]).split('最新：<a href=')[1]).split('>')[0])[1:-1]
    return l