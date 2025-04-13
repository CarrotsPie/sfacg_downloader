import time
import requests
import re
import hashlib
import json
import uuid

with open('dict.json', 'r', encoding='utf-8') as file:
    dictionary = json.load(file)
nonce = str(uuid.uuid4()).upper()
tr =False
try:
    with open('deviceToken.txt','r',encoding='utf-8') as file:
        device_token = file.read()  
except:
    print("deviceToken可以在重装菠萝包APP并随机点开一部小说后的Android/data/com.sfacg/files/boluobao/log/com.sfacg.log.txt中找到,\n如果这个文件里有多个deviceToken，请使用时间更靠后的那一个")
    device_token = input("输入deviceToken:")
    device_token = device_token.upper()
    with open('deviceToken.txt','w') as file:
        file.write(device_token)
    tr = True
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

    if case == 'Upper':
        return m.hexdigest().upper()
    else:
        return m.hexdigest()


def get_catalog(novel):
    chapters = {}
    title = ""
    try:
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f'{nonce}{timestamp}{device_token}{SALT}','Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        resp = requests.get(f'https://api.sfacg.com/novels/{novel}?expand=chapterCount%2CbigBgBanner%2CbigNovelCover%2CtypeName%2Cintro%2Cfav%2Cticket%2CpointCount%2Ctags%2CsysTags%2Csignlevel%2Cdiscount%2CdiscountExpireDate%2CtotalNeedFireMoney%2Crankinglist%2CoriginTotalNeedFireMoney%2Cfirstchapter%2Clatestchapter%2Clatestcommentdate%2Cessaytag%2CauditCover%2CpreOrderInfo%2CcustomTag%2Ctopic%2CunauditedCustomtag%2ChomeFlag%2Cisbranch%2Cessayawards', headers=headers).json()
        title = resp['data']['novelName']
    except:
        print("标题获取失败")
        title = "标题获取失败"
    try:
        timestamp = int(time.time() * 1000)
        sign = md5_hex(f'{nonce}{timestamp}{device_token}{SALT}','Upper')
        headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
        catalog = requests.get(
            f'https://api.sfacg.com/novels/{novel}/dirs?expand=originNeedFireMoney', headers=headers).json()
        for volume in catalog['data']['volumeList']:
            chapters[volume['title']]=[]
            for chapter in volume['chapterList']:
                chapters[volume['title']].append(chapter['chapId'])
    except:
        print("目录获取失败")
        title = "目录获取失败"
    return title, chapters


def download_chapter(chapters):
    content = ""
    for chapter in chapters:
        try:
            timestamp = int(time.time() * 1000)
            sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
            headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
            url = f"https://api.sfacg.com/Chaps/{chapter}?expand=content%2CneedFireMoney%2CoriginNeedFireMoney%2Ctsukkomi%2Cchatlines%2Cisbranch%2CisContentEncrypted%2CauthorTalk&autoOrder=false"
            resp = requests.get(url, headers=headers).json()
            if (resp['status']['httpCode'] == 200):
                content += resp['data']['title'] + '\n'
                tmp = ""
                warn = ""
                if 'content' in resp['data']:
                    tmp += resp['data']['content']
                    if 'expand' in resp['data'] and 'content' in resp['data']['expand']:
                        tmp += resp['data']['expand']['content']
                else:
                    tmp += resp['data']['expand']['content']
                for char in tmp:
                    if char in dictionary:
                        content += dictionary[char]
                    else:
                        content += char
                content += '\n' + warn
                print(f"{resp['data']['title']} 已下载")
            else:
                print(f"{chapter} 下载失败，请检查是否未订阅该章节")
        except:
            print(f"{chapter} 下载失败,可能是网络问题")
    return content


def get_cookie(username, password):
    timestamp = int(time.time() * 1000)
    sign = md5_hex(f"{nonce}{timestamp}{device_token}{SALT}", 'Upper')
    headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={device_token}&sign={sign}'
    data = json.dumps(
        {"password": password, "shuMeiId": "", "username": username})
    url = "https://api.sfacg.com/sessions"
    resp = requests.post(url, headers=headers, data=data)
    if (resp.json()["status"]["httpCode"] == 200):
        cookie = requests.utils.dict_from_cookiejar(resp.cookies)
        return f'.SFCommunity={cookie[".SFCommunity"]}; session_APP={cookie["session_APP"]}'
    else:
        return "请检查账号或密码是否错误"


if __name__ == "__main__":
    novel = input("输入小说ID:")
    username = input("输入手机号:")
    password = input("输入密码:")
    headers['cookie'] = get_cookie(username, password)
    if (headers['cookie'] == "请检查账号或密码是否错误"):
        print("请检查账号或密码是否错误")
    else:
        title, chapters = get_catalog(novel)
        if title =='标题获取失败' or title =='目录获取失败':
            exit
        print(title)
        i = 0
        for volume in chapters:
            i = i + 1
            print(i,':',volume)
        tot = i
        tr = True
        while tr:
            down = input("请输入需要下载的卷号(比如下载第1卷和第3到5卷输入1,3-5，若不输入则全下载):")
            try:
                downList = []
                if down == '':
                    for i in range(tot):
                        downList.append(i+1)
                else:
                    li = down.split(',')
                    for vol in li:
                        if '-' not in vol:
                            downList.append(int(vol))
                        else:
                            for i in range(int(vol.split('-')[0]),int(vol.split('-')[1])):
                                downList.append(i)
                downList = list(set(downList))
                tr = False
            except:
                print('卷号输入错误,请重新输入')
        print("计划下载卷: ",downList)
        i = 0
        content = title + '\n\n'
        for volume in chapters:
            i = i + 1
            if i in downList:
                print('正在下载: ',volume)
                content = content + volume + '\n\n' + download_chapter(chapters[volume])
        title = title.replace('\\', ' ').replace('\/', ' ').replace(':', ' ').replace('*', ' ').replace(
            '?', ' ').replace('\"', ' ').replace('<', ' ').replace('>', ' ').replace('|', ' ')
        with open(f'{title}{downList}.txt', 'w', encoding="utf-8") as f:
            f.write(content)
