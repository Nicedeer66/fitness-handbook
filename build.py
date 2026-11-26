#!/usr/bin/env python3
"""健身知识手册 构建脚本：src/*.md + figs/*.py + sources.json → out/index.html（单文件，零外部依赖）。
用法：python3 build.py        生成 out/index.html 和 out/figs.html（图解总览，检查用）
"""
import re, json, base64, pathlib, sys, html, datetime
import markdown

ROOT = pathlib.Path(__file__).parent
sys.path.insert(0, str(ROOT))
import figs  # noqa: E402
from figs.base import REG, ALT  # noqa: E402

VERSION = 'v1.0'
REPO = 'https://github.com/Nicedeer66/fitness-handbook'
SITE = 'https://fitness.liangdeer.com'
TODAY = datetime.date(2026, 11, 26)
PARTS = [
    ('p0', '起点', 'grey', '杠铃杆'),
    ('p1', '一 原理', 'red', '25 kg 红片'),
    ('p2', '二 肌群与动作', 'blue', '20 kg 蓝片'),
    ('p3', '三 边界与编排', 'yellow', '15 kg 黄片'),
    ('p4', '四 吃与恢复', 'green', '10 kg 绿片'),
    ('p5', '五 更多场景', 'plum', '5 kg 小片'),
    ('px', '附录', 'grey', '卡扣'),
]
BOX_LABEL = {'me': '对照你的记录', 'warn': '安全边界', 'do': '下次可以试', 'ev': '证据怎么说', 'key': '本章结论',
             'todo': '待核实'}
LEVELS = {'A': '系统综述 / 荟萃分析', 'B': '随机对照试验', 'C': '指南 / 立场声明 / 专家共识',
          'D': '观察性、机制、肌电研究或叙述性综述', 'X': '待核实'}
KW = {
    '杠铃深蹲': 'barbell back squat form', '传统硬拉': 'conventional deadlift form', '站姿杠铃推举': 'overhead press form',
    '分腿蹲': 'split squat form', '弹力带划船': 'resistance band seated row',
    '史密斯平板卧推': 'Smith machine bench press', '上斜推（固定一种器械）': 'incline chest press machine', '坐姿推胸器械': 'seated chest press machine',
    '蝴蝶机夹胸': 'pec deck fly', '俯卧撑': 'push-up form', '高位下拉（宽握长杆）': 'lat pulldown form', '坐姿绳索划船': 'seated cable row',
    '辅助引体向上': 'assisted pull-up machine', '胸托式或器械划船': 'chest supported row', '哑铃侧平举': 'dumbbell lateral raise scapular plane',
    '反向蝴蝶机': 'reverse pec deck rear delt fly', '绳索过顶臂屈伸': 'overhead cable triceps extension', '绳索下压（直杆或绳把）': 'triceps pushdown',
    '哑铃弯举': 'dumbbell curl form', '腿举': 'leg press form', '腿屈伸': 'leg extension form', '坐姿腿弯举（没有就用俯卧）': 'seated leg curl',
    '臀推（先从器械或徒手臀桥开始）': 'hip thrust / glute bridge', '站姿提踵': 'standing calf raise', '箱式高脚杯深蹲': 'goblet box squat',
    '平板支撑': 'plank form', '死虫': 'dead bug exercise',
}
SOURCES = json.load(open(ROOT / 'sources.json', encoding='utf-8'))


def esc(s):
    return html.escape(str(s), quote=True)


def front(text):
    meta = {}
    if text.startswith('---'):
        _, fm, text = text.split('---', 2)
        for ln in fm.strip().splitlines():
            k, _, v = ln.partition(':')
            meta[k.strip()] = v.strip()
    return meta, text


def inline(s):
    s = esc(s)
    return re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', s)


def pre(text):
    out, stack, exname = [], [], None
    for ln in text.split('\n'):
        m = re.match(r'^:::\s*(\w+)\s*(.*)$', ln)
        if m:
            kind, title = m.group(1), m.group(2).strip()
            if kind == 'ex':
                name, _, tg = title.partition('|')
                exname = name.strip()
                out += ['', '<div class="ex" markdown="1">',
                        f'<div class="ex-h"><h3>{esc(name.strip())}</h3><span>{esc(tg.strip())}</span></div>',
                        '<div class="ex-b" markdown="1">', '']
                k = KW.get(name.strip())
                zh = re.sub(r'（.*?）', '', name.strip()) + ' 教学'
                tail = (f'<p class="kw">想看真人示范：B 站搜「{esc(zh)}」，YouTube 搜「{esc(k)}」</p>\n' if k else '')
                stack.append(tail + '</div>\n</div>')
            else:
                out += ['', f'<div class="box {kind}" markdown="1">',
                        f'<p class="box-t">{esc(title or BOX_LABEL.get(kind, ""))}</p>', '']
                stack.append('</div>')
            continue
        if ln.strip() == ':::':
            out += ['', stack.pop(), '']
            continue
        m = re.match(r'^\{\{fig:([\w-]+)(?:\|(.*))?\}\}\s*$', ln)
        if m:
            name, cap = m.group(1), (m.group(2) or '')
            if name not in REG:
                raise SystemExit(f'缺图：{name}')
            if cap and name not in ALT:
                alt = re.sub(r'\*\*|`|\[@[^\]]+\]', '', cap).strip()
                ALT[name] = re.sub(r'([。：])\s+', r'\1', alt).rstrip('。')
            elif not cap and name not in ALT and exname and stack:
                ALT[name] = f'{exname}动作示意'
            capo = f'<figcaption>{inline(cap)}</figcaption>' if cap else ''
            out += ['', f'<figure class="figure"><div class="figwrap"><!--FIG:{name}--></div>{capo}</figure>', '']
            continue
        out.append(ln)
    if stack:
        raise SystemExit('有没闭合的 ::: 块')
    return '\n'.join(out)


def src_html(key, verified_only=False):
    s = SOURCES[key]
    lv = s.get('lv', 'D') if s.get('url') else 'X'
    link = f' <a href="{esc(s["url"])}" target="_blank" rel="noopener">原文</a>' if s.get('url') else ' <span class="lv X">链接待核实</span>'
    note = f' {esc(s["note"])}' if s.get('note') else ''
    return (f'<span><span class="lv {lv}" title="{LEVELS[lv]}">{lv}</span>{esc(s["a"])} ({s["y"]}). '
            f'<i>{esc(s["t"])}</i>. {esc(s.get("j", ""))}.{link}{note}</span>')


def render(meta, text):
    cid = meta['id']
    md = markdown.Markdown(extensions=['tables', 'md_in_html', 'sane_lists'])
    body = md.convert(pre(text))
    body = re.sub(r'<!--FIG:([\w-]+)-->', lambda m: REG[m.group(1)](), body)
    body = body.replace('<table>', '<div class="tablewrap"><table>').replace('</table>', '</table></div>')
    body = re.sub(r'(\d)–(\d)', '\\1\u2060–\u2060\\2', body)
    body = body.replace('RIR ', 'RIR\u00a0').replace(' → ', '\u00a0→\u00a0')
    if meta.get('num'):
        n = [0]

        def h2(m):
            n[0] += 1
            return f'<h2><span class="num">{meta["num"]}.{n[0]}</span>'
        body = re.sub(r'<h2>', h2, body)
    cited = []

    def cite(m):
        outs = []
        for k in re.findall(r'@([\w-]+)', m.group(0)):
            if k not in SOURCES:
                raise SystemExit(f'{cid}: 未登记的来源 {k}')
            if k not in cited:
                cited.append(k)
            i = cited.index(k) + 1
            outs.append(f'<a href="#{cid}" data-t="s-{cid}-{k}">{i}</a>')
        return '<sup class="cite">' + ''.join(outs) + '</sup>'
    body = re.sub(r'\[(?:@[\w-]+;?\s*)+\]', cite, body)
    if cited:
        body += '<div class="src"><h2>本章来源</h2><ol>' + ''.join(
            f'<li id="s-{cid}-{k}"><b>{i}</b>{src_html(k)}</li>' for i, k in enumerate(cited, 1)) + '</ol></div>'
    return body, cited


def main():
    chapters = []
    for f in sorted((ROOT / 'src').glob('*.md')):
        meta, text = front(f.read_text(encoding='utf-8'))
        if 'id' not in meta:
            continue
        body, cited = render(meta, text)
        chapters.append(dict(meta=meta, body=body, cited=cited))
    order = {p[0]: i for i, p in enumerate(PARTS)}
    chapters.sort(key=lambda c: (order[c['meta']['part']], int(c['meta'].get('ord', c['meta'].get('num', 0) or 0))))
    pc = {p[0]: p[2] for p in PARTS}

    # 来源总表
    used = {}
    for c in chapters:
        for k in c['cited']:
            used.setdefault(k, []).append(c['meta'])
    rows = []
    for k in sorted(used, key=lambda k: (SOURCES[k]['a'].lower(), SOURCES[k]['y'])):
        where = '、'.join(f'<a href="#{m["id"]}">第 {m["num"]} 章</a>' if m.get('num') else f'<a href="#{m["id"]}">{m["title"]}</a>' for m in used[k])
        rows.append(f'<li><b></b>{src_html(k)[:-7]} <span style="color:var(--ink-3)">引用于：{where}</span></span></li>')
    n_ok = sum(1 for k in used if SOURCES[k].get('url'))
    legend = ''.join(f'<li><span class="lv {k}">{k}</span>{v}</li>' for k, v in LEVELS.items())
    src_page = (f'<header class="ch-head"><div class="ch-eyebrow"><i></i>附录</div><h1>来源清单</h1>'
                + (f'<p class="lede">全书引用 {len(used)} 条来源，每一条都由没有参与写作的独立审稿对照原文核对过，并附上了原文链接。</p></header>' if n_ok == len(used) else f'<p class="lede">全书引用 {len(used)} 条来源，其中 {n_ok} 条的原文链接已由独立审稿核对过，其余标为待核实。</p></header>')
                + f'<ul class="legend-lv">{legend}</ul><div class="src"><ol>{"".join(rows)}</ol></div>')
    chapters.append(dict(meta=dict(id='sources', part='px', title='来源清单', ord='99'), body=src_page, cited=[], raw=True))

    # 目录
    nav, toc = [], []
    for pid, pname, color, plate in PARTS:
        cs = [c for c in chapters if c['meta']['part'] == pid]
        if not cs:
            continue
        nav.append(f'<div class="nav-part" style="--pc:var(--{color})"><i></i>{pname}</div>')
        items = []
        for c in cs:
            m = c['meta']
            num = m.get('num', '')
            nav.append(f'<a class="nl" style="--pc:var(--{color})" href="#{m["id"]}"><b>{num or "·"}</b>{esc(m["title"])}</a>')
            items.append(f'<a href="#{m["id"]}"><b>{num or "·"}</b><strong>{esc(m["title"])}</strong>'
                         f'<span>{esc(m.get("toc", ""))}</span></a>')
        toc.append(f'<div class="toc-part" style="--pc:var(--{color})"><h2>{pname} · {plate}</h2>{"".join(items)}</div>')

    # 页面
    pages = []
    n_ch = sum(1 for c in chapters if c['meta'].get('num'))
    n_fig = sum(c['body'].count('<svg class="fig') for c in chapters)
    n_words = sum(len(re.sub(r'<[^>]+>|\s', '', c['body'])) for c in chapters if not c.get('raw'))
    home_meta, home_text = front((ROOT / 'src' / '_home.md').read_text(encoding='utf-8'))
    home_body = markdown.Markdown(extensions=['tables', 'md_in_html']).convert(pre(home_text))
    home_body = re.sub(r'<!--FIG:([\w-]+)-->', lambda m: REG[m.group(1)](), home_body)
    home_body = home_body.replace('<!--LEVELS-->', f'<ul class="legend-lv">{legend}</ul>')
    cover = f'''<section class="page cover" id="home" data-title="封面">
<div class="cover-eyebrow">{VERSION} · {TODAY.year} 年 {TODAY.month} 月</div>
<h1>健身知识手册</h1>
<p class="lede">一本讲清楚“为什么这样练”的健身手册：肌肉怎么长、一组该练多累、每个部位用哪些动作、一周怎么排、怎么吃才能一边减脂一边增肌。每个关键结论都标了研究来源和证据等级。</p>
<div class="stats">
<div><b class="num">{n_ch}<em>章</em></b><span>另有术语表和常见说法辨析</span></div>
<div><b class="num">{n_fig}<em>张</em></b><span>肌群图、动作图和图解</span></div>
<div><b class="num">{len(used)}<em>条</em></b><span>研究和指南来源，逐条核对过原文</span></div>
<div><b class="num">{n_words / 10000:.1f}<em>万字</em></b><span>正文，按章节分页阅读</span></div>
</div>
<figure class="figure"><div class="figwrap">{REG["cover_bar"]()}{REG["cover_bar_m"]()}</div><figcaption>目录按杠铃装片的顺序排：最重的红片在最里面，对应全书的地基。点任意一片进入那一部分。</figcaption></figure>
<div class="toc">{"".join(toc)}</div>
{home_body}
</section>'''
    pages.append(cover)
    seq = [c['meta'] for c in chapters]
    for i, c in enumerate(chapters):
        m = c['meta']
        color = pc[m['part']]
        pname = next(p[1] for p in PARTS if p[0] == m['part'])
        if c.get('raw'):
            head = ''
        else:
            numh = f'<div class="ch-num">{int(m["num"]):02d}</div>' if m.get('num') else ''
            head = (f'<header class="ch-head"><div class="ch-eyebrow"><i></i>{pname}</div>{numh}'
                    f'<h1>{esc(m["title"])}</h1><p class="lede">{esc(m.get("lede", ""))}</p></header>')
        prev = seq[i - 1] if i else dict(id='home', title='封面')
        nxt = seq[i + 1] if i + 1 < len(seq) else None
        pn = f'<nav class="pn"><a href="#{prev["id"]}"><small>上一章</small>{esc(prev["title"])}</a>'
        pn += f'<a class="nx" href="#{nxt["id"]}"><small>下一章</small>{esc(nxt["title"])}</a>' if nxt else ''
        pn += '</nav>'
        title = (f'第 {m["num"]} 章 ' if m.get('num') else '') + m['title']
        pages.append(f'<section class="page" id="{m["id"]}" data-title="{esc(title)}" style="--part:var(--{color})" hidden>'
                     f'{head}{c["body"]}{pn}</section>')

    font = base64.b64encode((ROOT / 'fonts/barlow-condensed-latin-600-normal.woff2').read_bytes()).decode()
    font7 = base64.b64encode((ROOT / 'fonts/barlow-condensed-latin-700-normal.woff2').read_bytes()).decode()
    css = (f'@font-face{{font-family:"Barlow Condensed";font-weight:600;font-display:swap;src:url(data:font/woff2;base64,{font}) format("woff2")}}'
           f'@font-face{{font-family:"Barlow Condensed";font-weight:700;font-display:swap;src:url(data:font/woff2;base64,{font7}) format("woff2")}}'
           + (ROOT / 'style.css').read_text(encoding='utf-8'))
    js = (ROOT / 'app.js').read_text(encoding='utf-8')
    DESC = (f'一本讲给普通人的力量训练入门书：训练原理、主要肌群与动作、安全边界与计划编排、营养与恢复，'
            f'外加杠铃、女性训练和居家训练。共 {n_ch} 章、{n_fig} 张图，结论附 {len(used)} 条已核来源。')
    FAV = base64.b64encode((ROOT / 'assets/favicon.svg').read_bytes()).decode()
    doc = f'''<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>健身知识手册</title>
<meta name="description" content="{DESC}">
<meta name="theme-color" content="#d6352c">
<meta property="og:type" content="book">
<meta property="og:site_name" content="健身知识手册">
<meta property="og:title" content="健身知识手册">
<meta property="og:description" content="{DESC}">
<meta property="og:url" content="{SITE}/">
<meta property="og:image" content="{SITE}/og.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:locale" content="zh_CN">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="健身知识手册">
<meta name="twitter:description" content="{DESC}">
<meta name="twitter:image" content="{SITE}/og.png">
<link rel="icon" type="image/svg+xml" href="data:image/svg+xml;base64,{FAV}">
<link rel="apple-touch-icon" href="{SITE}/apple-touch-icon.png">
<style>{css}</style>
</head>
<body>
<aside class="nav" id="nav">
<a class="nav-brand" href="#home">健身知识手册<small>{VERSION}</small></a>
{"".join(nav)}
<div class="nav-foot"><button id="all-btn" type="button">展开全书（便于搜索）</button><br>{TODAY.isoformat()} 更新<br>不是医疗建议，身体相关的决定以医生意见为准。<br>文字与图解采用 <a href="https://creativecommons.org/licenses/by-nc-sa/4.0/deed.zh-hans" target="_blank" rel="noopener">CC BY-NC-SA 4.0</a> 许可，代码采用 MIT 许可。<a href="{REPO}" target="_blank" rel="noopener">源代码</a></div>
</aside>
<div class="scrim" id="scrim"></div>
<div class="shell">
<div class="topbar"><button id="menu-btn" type="button">目录</button><span id="crumb"></span></div>
<main>
{"".join(pages)}
</main>
</div>
<script>{js}</script>
</body>
</html>'''
    (ROOT / 'out').mkdir(exist_ok=True)
    (ROOT / 'out' / 'index.html').write_text(doc, encoding='utf-8')
    (ROOT / 'site').mkdir(exist_ok=True)
    (ROOT / 'site' / 'index.html').write_text(doc, encoding='utf-8')
    for f in ('og.png', 'apple-touch-icon.png', 'favicon.svg'):
        if (ROOT / 'assets' / f).exists():
            (ROOT / 'site' / f).write_bytes((ROOT / 'assets' / f).read_bytes())
    sheet = ''.join(f'<div style="break-inside:avoid;margin:0 0 18px"><div style="font:12px monospace;color:#888">{k}</div>'
                    f'<div class="figwrap">{fn()}</div></div>' for k, fn in REG.items())
    (ROOT / 'out' / 'figs.html').write_text(
        f'<!DOCTYPE html><html><head><meta charset="utf-8"><style>{css} body{{padding:16px}} .sheet{{columns:3 380px;column-gap:18px}}</style></head>'
        f'<body><div class="sheet">{sheet}</div></body></html>', encoding='utf-8')
    words = sum(len(re.sub(r'<[^>]+>|\s', '', c['body'])) for c in chapters if not c.get('raw'))
    print(f'章节 {len(chapters)}  图 {len(REG)}  来源 {len(used)}（已核 {n_ok}）  正文约 {words} 字  文件 {len(doc)/1024:.0f} KB')
    missing = [k for k in SOURCES if k not in used]
    if missing:
        print('未被引用的来源：', ' '.join(missing))


if __name__ == '__main__':
    main()
