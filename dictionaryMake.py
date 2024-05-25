import time
import requests
import re
import hashlib
import json
import uuid
nonce = "C7DC5CAD-31CF-4431-8635-B415B75BF4F3"
device_token = str(uuid.uuid4()).upper()
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

headers_PC = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}


def md5_hex(input, case):
    m = hashlib.md5()
    m.update(input.encode())

    if case == 'Upper':
        return m.hexdigest().upper()
    else:
        return m.hexdigest()


def get_catalog(novel):
    chapter = []
    title = ""

    url = f"https://book.sfacg.com/Novel/{novel}/MainIndex/"

    with requests.get(url, headers=headers_PC) as resp:
        links = re.findall(r'<a href="(.*?)" title=', resp.text)
        title = re.findall(r'<h1 class="story-title">(.*?)</h1>', resp.text)[0]
        for link in links:
            chapter_id = link
            if (link.split('/')[1] == "vip"):
                continue
            chapter.append(chapter_id)
    return title, chapter


chr = {}


def download_chapter(chapters):
    global chr
    for chapter in chapters:
        content = ""
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        url = f"https://api.sfacg.com/Chaps/{chapter.split('/')[-2]}?expand=content%2CneedFireMoney%2CoriginNeedFireMoney%2Ctsukkomi%2Cchatlines%2Cisbranch%2CisContentEncrypted%2CauthorTalk&autoOrder=false"
        resp = requests.get(url, headers=headers).json()
        if (resp['status']['httpCode'] == 200):
            if 'content' in resp['data']:
                content += resp['data']['content']
                if 'expand' in resp['data'] and 'content' in resp['data']['expand']:
                    content += resp['data']['expand']['content']
            else:
                content += resp['data']['expand']['content']
            print(f"{resp['data']['title']} 已下载")
        content = ''.join(re.findall(r'[\u4e00-\u9fff]+', content))
        resp = requests.get('https://book.sfacg.com' +
                            chapter, headers=headers_PC)
        content0 = ''.join(re.findall(r'<p>(.*?)</p>', resp.text)[0:-1])
        content0 = ''.join(re.findall(r'[\u4e00-\u9fff]+', content0))
        if (len(content) == len(content0)):
            for i in range(len(content0)):
                if (content[i] in chr and content0[i] == chr[content[i]]):
                    pass
                else:
                    if (content[i] in chr):
                        print(content[i], content0[i], chr[content[i]])
                        print('error\n\n\n\n\n')
                        print(content)
                        print(content0)
                chr[content[i]] = content0[i]
        else:
            print("长度不一致")

    return content


if __name__ == "__main__":
    with open('novelList.txt', 'a') as f:
        f.write('')
    with open('novelList.txt', 'r') as file:
        novels = [line.strip() for line in file]
    for novel in novels:
        title, chapter = get_catalog(novel)
        download_chapter(chapter)

        print(len(chr))
        with open(f'dict.json', 'w', encoding="utf-8") as f:
            f.write(json.dumps(chr, ensure_ascii=False, indent=4))
