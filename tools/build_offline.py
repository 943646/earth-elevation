#!/usr/bin/env python3
"""从网页版生成单文件离线版：index.html → earth-offline.html，en.html → earth-offline-en.html。

把 <script src="lib/..."> 内联，把 ASSETS 里的数据文件路径替换为 base64 内嵌数据，
并删除只适用于网页版的 <!--WEB-ONLY--> 段落。修改 index.html / lib / data 后重新运行：

    python3 tools/build_offline.py
"""
import base64, json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MIME = {'.jpg': 'image/jpeg', '.png': 'image/png', '.webp': 'image/webp'}


def read(path, mode='r'):
    with open(os.path.join(ROOT, path), mode, **({} if 'b' in mode else {'encoding': 'utf-8'})) as f:
        return f.read()


def build(src_name, out_name):
    html = read(src_name)

    # 1. 外部脚本内联（"</script" 转义，防止提前结束标签）
    def inline_script(m):
        code = read(m.group(1)).replace('</script', '<\\/script')
        return '<script>' + code + '</script>'
    html, n = re.subn(r'<script src="(lib/[^"]+)"></script>', inline_script, html)
    assert n == 2, f'expected 2 lib scripts, got {n}'

    # 2. 数据文件内嵌
    m = re.search(r'const ASSETS = \{(.*?)\};', html, re.S)
    assert m, 'ASSETS block not found'
    entries = []
    for key, path in re.findall(r"(\w+):\s*'([^']+)'", m.group(1)):
        if path.endswith('.json'):
            value = json.dumps(json.loads(read(path)), separators=(',', ':'), ensure_ascii=False)
        else:
            b64 = base64.b64encode(read(path, 'rb')).decode()
            value = "'data:%s;base64,%s'" % (MIME[os.path.splitext(path)[1]], b64)
        entries.append('  %s: %s' % (key, value))
    html = html[:m.start()] + 'const ASSETS = {\n' + ',\n'.join(entries) + '\n};' + html[m.end():]

    # 3. 删除网页版专用段落（如"下载离线版"按钮）
    html, n = re.subn(r'[ \t]*<!--WEB-ONLY-->.*?<!--/WEB-ONLY-->\r?\n', '', html, flags=re.S)
    for a, b in LOADING_TEXT:
        html = html.replace(a, b)

    out = os.path.join(ROOT, out_name)
    with open(out, 'w', encoding='utf-8', newline='') as f:
        f.write(html)
    print('wrote %s (%.1f MB)' % (out, os.path.getsize(out) / 1e6))


LOADING_TEXT = [('正在加载程序与离线数据（约 8 MB）', '正在装入内嵌离线数据'),
                ('Loading app and offline data (~8 MB)', 'Loading embedded offline data')]

for src_name, out_name in [('index.html', 'earth-offline.html'), ('en.html', 'earth-offline-en.html')]:
    if os.path.exists(os.path.join(ROOT, src_name)):
        build(src_name, out_name)
