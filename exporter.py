# exporter.py
import re
import uuid
import requests
from ebooklib import epub
from typing import List, Dict
from config import CHAR_MAP, replace_chars

def format_line(line: str) -> str:
    """处理每行文本：删除前导空格，再添加两个全角空格作为首行缩进"""
    stripped = line.lstrip(' ')          # 删除前导半角空格
    if stripped.startswith('[img='):
        return stripped
    else:
        return '　　' + stripped            # 两个全角空格 + 原内容

def build_txt(volumes_data: List[Dict], title: str, selected_volumes_indices: List[int]) -> str:
    lines = [title, "\n\n"]
    for vol in volumes_data:
        lines.append(vol['name'])
        lines.append("\n\n")
        for chap in vol['chapters']:
            cleaned = replace_chars(chap['content'], CHAR_MAP)
            lines.append(f"{chap['title']}\n")
            # 处理内容每行
            for content_line in cleaned.splitlines():
                if content_line.strip():          # 非空行
                    lines.append(format_line(content_line))
                else:                             # 空行
                    lines.append("")
            lines.append("\n")
    return '\n'.join(lines)

def export_txt(content: str, title: str, suffix: str = ""):
    filename = re.sub(r'[\\/:*?"<>|]', ' ', title) + suffix + ".txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"TXT 已保存: {filename}")

def export_epub(volumes_data: List[Dict], title: str, author: str, cover_url: str, suffix: str = ""):
    book = epub.EpubBook()
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(title)
    book.set_language('zh')
    book.add_author(author)

    # 封面
    try:
        cover_img = requests.get(cover_url, timeout=15).content
        book.set_cover('cover.jpg', cover_img)
    except Exception as e:
        print(f"[警告] 封面下载失败: {e}，继续生成无封面的 EPUB")

    spine = ['nav']
    toc = []

    for vol in volumes_data:
        vol_name = vol['name']
        vol_html = epub.EpubHtml(title=vol_name, file_name=f"vol_{uuid.uuid4().hex}.xhtml", lang='zh')
        vol_html.content = f"<h2>{vol_name}</h2>"
        book.add_item(vol_html)
        spine.append(vol_html)

        vol_chapters = []
        for chap in vol['chapters']:
            cleaned_content = replace_chars(chap['content'], CHAR_MAP)
            chap_html = epub.EpubHtml(title=chap['title'], file_name=f"chap_{chap['id']}.xhtml", lang='zh')
            chap_content = f"<h2>{chap['title']}</h2>"

            for line in cleaned_content.splitlines():
                if '[img=' in line:
                    # 图片行：同样删除前导空格并添加缩进
                    stripped_line = line.lstrip(' ')
                    img_match = re.search(r'https?://.*?(?=\[\/img\]|$)', stripped_line)
                    if img_match:
                        img_url = img_match.group()
                        try:
                            img_data = requests.get(img_url, timeout=15).content
                            img_name = img_url.split('/')[-1]
                            img_item = epub.EpubImage(
                                uid=str(uuid.uuid4()),
                                file_name=f"img/{img_name}",
                                media_type='image/jpeg',
                                content=img_data
                            )
                            book.add_item(img_item)
                            chap_content += f'<p><img src="img/{img_name}"/></p>'
                        except Exception as e:
                            print(f"[警告] 图片 {img_url} 下载失败: {e}")
                            chap_content += f"<p>[图片加载失败]</p>"
                    else:
                        chap_content += f"<p>　　{stripped_line}</p>"
                else:
                    # 普通文本行
                    if line.strip():   # 非空行
                        stripped_line = line.lstrip(' ')
                        chap_content += f"<p>　　{stripped_line}</p>"
                    else:              # 空行
                        chap_content += "<p></p>"

            chap_html.content = chap_content
            book.add_item(chap_html)
            vol_chapters.append(chap_html)
            spine.append(chap_html)

        toc.append((vol_html, tuple(vol_chapters)))

    book.toc = tuple(toc)
    book.spine = spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    filename = re.sub(r'[\\/:*?"<>|]', ' ', title) + suffix + ".epub"
    epub.write_epub(filename, book, {})
    print(f"EPUB 已保存: {filename}")