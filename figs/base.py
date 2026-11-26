"""图解基础件：所有图都输出内联 SVG，颜色只用 CSS 类，跟随页面明暗主题。"""
import html, re, math

REG = {}


ALT = {}  # 图名 → 无障碍描述，由 build.py 从图注填入


def fig(name, w, h, cls=None):
    def deco(fn):
        def make():
            c = cls or ('w360' if w <= 400 else 'w480' if w <= 540 else 'w720')
            doc = (fn.__doc__ or '').strip().splitlines()
            body = fn()
            label = ALT.get(name) or (doc[0].rstrip('。') if doc else '示意图')
            texts = [html.unescape(t) for t in re.findall(r'<text[^>]*>([^<]+)</text>', body)]
            if texts and name in ALT and label.endswith('动作示意'):
                label += '：' + '；'.join(texts[:4])
            return (f'<svg class="fig {c}" viewBox="0 0 {w} {h}" role="img" '
                    f'aria-label="{esc(label)}">{body}</svg>')
        REG[name] = make
        return fn
    return deco


def esc(s):
    return html.escape(str(s), quote=True)


def tw(s, fs=12.5):
    """估算文字宽度：中日韩字符按 1em，其余按 0.56em。"""
    n = 0.0
    for ch in str(s):
        n += 1.0 if ord(ch) > 0x2E80 else (0.3 if ch in ' .,:;|il!' else 0.56)
    return n * fs


def T(x, y, s, cls='t', a='start', extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{a}"{extra}>{esc(s)}</text>'


def TT(x, y, lines, cls='t', a='start', lh=17):
    return ''.join(T(x, y + i * lh, s, cls, a) for i, s in enumerate(lines))


def R(x, y, w, h, cls, r=0, extra=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" rx="{r}" class="{cls}"{extra}/>'


def C(cx, cy, r, cls, extra=''):
    return f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" class="{cls}"{extra}/>'


def L(x1, y1, x2, y2, cls='s-line', sw=1.5, dash=None, cap='round'):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}" '
            f'stroke-width="{sw}" stroke-linecap="{cap}"{d}/>')


def P(d, cls, sw=None, extra=''):
    s = f' stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"' if sw else ''
    return f'<path d="{d}" class="{cls}"{s}{extra}/>'


def poly(pts, cls, extra=''):
    return f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x, y in pts)}" class="{cls}"{extra}/>'


_FILL = {'s-ink': 'f-ink', 's-hi': 'f-hi', 's-red': 'f-red', 's-blue': 'f-blue', 's-green': 'f-green',
         's-yellow': 'f-yellow', 's-grey': 'f-grey', 's-eq': 'f-eq', 's-line': 'f-grey'}


def arrow(x1, y1, x2, y2, cls='s-ink', sw=1.8, head=7, dash=None):
    """直线箭头，箭头尖在 (x2,y2)。"""
    ang = math.atan2(y2 - y1, x2 - x1)
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    px, py = -math.sin(ang) * head * 0.5, math.cos(ang) * head * 0.5
    return (L(x1, y1, bx, by, cls, sw, dash) +
            poly([(x2, y2), (bx + px, by + py), (bx - px, by - py)], _FILL.get(cls, 'f-ink')))


def carrow(x1, y1, cx, cy, x2, y2, cls='s-ink', sw=1.8, head=7, dash=None):
    """二次贝塞尔曲线箭头。"""
    ang = math.atan2(y2 - cy, x2 - cx)
    bx, by = x2 - head * math.cos(ang), y2 - head * math.sin(ang)
    px, py = -math.sin(ang) * head * 0.5, math.cos(ang) * head * 0.5
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return (f'<path d="M{x1:.1f},{y1:.1f} Q{cx:.1f},{cy:.1f} {bx:.1f},{by:.1f}" class="{cls}" '
            f'stroke-width="{sw}" stroke-linecap="round"{d}/>' +
            poly([(x2, y2), (bx + px, by + py), (bx - px, by - py)], _FILL.get(cls, 'f-ink')))


def chip(x, y, s, cls='f-surf2', tcls='ts', pad=7, h=20, a='start'):
    """小标签：圆角底 + 文字。x 为左端（a=start）或中心（a=middle）。"""
    w = tw(s, 11) + pad * 2
    x0 = x - w / 2 if a == 'middle' else x
    return R(x0, y - h / 2, w, h, cls, h / 2) + T(x0 + w / 2, y + 4, s, tcls, 'middle')


def hbars(items, x=0, y=0, w=360, label_w=70, bh=16, gap=11, vmax=None, unit='', val_w=44):
    """横向条形图。items: [(label, value, fill_cls, note)]；返回 (svg, 高度)。"""
    vmax = vmax or max(v for _, v, *_ in items)
    bw = w - label_w - val_w
    out = []
    yy = y
    for it in items:
        label, v = it[0], it[1]
        cls = it[2] if len(it) > 2 and it[2] else 'f-off'
        note = it[3] if len(it) > 3 else ''
        out.append(T(x + label_w - 8, yy + bh - 3.5, label, 't', 'end'))
        out.append(R(x + label_w, yy, bw, bh, 'f-surf2', 4))
        out.append(R(x + label_w, yy, max(bw * v / vmax, 2), bh, cls, 4))
        out.append(T(x + label_w + bw * v / vmax + 6, yy + bh - 2.5, f'{v:g}{unit}', 'tn'))
        if note:
            out.append(T(x + w, yy + bh - 3.5, note, 'ts t2', 'end'))
        yy += bh + gap
    return ''.join(out), yy - y - gap


def axes(x0, y0, w, h, xl='', yl='', xt=None, yt=None):
    """简单坐标轴：左下角 (x0,y0)，向右 w、向上 h。xt/yt: [(frac, label)]"""
    o = [L(x0, y0, x0 + w, y0, 's-line', 1.2), L(x0, y0, x0, y0 - h, 's-line', 1.2)]
    for f, lab in (xt or []):
        o.append(L(x0 + w * f, y0, x0 + w * f, y0 + 4, 's-line', 1.2))
        o.append(T(x0 + w * f, y0 + 17, lab, 'ts t2', 'middle'))
    for f, lab in (yt or []):
        o.append(L(x0 - 4, y0 - h * f, x0 + w, y0 - h * f, 'grid'))
        o.append(T(x0 - 7, y0 - h * f + 4, lab, 'ts t2', 'end'))
    if xl:
        o.append(T(x0 + w, y0 + 33, xl, 'ts t2', 'end'))
    if yl:
        o.append(T(x0 - 2, y0 - h - 9, yl, 'ts t2'))
    return ''.join(o)


def curve(fn, x0, y0, w, h, cls='s-ink', sw=2.2, n=60, t0=0.0, t1=1.0, dash=None):
    """fn: t∈[0,1] → v∈[0,1]，画在以 (x0,y0) 为左下角的坐标区内。"""
    pts = []
    for i in range(n + 1):
        t = t0 + (t1 - t0) * i / n
        pts.append((x0 + w * t, y0 - h * fn(t)))
    d = 'M' + ' L'.join(f'{x:.1f},{y:.1f}' for x, y in pts)
    da = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<path d="{d}" class="{cls}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"{da}/>'


def box(x, y, w, h, lines, cls='f-surf2', tcls='t', r=10, stroke=None, lh=16):
    """流程图节点：圆角框 + 居中多行字。"""
    st = f' stroke="var(--{stroke})" stroke-width="1.5"' if stroke else ''
    o = [R(x, y, w, h, cls, r, st)]
    n = len(lines)
    ty = y + h / 2 - (n - 1) * lh / 2 + 4.5
    for i, s in enumerate(lines):
        o.append(T(x + w / 2, ty + i * lh, s, tcls if i == 0 else tcls.replace(' tb', ''), 'middle'))
    return ''.join(o)
