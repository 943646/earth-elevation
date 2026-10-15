# 全球海拔与海深离线查询系统

三维地球上查询任意位置的海拔 / 海深，数据全部本地内置，不依赖网络。

- 在线访问：https://943646.github.io/earth-elevation/ （中文） · https://943646.github.io/earth-elevation/en.html （English）
- 单文件离线版：[`earth-offline.html`](earth-offline.html)（中文）、[`earth-offline-en.html`](earth-offline-en.html)（English），下载后双击即可使用，无需网络
- 位置链接：地址栏会记录当前视角与选点（如 `#view=27.9881,86.925,160&pin=27.9881,86.925`），中英文切换时保持位置，也可直接复制链接分享

## 文件结构

| 路径 | 说明 |
|---|---|
| `index.html` | 中文网页版（界面与程序），数据从下面的文件加载 |
| `en.html` | 英文网页版，由 `tools/build_en.py` 从 `index.html` 生成 |
| `lib/three.min.js`、`lib/OrbitControls.js` | three.js 三维引擎 |
| `data/land.jpg`、`data/sea.jpg` | 陆地海拔 / 海洋深度贴图（sqrt 编码，约 5 km 网格） |
| `data/mask.png` | 海陆掩膜 |
| `data/ext.webp` | 极值网格：每格（约 20 km）最高点 / 最深点，16 位无损 |
| `data/countries.json` | Natural Earth 10m 国界（TopoJSON） |
| `earth-offline.html` / `earth-offline-en.html` | 由构建脚本生成的中文 / 英文单文件离线版（所有文件内嵌） |
| `tools/build_en.py` | 生成英文网页版（翻译对照表 + 防漏译检查） |
| `tools/build_offline.py` | 生成中英文单文件离线版的脚本 |

## 修改后重新生成英文版与离线版

修改 `index.html`、`lib/` 或 `data/` 后依次运行（需要 Python 3）：

```
python3 tools/build_en.py        # 生成英文网页版 en.html
python3 tools/build_offline.py   # 生成中英文两个单文件离线版
```

如果改动了界面文字，`build_en.py` 会提示哪些原文在对照表里找不到或仍有中文未翻译，按提示补充 `tools/build_en.py` 中的对照表即可。

## 数据来源

- 地形 / 海深：AWS Terrain Tiles（SRTM · GMTED · ETOPO1 · GEBCO）
- 国界：Natural Earth 10m（经 world-atlas）
- 经典位置：各高峰、海沟等的官方测量值
