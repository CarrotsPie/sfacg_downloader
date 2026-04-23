# api.py
import time
import uuid
import requests
import json
import csv
import os
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Tuple, Optional
from config import DEVICE_TOKEN, SALT, BASE_HEADERS, DEFAULT_MAX_THREADS, CACHE_DIR, DEFAULT_MAX_RETRIES
from sign import get_sign

class ApiClient:
    def __init__(self):
        self.headers = BASE_HEADERS.copy()
        self.device_token = DEVICE_TOKEN
        self.salt = SALT
        self.nonce = self._init_nonce()

    def _init_nonce(self) -> str:
        """通过测试请求获取一个可用的 nonce"""
        test_url = "https://api.sfacg.com/Chaps/8436696?expand=content%2Cexpand.content"
        while True:
            nonce = str(uuid.uuid4()).upper()
            timestamp = int(time.time() * 1000)
            sign = get_sign(nonce, timestamp, self.device_token, self.salt)
            self.headers['sfsecurity'] = f'nonce={nonce}&timestamp={timestamp}&devicetoken={self.device_token}&sign={sign}'
            try:
                resp = requests.get(test_url, headers=self.headers, timeout=10)
                data = resp.json()
                if data.get('status', {}).get('httpCode') != 417:
                    print(f"[*] 初始化 nonce 成功: {nonce}")
                    return nonce
            except Exception:
                pass
            print(f"[!] nonce {nonce} 无效，重新生成...")
            time.sleep(0.5)

    def set_cookie(self, cookie: str):
        self.headers['cookie'] = cookie

    def _request(self, method: str, url: str, max_retries: int = DEFAULT_MAX_RETRIES, **kwargs) -> dict:
        """发送带签名的请求，自动重试417及网络异常"""
        retry = 0
        while retry < max_retries:
            try:
                timestamp = int(time.time() * 1000)
                sign = get_sign(self.nonce, timestamp, self.device_token, self.salt)
                self.headers['sfsecurity'] = f'nonce={self.nonce}&timestamp={timestamp}&devicetoken={self.device_token}&sign={sign}'

                req_headers = self.headers.copy()
                if 'headers' in kwargs:
                    req_headers.update(kwargs.pop('headers'))

                if method.upper() == 'GET':
                    resp = requests.get(url, headers=req_headers, timeout=10, **kwargs)
                elif method.upper() == 'POST':
                    resp = requests.post(url, headers=req_headers, timeout=10, **kwargs)
                else:
                    raise ValueError(f"Unsupported method: {method}")

                if resp.status_code != 200:
                    try:
                        data = resp.json()
                    except:
                        data = {'status': {'httpCode': resp.status_code}}
                else:
                    data = resp.json()

                http_code = data.get('status', {}).get('httpCode', 0)
                if http_code == 417:
                    retry += 1
                    print(f"[_request] 417 签名错误，重试 {retry}/{max_retries} - {url}")
                    time.sleep(0.5)
                    continue
                return data

            except (requests.exceptions.Timeout, requests.exceptions.ConnectionError) as e:
                retry += 1
                print(f"[_request] 网络异常: {e}，重试 {retry}/{max_retries} - {url}")
                time.sleep(1)
            except Exception as e:
                retry += 1
                print(f"[_request] 未知异常: {e}，重试 {retry}/{max_retries} - {url}")
                time.sleep(1)

        raise Exception(f"请求失败，已达到最大重试次数: {url}")

    def login(self, username: str, password: str) -> Optional[str]:
        """登录并返回 cookie 字符串"""
        url = "https://api.sfacg.com/sessions"
        payload = json.dumps({"password": password, "shuMeiId": "", "username": username})
        session = requests.Session()
        session.headers.update(self.headers)
        timestamp = int(time.time() * 1000)
        sign = get_sign(self.nonce, timestamp, self.device_token, self.salt)
        session.headers['sfsecurity'] = f'nonce={self.nonce}&timestamp={timestamp}&devicetoken={self.device_token}&sign={sign}'
        try:
            resp = session.post(url, data=payload, timeout=10)
            if resp.status_code == 200 and resp.json().get('status', {}).get('httpCode') == 200:
                cookie_dict = requests.utils.dict_from_cookiejar(session.cookies)
                return f'.SFCommunity={cookie_dict[".SFCommunity"]}; session_APP={cookie_dict["session_APP"]}'
        except Exception:
            pass
        return None

    def check_login(self) -> bool:
        """检查当前 cookie 是否有效"""
        url = "https://api.sfacg.com/user"
        try:
            resp = self._request('GET', url)
            return resp.get('status', {}).get('httpCode') == 200
        except:
            return False

    def get_catalog(self, novel_id: str) -> Tuple[str, str, str, List[Dict]]:
        """
        获取小说目录
        返回: (书名, 作者, 封面URL, volumes列表)
        volumes每个元素: {'name': 卷名, 'chapters': [{'id':, 'title':, 'need_fire':}, ...]}
        """
        info_resp = self._request('GET', f'https://api.sfacg.com/novels/{novel_id}?expand=bigNovelCover')
        title = info_resp['data']['novelName']
        author = info_resp['data']['authorName']
        cover = info_resp['data']['expand']['bigNovelCover']

        dir_resp = self._request('GET', f'https://api.sfacg.com/novels/{novel_id}/dirs?expand=originNeedFireMoney')
        volumes = []
        for volume in dir_resp['data']['volumeList']:
            vol_name = volume['title']
            chapters = []
            for chap in volume['chapterList']:
                chapters.append({
                    'id': chap['chapId'],
                    'title': chap['title'],               # 章节标题
                    'need_fire': chap.get('needFireMoney', 0)
                })
            volumes.append({'name': vol_name, 'chapters': chapters})
        return title, author, cover, volumes

    def download_chapter(self, chap_id: int) -> Tuple[bool, Optional[str], Optional[str]]:
        """下载单个章节，返回(成功, 标题, 内容)"""
        url = f"https://api.sfacg.com/Chaps/{chap_id}?expand=content%2Cexpand.content"
        try:
            resp = self._request('GET', url, max_retries=8)
            if resp.get('status', {}).get('httpCode') == 200:
                title = resp['data']['title']
                tmp = ""
                if 'content' in resp['data']:
                    tmp += resp['data']['content']
                    if 'expand' in resp['data'] and 'content' in resp['data']['expand']:
                        tmp += resp['data']['expand']['content']
                else:
                    tmp += resp['data']['expand']['content']
                return True, title, tmp
            elif resp.get('status', {}).get('httpCode') == 403:
                print(f"[{chap_id}] 403 未订阅/需付费，跳过")
                return False, None, None
            else:
                print(f"[{chap_id}] 未知状态码: {resp.get('status', {}).get('httpCode')}")
                return False, None, None
        except Exception as e:
            print(f"[{chap_id}] 下载失败: {e}")
            return False, None, None

    # ---------- 缓存相关 ----------
    def _get_cache_path(self, novel_id: str) -> str:
        """获取缓存文件路径，自动创建 cache 目录"""
        if not os.path.exists(CACHE_DIR):
            os.makedirs(CACHE_DIR)
        return os.path.join(CACHE_DIR, f"{novel_id}.csv")

    def _load_cache(self, novel_id: str) -> Dict[int, Tuple[str, str]]:
        """
        加载缓存，返回 {chap_id: (title, content)}
        """
        cache_path = self._get_cache_path(novel_id)
        cache = {}
        if os.path.exists(cache_path):
            try:
                with open(cache_path, 'r', encoding='utf-8', newline='') as f:
                    reader = csv.reader(f)
                    next(reader, None)  # 跳过表头
                    for row in reader:
                        if len(row) >= 3:
                            chap_id = int(row[0])
                            title = row[1]
                            content = row[2]
                            cache[chap_id] = (title, content)
                print(f"[缓存] 从 {cache_path} 加载了 {len(cache)} 个章节")
            except Exception as e:
                print(f"[缓存] 加载失败: {e}")
        return cache

    def _save_cache(self, novel_id: str, cache: Dict[int, Tuple[str, str]]):
        """保存缓存字典到 CSV 文件"""
        cache_path = self._get_cache_path(novel_id)
        try:
            with open(cache_path, 'w', encoding='utf-8', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(['chap_id', 'title', 'content'])
                for chap_id, (title, content) in cache.items():
                    writer.writerow([chap_id, title, content])
            print(f"[缓存] 保存了 {len(cache)} 个章节到 {cache_path}")
        except Exception as e:
            print(f"[缓存] 保存失败: {e}")

    # ---------- 并发下载（含缓存） ----------
    def download_chapters_concurrent(self, chapters_info: List[Dict], novel_id: str,
                                     max_workers: int = DEFAULT_MAX_THREADS) -> Tuple[Dict[int, Dict], List[int]]:
        """
        并发下载章节，使用缓存避免重复请求
        chapters_info: [{'id':, 'title':, 'need_fire':}, ...]
        novel_id: 小说ID，用于缓存文件名
        返回 (成功字典, 失败列表)
              成功字典格式: {chap_id: {'id':, 'title':, 'content':}, ...}
        """
        # 加载缓存
        cache = self._load_cache(novel_id)
        success_dict = {}

        # 处理付费章节
        paid_chaps = [chap for chap in chapters_info if chap.get('need_fire', 0) > 1]
        for chap in paid_chaps:
            success_dict[chap['id']] = {
                'id': chap['id'],
                'title': chap['title'],
                'content': "【未订阅/需付费】\n\n"
            }
            print(f"【{chap['title']}】 未订阅，跳过下载")

        # 处理免费章节
        free_chaps = [chap for chap in chapters_info if chap.get('need_fire', 0) == 0]
        # 从缓存中取
        for chap in free_chaps[:]:  # 遍历副本，便于修改
            chap_id = chap['id']
            if chap_id in cache:
                title, content = cache[chap_id]
                success_dict[chap_id] = {'id': chap_id, 'title': title, 'content': content}
                print(f"[缓存] {title} 从缓存加载")
                free_chaps.remove(chap)

        # 并发下载缓存中不存在的免费章节
        if free_chaps:
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                future_to_chap = {
                    executor.submit(self.download_chapter, chap['id']): chap
                    for chap in free_chaps
                }
                for future in as_completed(future_to_chap):
                    chap = future_to_chap[future]
                    chap_id = chap['id']
                    chap_title = chap['title']
                    success, title, content = future.result()
                    if success:
                        final_title = title if title else chap_title
                        final_content = content
                        success_dict[chap_id] = {'id': chap_id, 'title': final_title, 'content': final_content}
                        # 更新缓存
                        cache[chap_id] = (final_title, final_content)
                        print(f"{final_title} 已下载并缓存")
                    else:
                        print(f"[{chap_title}] 下载失败，未缓存")

            # 保存更新后的缓存
            self._save_cache(novel_id, cache)

        return success_dict