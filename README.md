# 健身知识手册

一本讲清楚“为什么这样练”的中文健身手册：肌肉怎么长、一组该练多累、每个部位用哪些动作、一周怎么排、怎么吃才能一边减脂一边增肌。

在线阅读：<https://fitness.liangdeer.com>

## 内容

| 部分 | 章节 |
|---|---|
| 起点 | 1 先给自己的训练算笔账 |
| 原理 | 2 肌肉怎么长 · 3 训练变量 · 4 渐进超负荷、平台与减载 |
| 肌群与动作 | 5 胸 · 6 背 · 7 肩 · 8 手臂 · 9 下肢与核心 |
| 边界与编排 | 10 安全边界 · 11 计划编排 |
| 吃与恢复 | 12 营养与身体重组 · 13 恢复、有氧与测量 |
| 更多场景 | 14 杠铃自由重量 · 15 女性训练 · 16 居家与无器械训练 |
| 附录 | 术语表 · 十二个常见说法 · 来源清单 |

- 60 多张代码绘制的肌群图、动作图和图解，跟随系统的浅色和深色模式。
- 每个关键结论标注研究来源和证据等级（A 荟萃分析、B 随机对照试验、C 指南与共识、D 观察性或机制研究）。
- 全部来源都由独立审稿对照原文核对过，并附原文链接。

这不是医疗建议。有伤病或慢性病的人，先读第 10 章，再和医生商量。

## 目录结构

```
├── site/               部署用：index.html（单文件，可直接打开）和分享图、图标
├── assets/             网站图标 favicon.svg、分享预览图 og.png、apple-touch-icon.png
├── build.py            构建脚本：把正文、插图和来源拼成单个 HTML
├── src/                正文，每章一个 Markdown 文件
├── figs/               插图，用 Python 生成内联 SVG
├── sources.json        来源登记表：作者、年份、标题、期刊、证据等级、链接
├── style.css, app.js   版式和阅读交互
├── fonts/              数字用的 Barlow Condensed 字体（SIL OFL 许可）
└── wrangler.jsonc      Cloudflare 部署配置
```

## 自己构建

需要 Python 3 和 `markdown` 包：

```
pip install markdown
python3 build.py
```

生成 `site/index.html` 和 `out/figs.html`（所有插图的总览）。

## 正文写法

- 每章开头是元信息：`id`、`num`（章号）、`part`、`title`、`toc`、`lede`。
- 提示框：`::: key`（本章结论）、`::: ev`（证据怎么说）、`::: do`（可以直接用的做法）、`::: warn`（安全边界），以单独一行 `:::` 结束。
- 动作卡片：`::: ex 动作名 | 目标肌肉`。
- 插图：单独一行 `{{fig:图名|图注}}`。
- 引用：`[@key]` 或 `[@key1;@key2]`，对应 `sources.json`。每章末尾自动生成本章来源。

发现错误欢迎提 Issue，尤其是引用和数字方面的。

## 许可

- 文字、图解：[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans)（署名、非商业、相同方式共享），见 `LICENSE-CONTENT.md`。
- 代码（`build.py`、`figs/`、`app.js`、`style.css`）：MIT，见 `LICENSE`。
- 字体 Barlow Condensed：SIL Open Font License 1.1，见 `fonts/`。
- 引用的研究和指南版权归原作者和出版方所有，本书只做摘要和转述。
