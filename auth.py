# auth.py
import os
from api import ApiClient


COOKIE_FILE = "cookie.txt"

def load_cookie() -> str:
    if not os.path.exists(COOKIE_FILE):
        return ""
    with open(COOKIE_FILE, "r", encoding="utf-8") as f:
        return f.read().strip()

def save_cookie(cookie: str):
    with open(COOKIE_FILE, "w", encoding="utf-8") as f:
        f.write(cookie)

def ensure_login(client: ApiClient) -> bool:
    """
    确保已登录，若未登录则提示输入并保存 cookie
    返回 True 表示登录有效
    """
    cookie = load_cookie()
    if cookie:
        client.set_cookie(cookie)
        if client.check_login():
            print("已登录（使用保存的 cookie）")
            return True
        else:
            print("保存的 cookie 已失效")
    # 未登录或失效，进行登录
    username = input("输入手机号: ")
    password = input("输入密码: ")
    new_cookie = client.login(username, password)
    if new_cookie:
        client.set_cookie(new_cookie)
        save_cookie(new_cookie)
        print("登录成功，cookie 已保存")
        return True
    else:
        print("登录失败，请检查账号密码")
        return False