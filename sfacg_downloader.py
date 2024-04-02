import time
import requests
import re
import hashlib
import json

nonce = "C7DC5CAD-31CF-4431-8635-B415B75BF4F3"
device_token = "192E221C-120E-3120-B3B6-62CB913B9D66"
SALT = "FN_Q29XHVmfV3mYX"
headers={
    'Host': 'api.sfacg.com',
    'accept-charset': 'UTF-8',
    'authorization': 'Basic YW5kcm9pZHVzZXI6MWEjJDUxLXl0Njk7KkFjdkBxeHE=',
    'accept': 'application/vnd.sfacg.api+json;version=1',
    'user-agent': 'boluobao/5.0.36(android;32)/H5/192e221c-120e-3120-b3b6-62cb913b9d66/H5',
    'accept-encoding': 'gzip',
    'Content-Type': 'application/json; charset=UTF-8'
}

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
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    url = f"https://book.sfacg.com/Novel/{novel}/MainIndex/"
    
    with requests.get(url, headers=headers) as resp:
        links = re.findall(r'<a href="(.*?)" title=', resp.text)
        title = re.findall(r'<h1 class="story-title">(.*?)</h1>',resp.text)[0]
        for link in links:
            chapter_id = link.split('/')[-2]
            chapter.append(chapter_id)
    return title,chapter

def download_chapter(chapters):
    content = ""
    for chapter in chapters:
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        url = f"https://api.sfacg.com/Chaps/{chapter}?expand=content%2CneedFireMoney%2CoriginNeedFireMoney%2Ctsukkomi%2Cchatlines%2Cisbranch%2CisContentEncrypted%2CauthorTalk&autoOrder=false"
        resp = requests.get(url, headers=headers).json()
        if(resp['status']['httpCode'] == 200):
            content += resp['data']['title'] + '\n'
            if 'content' in resp['data']:
                content += resp['data']['content']
                if 'expand' in resp['data'] and 'content' in resp['data']['expand']:
                    content += resp['data']['expand']['content']
            else:
                content += resp['data']['expand']['content']
            content += '\n'
            print(f"{resp['data']['title']} 已下载")
        else:
            print(f"{chapter} 下载失败，请检查是否未订阅该章节")
    return content

def get_cookie(username, password):
    timestamp = int(time.time() * 1000)
    sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
    headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
    data = json.dumps({"password":password, "shuMeiId":"","username":username})
    url = "https://api.sfacg.com/sessions"
    resp = requests.post(url, headers = headers,data = data)
    if(resp.json()["status"]["httpCode"] == 200):
        cookie = requests.utils.dict_from_cookiejar(resp.cookies)
        return f'.SFCommunity={cookie[".SFCommunity"]}; session_APP={cookie["session_APP"]}'
    else:
        return "请检查账号或密码是否错误"

if __name__ == "__main__":
    novel = input("输入小说ID:")
    username = input("输入手机号:")
    password = input("输入密码:")
    headers['cookie'] = get_cookie(username, password)
    print(headers['cookie'])
    if (headers['cookie'] == "请检查账号或密码是否错误"):
        print("请检查账号或密码是否错误")
    else:
        title, chapter = get_catalog(novel)
        content = title + '\n\n' +download_chapter(chapter)
        with open(f'{title}.txt','w',encoding = "utf-8") as f:
            f.write(content)