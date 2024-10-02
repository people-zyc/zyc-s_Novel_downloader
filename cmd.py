import os
import get
import re
import subprocess
from concurrent.futures import ThreadPoolExecutor
command={}
command_trigger_words=[]
# 从指定文件中读取插件列表并解析，将插件名和其对应的命令保存到字典中，并将插件名添加到触发词列表中
#如无指定文件，则创建一个空文件
with open("C/Uesrs/zyc's_Novel_downloader/addon.list", 'r', encoding='utf-8') as f:
    addons = f.read().split('===')
    for addon in addons:
        command[addon.split('|')[0]] = addon.split('|')[1]
        command_trigger_words.append(addon.split('|')[0])
def remove_ads(text):
    return re.sub(r"请收藏本站.*\n*|$.*?$", "", text)
down_folder = os.path.join(os.path.dirname(__file__), 'down')
txt_folder = os.path.join(os.path.dirname(__file__), 'txt')
os.makedirs(down_folder, exist_ok=True)
os.makedirs(txt_folder, exist_ok=True)

def download_file(book_id, chapter):
    url = f'https://www.3bqg.cc/book/{book_id}/{chapter}.html'
    output_file = os.path.join(down_folder, f'{chapter}.html')
    command = f'curl -o "{output_file}" "{url}"'
    try:
        subprocess.run(command, shell=True, check=True)
        print(f"成功下载: {chapter}.html")
    except subprocess.CalledProcessError as e:
        print(f"下载失败: {chapter}.html (错误: {e})")
print('欢迎使用zyc的小说下载器，本下载器基于网站https://www.3bqg.cc/,仅供学习交流使用。')
a = input(">>>")
if a.split(' ')[0] == 'turn':
    if len(a.split(' ')) == 1:
        print('error,必须为以上命令指定参数。')
        exit()
    for i in range(1, int(a.split(' ')[1]) + 1):
        try:
            input_filename = os.path.join(down_folder, f'{i}.html')
            print(f"检查文件: {input_filename}")
            if os.path.exists(input_filename):
                with open(input_filename, 'r', encoding='utf-8') as f:
                    content = f.read()
                content = remove_ads(content)
                output_filename = os.path.join(txt_folder, get.get_data_title(content) + '.txt')
                print(f"创建输出文件: {output_filename}")
                with open(output_filename, 'w', encoding='utf-8') as f2:
                    f2.write(get.get_data_text(content))
            else:
                print(f"文件 {input_filename} 不存在。")
        except Exception as e:
            print(f"发生错误: {e}")

elif a.split(' ')[0]  == 'down':
    if len(a.split(' ')) < 3:
        print('error,必须为以上命令指定参数。')
        exit()
    chapters = range(1, a.split(' ')[2] + 1)
    with ThreadPoolExecutor(max_workers=128) as executor:
        executor.map(lambda chapter: download_file(a.split(' ')[1], chapter), chapters)
elif a == 'exit':
    exit()
elif a == 'help':
    print('The commands list')
    print('turn [number]:\t将下载的html文件转换为txt文件，并保存到txt文件夹，number为转换的数量。')
    print('down [book_id] [number]:\t下载指定小说的第1章到第number章的内容。')
    print('exit:\t退出程序。')
    print('help:\t显示帮助信息。')
    print('命令插件列表：')
    for i in command_trigger_words:
        print('/t',endl='')
        print(i,endl='\t')
        print(command[i])
        print('\n')
else:
    falg=0
    for _ in command_trigger_words:
        if a.split(' ')[0] == i:
            exec(command[i])
            falg=1
            break
    if falg==0:
        print("命令不存在，请检查输入是否正确。")