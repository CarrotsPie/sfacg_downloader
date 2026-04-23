# catalog.py
from api import ApiClient
from typing import List, Dict

def get_novel_info(client: ApiClient, novel_id: str):
    """返回 (书名, 作者, 封面URL, volumes)"""
    return client.get_catalog(novel_id)

def select_volumes(volumes: List[Dict]) -> List[int]:
    """
    交互式让用户选择要下载的卷号（1-based）
    volumes: [{'name': 卷名, 'chapters': [...]}, ...]
    返回选中的索引列表（1-based）
    """
    total = len(volumes)
    print(f"共 {total} 卷：")
    for idx, vol in enumerate(volumes, 1):
        print(f"{idx}: {vol['name']}")

    while True:
        down = input("请输入需要下载的卷号(如 1,3-5，不输入则全下载): ").strip()
        try:
            if down == '':
                return list(range(1, total + 1))
            selected = set()
            for part in down.split(','):
                if '-' in part:
                    start, end = map(int, part.split('-'))
                    selected.update(range(start, end + 1))
                else:
                    selected.add(int(part))
            for v in selected:
                if v < 1 or v > total:
                    raise ValueError(f"卷号 {v} 超出范围")
            return sorted(selected)
        except Exception as e:
            print(f"输入错误: {e}，请重新输入")