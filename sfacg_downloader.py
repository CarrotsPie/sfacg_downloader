# main.py
from api import ApiClient
from auth import ensure_login
from catalog import get_novel_info, select_volumes
from exporter import build_txt, export_txt, export_epub
from config import DEFAULT_MAX_THREADS

def main():
    client = ApiClient()
    if not ensure_login(client):
        return

    novel_id = input("输入小说ID: ").strip()
    title, author, cover_url, volumes = get_novel_info(client, novel_id)
    if not title or not volumes:
        print("小说信息为空，可能 ID 错误")
        return

    selected_idx = select_volumes(volumes)
    print("计划下载卷:", [volumes[i-1]['name'] for i in selected_idx])

    volumes_data = []
    for idx in selected_idx:
        vol = volumes[idx-1]
        vol_name = vol['name']
        chapters_info = vol['chapters']   # 包含 id, title, need_fire
        print(f"\n=== 开始下载卷: {vol_name} ===")
        success_dict = client.download_chapters_concurrent(
            chapters_info, novel_id, max_workers=DEFAULT_MAX_THREADS
        )
        # 按原始顺序组装章节列表（付费章节已在success_dict中，失败章节用占位符）
        ordered_chapters = []
        for chap_info in chapters_info:
            chap_id = chap_info['id']
            if chap_id in success_dict:
                ordered_chapters.append(success_dict[chap_id])
            else:
                # 下载彻底失败（网络问题），添加占位内容
                ordered_chapters.append({
                    'id': chap_id,
                    'title': chap_info['title'],
                    'content': f"【章节下载失败，ID: {chap_id}】\n\n"
                })
                print(f"[警告] 章节 {chap_info['title']} 下载失败，已添加占位符")
        volumes_data.append({'name': vol_name, 'chapters': ordered_chapters})

    suffix = f"_{'_'.join(map(str, selected_idx))}" if len(selected_idx) != len(volumes) else ""
    txt_content = build_txt(volumes_data, title, selected_idx)
    export_txt(txt_content, title, suffix)
    export_epub(volumes_data, title, author, cover_url, suffix)

if __name__ == "__main__":
    main()
