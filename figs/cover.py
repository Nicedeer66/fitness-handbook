"""公开版的封面图和第 1 章示例图。示例数据是虚构的，不对应任何个人。"""
from .base import *


def _cover(narrow):
    o = []
    cy = 62
    if narrow:
        shaft, plates, fs, x = 4, (52, 82, 76, 62, 50), 11.5, 0
    else:
        shaft, plates, fs, x = 84, (60, 100, 90, 78, 70), 13.5, 0
    o.append(R(0, cy - 5, shaft + 8, 10, 'f-eq', 5))
    o.append(R(shaft, cy - 14, 14, 28, 'f-eq', 3))
    tot = sum(plates) + 5 * len(plates)
    o.append(R(shaft + 14, cy - 8, tot + 26, 16, 'f-off', 4))
    x = shaft + 18
    spec = (('原理', '第 2–4 章', 'f-red', '#c2'), ('肌群与动作', '第 5–9 章', 'f-blue', '#c5'),
            ('边界与编排', '第 10–11 章', 'f-yellow', '#c10'), ('吃与恢复', '第 12–13 章', 'f-green', '#c12'), ('更多场景', '第 14–16 章', 'f-plum', '#c14'))
    for (lab, sub, cls, href), wd in zip(spec, plates):
        o.append(f'<a href="{href}">' + R(x, cy - 56, wd, 112, cls, 9) +
                 T(x + wd / 2, cy - 2, lab, 't tb', 'middle', f' style="fill:#fff;font-size:{fs}px"') +
                 T(x + wd / 2, cy + 17, sub.replace('第 ', '').replace(' 章', ' 章') if not narrow else sub.replace('第 ', ''), 'ts', 'middle', ' style="fill:#fff;opacity:.85;font-size:10px"') + '</a>')
        x += wd + 5
    o.append(R(x, cy - 17, 16, 34, 'f-eq', 4))
    if not narrow:
        o.append('<a href="#c1">' + T(0, cy - 18, '起点 · 第 1 章', 't') + '</a>')
    return ''.join(o)


@fig('cover_bar', 560, 124, 'w560 only-wide')
def _():
    """全书目录：五个部分画成杠铃上的五片杠铃片，点任意一片进入对应部分"""
    return _cover(False)


@fig('cover_bar_m', 372, 124, 'wfull only-narrow')
def _():
    """全书目录：五个部分画成杠铃上的五片杠铃片，点任意一片进入对应部分"""
    return _cover(True)


@fig('ex_weekly', 360, 330)
def _():
    """示例：每个肌群每周组数，对照每周 10 到 20 组的常用区间"""
    # 间接组按半组折算后的每周组数（示例数据）
    rows = [('背', 14), ('胸', 16), ('二头', 14.5), ('三头', 8), ('肩侧束', 3),
            ('肩后束', 7), ('股四头', 4), ('臀', 2), ('腘绳', 1)]
    lo, hi = 10, 20
    o = [T(0, 14, '示例：每周组数（间接组按半组算）', 't tb')]
    x0, w, vmax, y = 62, 248, 22, 46
    for v in (0, 5, 10, 15, 20):
        o.append(L(x0 + w * v / vmax, 34, x0 + w * v / vmax, 34 + len(rows) * 28, 'grid'))
        o.append(T(x0 + w * v / vmax, 30, str(v), 'ts t2', 'middle'))
    for lab, a in rows:
        o.append(T(x0 - 8, y + 4, lab, 't', 'end'))
        o.append(R(x0 + w * lo / vmax, y - 8, w * (hi - lo) / vmax, 16, 'f-off', 8))
        inside = lo <= a <= hi
        dx = x0 + w * a / vmax
        o.append(C(dx, y, 6.5, 'f-eq' if inside else 'f-hi'))
        if inside:
            o.append(T(x0 + w * hi / vmax + 8, y + 5, f'{a:g}', 'tn'))
        else:
            o.append(T(dx + 11, y + 5, f'{a:g}', 'tn'))
        y += 28
    yb = y + 8
    o.append(R(0, yb - 9, 22, 12, 'f-off', 6)); o.append(T(28, yb + 1, '10–20 组', 'ts'))
    o.append(C(104, yb - 3, 5.5, 'f-hi')); o.append(T(114, yb + 1, '低于区间', 'ts'))
    o.append(C(190, yb - 3, 5.5, 'f-eq')); o.append(T(200, yb + 1, '在区间内', 'ts'))
    return ''.join(o)



@fig('ex_compare', 360, 236)
def _():
    o = [T(0, 14, '这几次“进步”，哪些算数', 't tb')]
    rows = [('算', 'f-green', '同一台器械，40 kg × 10 → 40 kg × 11，RIR 都是 2'),
            ('算', 'f-green', '同一台器械，35 kg × 8 → 40 kg × 8，RIR 都是 2'),
            ('不算', 'f-red', '10 次 RIR 2 → 11 次 RIR 0：只是把余力花掉了'),
            ('不算', 'f-red', '史密斯卧推 → 自由杠铃卧推：器械不同，标重不可比'),
            ('不算', 'f-red', '第一个做 → 第四个做：顺序不同，疲劳程度不同'),
            ('不算', 'f-red', '每侧挂片 → 总重：口径不同')]
    y = 40
    for lab, c, txt in rows:
        o.append(R(0, y - 13, 38, 20, c, 10))
        o.append(T(19, y + 1, lab, 'ts tb', 'middle', ' style="fill:#fff"'))
        o.append(T(48, y + 1, txt, 'ts'))
        y += 32
    return ''.join(o)
