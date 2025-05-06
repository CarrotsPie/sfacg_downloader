import time
import requests
import re
import hashlib
import json
import uuid
import html
from ebooklib import epub

# 加载字典（特殊字符替换）
with open('dict.json', 'r', encoding='utf-8') as file:
    dictionary = json.load(file)

# 初始化变量
nonce = str(uuid.uuid4()).upper()
tr = False

# 读取或输入 device_token
try:
    with open('deviceToken.txt', 'r', encoding='utf-8') as file:
        device_token = file.read()
except:
    print("deviceToken 可以在重装菠萝包 APP 并随机点开一部小说后的 Android/data/com.sfacg/files/boluobao/log/com.sfacg.log.txt 中找到。\n如果这个文件里有多个 deviceToken，请使用时间更靠后的那一个。")
    device_token = input("输入 deviceToken: ").upper()
    with open('deviceToken.txt', 'w') as file:
        file.write(device_token)
    tr = True

# 常量
SALT = "FN_Q29XHVmfV3mYX"
headers = {
    'Host': 'api.sfacg.com',
    'accept-charset': 'UTF-8',
    'authorization': 'Basic YW5kcm9pZHVzZXI6MWEjJDUxLXl0Njk7KkFjdkBxeHE=',
    'accept': 'application/vnd.sfacg.api+json;version=1',
    'user-agent': f'boluobao/5.0.36(android;32)/H5/{device_token.lower()}/H5',
    'accept-encoding': 'gzip',
    'Content-Type': 'application/json; charset=UTF-8'
}


def md5_hex(input, case):
    m = hashlib.md5()
    m.update(input.encode())
    return m.hexdigest().upper() if case == 'Upper' else m.hexdigest()


def clean_title(title):
    # 去除可能导致目录错误的特殊字符
    return html.escape(re.sub(r'[（）()【】]', '', title).strip())


def get_catalog(novel):
    chapters = {}
    title = ""
    try:
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f'{nonce}{timestamp}{device_token}{SALT}', 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        resp = requests.get(f'https://api.sfacg.com/novels/{novel}', headers=headers).json()
        title = resp['data']['novelName']
    except:
        print("标题获取失败")
        title = "标题获取失败"

    try:
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f'{nonce}{timestamp}{device_token}{SALT}', 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        catalog = requests.get(f'https://api.sfacg.com/novels/{novel}/dirs?expand=originNeedFireMoney', headers=headers).json()
        for volume in catalog['data']['volumeList']:
            chapters[volume['title']] = []
            for chapter in volume['chapterList']:
                chapters[volume['title']].append(chapter['chapId'])
    except:
        print("目录获取失败")
        title = "目录获取失败"
    return title, chapters


def download_chapter(chapters):
    content = ""
    chapter_texts = []  # 用于 EPUB
    for chapter in chapters:
        try:
            timestamp = int(time.time() * 1000)
            sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
            headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
            url = f"https://api.sfacg.com/Chaps/{chapter}?expand=content%2Cexpand.content"
            resp = requests.get(url, headers=headers).json()
            if resp['status']['httpCode'] == 200:
                title = resp['data']['title']
                content += title + '\n'
                tmp = ""
                if 'content' in resp['data']:
                    tmp += resp['data']['content']
                    if 'expand' in resp['data'] and 'content' in resp['data']['expand']:
                        tmp += resp['data']['expand']['content']
                else:
                    tmp += resp['data']['expand']['content']
                text = ''
                for char in tmp:
                    text += dictionary.get(char, char)
                content += text + '\n'
                chapter_texts.append(f"{title}\n{text}")
                print(f"{title} 已下载")
            else:
                print(f"{chapter} 下载失败，请检查是否未订阅该章节")
        except:
            print(f"{chapter} 下载失败，可能是网络问题")
    return content, chapter_texts


def get_cookie(username, password):
    timestamp = int(time.time() * 1000)
    sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
    headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
    data = json.dumps({"password": password, "shuMeiId": "", "username": username})
    resp = requests.post("https://api.sfacg.com/sessions", headers=headers, data=data)
    if resp.json()["status"]["httpCode"] == 200:
        cookie = requests.utils.dict_from_cookiejar(resp.cookies)
        return f'.SFCommunity={cookie[".SFCommunity"]}; session_APP={cookie["session_APP"]}'
    else:
        return "请检查账号或密码是否错误"


def save_as_epub(title, chapters_text):
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language('zh')

    spine = ['nav']
    toc = []
    for i, text in enumerate(chapters_text):
        raw_title = text.splitlines()[0]
        title_line = clean_title(raw_title)
        body_lines = text.splitlines()[1:]
        c = epub.EpubHtml(title=title_line, file_name=f'chap_{i+1}.xhtml', lang='zh')
        c.content = f"<h2>{title_line}</h2><p>{'</p><p>'.join(body_lines)}</p>"
        book.add_item(c)
        toc.append(c)
        spine.append(c)

    book.toc = tuple(toc)
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(f"{title}.epub", book, {})


if __name__ == "__main__":
    novel = input("输入小说ID: ")
    username = input("输入手机号: ")
    password = input("输入密码: ")
    headers['cookie'] = get_cookie(username, password)
    if headers['cookie'] == "请检查账号或密码是否错误":
        print("请检查账号或密码是否错误")
    else:
        title, chapters = get_catalog(novel)
        if title in ['标题获取失败', '目录获取失败']:
            exit()
        print(title)
        i = 0
        for volume in chapters:
            i += 1
            print(i, ':', volume)
        tot = i
        tr = True
        while tr:
            down = input("请输入需要下载的卷号(如 1,3-5，不输入则全下载): ")
            try:
                downList = []
                if down == '':
                    downList = list(range(1, tot + 1))
                else:
                    for part in down.split(','):
                        if '-' in part:
                            start, end = map(int, part.split('-'))
                            downList.extend(range(start, end + 1))
                        else:
                            downList.append(int(part))
                downList = list(set(downList))
                tr = False
            except:
                print('卷号输入错误，请重新输入')
        print("计划下载卷:", downList)

        i = 0
        content = title + '\n\n'
        all_texts = []
        for volume in chapters:
            i += 1
            if i in downList:
                print('正在下载:', volume)
                content += volume + '\n\n'
                vol_text, chap_texts = download_chapter(chapters[volume])
                content += vol_text
                all_texts.extend(chap_texts)

        title_clean = re.sub(r'[\\/:*?"<>|]', ' ', title)
        with open(f'{title_clean}{downList}.txt', 'w', encoding="utf-8") as f:
            f.write(content)

        save_as_epub(title_clean, all_texts)
        print(f"已保存为 TXT 和 EPUB：{title_clean}.txt / {title_clean}.epub")
