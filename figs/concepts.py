"""原理部分（第 2–4 章）的概念图。标了“示意”的图只表达趋势，形状不是实测数据。"""
import math
from .base import *


@fig('rir_scale', 360, 128)
def _():
    o = [T(0, 14, '一组做 12 次到力竭：停在第几次算 RIR 几', 't tb')]
    xs = [15 + i * 30 for i in range(12)]
    for i, x in enumerate(xs):
        n = i + 1
        cls = 'f-hi' if n == 12 else 'f-hi2' if n >= 9 else 'f-off'
        o.append(C(x, 52, 11.5, cls))
        st = ' style="fill:#fff"' if n == 12 else ''
        o.append(T(x, 57, str(n), 'tn', 'middle', st + ' font-size="13"'))
    for n, lab in ((9, 'RIR 3'), (10, 'RIR 2'), (11, 'RIR 1'), (12, 'RIR 0')):
        o.append(T(xs[n - 1], 84, lab, 'ts tb' if n < 12 else 'ts', 'middle', ' style="font-size:9.5px"'))
    o.append(P(f'M{xs[8]-11},94 v5 H{xs[10]+11} v-5', 's-hi', 1.5))
    o.append(T(xs[9], 116, '多数组停在这里', 'ts', 'middle'))
    o.append(T(xs[11], 116, '力竭', 'ts t2', 'middle'))
    o.append(TT(0, 88, ['前面几次还不吃力，', '作用是把后面几次变难'], 'ts t2', lh=15))
    return ''.join(o)


@fig('recruit', 360, 236)
def _():
    o = [T(0, 14, '同样做到力竭，大重量和小重量怎样动用肌纤维（示意）', 't tb')]
    for k, (x0, title, start) in enumerate(((10, '大重量 · 约 5 次力竭', .82), (198, '小重量 · 约 20 次力竭', .0))):
        w, h, y0 = 150, 118, 182
        o.append(T(x0, 40, title, 't'))
        base = .36
        pts_low = [(x0, y0), (x0, y0 - h * base), (x0 + w, y0 - h * base), (x0 + w, y0)]
        o.append(poly(pts_low, 'f-eq'))
        top = []
        n = 30
        for i in range(n + 1):
            t = i / n
            v = start + (1 - start) * (t ** (1.2 if k == 0 else 2.6))
            top.append((x0 + w * t, y0 - h * (base + (1 - base) * v)))
        o.append(poly([(x0, y0 - h * base)] + top + [(x0 + w, y0 - h * base)], 'f-hi'))
        o.append(L(x0, y0, x0 + w, y0, 's-line', 1.2))
        o.append(L(x0, y0, x0, y0 - h - 6, 's-line', 1.2))
        o.append(T(x0, y0 + 16, '第 1 次', 'ts t2'))
        o.append(T(x0 + w, y0 + 16, '力竭', 'ts t2', 'end'))
    o.append(R(10, 214, 11, 11, 'f-eq', 3)); o.append(T(26, 224, '容易动用的纤维', 'ts'))
    o.append(R(126, 214, 11, 11, 'f-hi', 3)); o.append(T(142, 224, '最难动用、增长潜力最大的纤维', 'ts'))
    return ''.join(o)


@fig('fail_tradeoff', 360, 232)
def _():
    x0, y0, w, h = 34, 176, 316, 124
    o = [T(0, 14, '离力竭越近，刺激涨得慢，疲劳涨得快（示意）', 't tb')]
    o.append(R(x0 + w * .4, y0 - h - 4, w * .4, h + 4, 'f-surf2', 6))
    o.append(T(x0 + w * .6, y0 - h + 12, '多数组放在这里', 'ts', 'middle'))
    o.append(axes(x0, y0, w, h, xt=[(i / 5, str(5 - i)) for i in range(6)]))
    o.append(curve(lambda t: .46 + .5 * t ** .8, x0, y0, w, h, 's-ink', 2.4))
    o.append(curve(lambda t: .08 + .86 * t ** 3.2, x0, y0, w, h, 's-hi', 2.4))
    o.append(T(x0 + 10, y0 - h * .62, '增肌刺激', 'ts tb'))
    o.append(T(x0 + w - 4, y0 - h * .33, '疲劳和', 'ts tb', 'end', ' style="fill:var(--fig-hi)"'))
    o.append(T(x0 + w - 4, y0 - h * .33 + 14, '恢复成本', 'ts tb', 'end', ' style="fill:var(--fig-hi)"'))
    o.append(T(x0, y0 + 36, '← 离力竭远', 'ts t2'))
    o.append(T(x0 + w / 2, y0 + 36, 'RIR（还能做几次）', 'ts t2', 'middle'))
    o.append(T(x0 + w, y0 + 36, '力竭 →', 'ts t2', 'end'))
    return ''.join(o)


@fig('vol_curve', 360, 262)
def _():
    x0, y0, w, h = 30, 196, 320, 150
    f = lambda x: (1 - math.exp(-x / 8.5)) * .948
    px = lambda x: x0 + w * x / 30
    py = lambda x: y0 - h * f(x)
    o = [T(0, 14, '每周组数与增肌效果：越往后，每多一组换来的越少', 't tb')]
    o.append(R(px(10), y0 - h - 6, px(20) - px(10), h + 6, 'f-surf2', 6))
    o.append(T(px(15), y0 - h + 8, '常见的高效区间', 'ts t2', 'middle'))
    o.append(axes(x0, y0, w, h, xt=[(v / 30, str(v)) for v in (0, 5, 10, 15, 20, 25, 30)]))
    o.append(curve(lambda t: f(30 * t), x0, y0, w, h, 's-ink', 2.4))
    pts = [(1, '股四头 1', 9, 4, 'start'), (3, '肩侧束 3', 10, 13, 'start'),
           (6.5, '三头* 6.5', -9, -5, 'end'), (14.5, '二头* 14.5', 6, 19, 'start')]
    for x, lab, dx, dy, a in pts:
        o.append(C(px(x), py(x), 5, 'f-hi'))
        o.append(T(px(x) + dx, py(x) + dy, lab, 'ts tb', a))
    c, b = 12, 11
    o.append(C(px(c), py(c), 5, 'f-hi')); o.append(C(px(b), py(b), 5, 'f-hi'))
    o.append(T(px(c) - 9, py(c) - 9, f'胸 {c} · 背 {b}', 'ts tb', 'end'))
    o.append(T(x0 + w, y0 + 34, '每周每个肌群的组数', 'ts t2', 'end'))
    o.append(T(x0 - 2, y0 - h - 12, '增肌效果', 'ts t2'))
    o.append(T(0, y0 + 56, '红点＝一个常见分布（示例）。* 折算值，复合动作每组计半组。', 'ts t2', 'start', ' style="font-size:10.4px"'))
    return ''.join(o)


@fig('freq_blocks', 360, 196)
def _():
    o = [T(0, 14, '同样每周 12 组胸：一次练完，还是分两次', 't tb')]
    x0, cw = 66, 42
    for i, d in enumerate('一二三四五六日'):
        o.append(T(x0 + i * cw + 18, 38, d, 'ts t2', 'middle'))

    def blocks(col, y, n, q):
        s = ''
        for j in range(n):
            cls = q(j)
            s += R(x0 + col * cw + (j % 3) * 13, y + (j // 3) * 13, 11, 11, cls, 2.5)
        return s
    o.append(T(0, 68, '一次练完', 't'))
    for i in range(7):
        o.append(R(x0 + i * cw - 3, 44, cw - 4, 58, 'f-surf2', 6))
    o.append(blocks(0, 47, 12, lambda j: 'f-hi' if j < 6 else 'f-hi2' if j < 9 else 'f-off'))
    o.append(T(0, 132, '分成两次', 't'))
    for i in range(7):
        o.append(R(x0 + i * cw - 3, 110, cw - 4, 34, 'f-surf2', 6))
    o.append(blocks(0, 114, 6, lambda j: 'f-hi'))
    o.append(blocks(3, 114, 6, lambda j: 'f-hi'))
    yb = 170
    for lx, c, lab in ((0, 'f-hi', '状态好的组'), (96, 'f-hi2', '打了折扣的组'), (204, 'f-off', '又累效果又差的组')):
        o.append(R(lx, yb - 9, 11, 11, c, 2.5)); o.append(T(lx + 16, yb + 1, lab, 'ts'))
    o.append(T(0, yb + 20, '示意：同一肌群一次练到第 7、8 组以后，次数和质量都会下降。', 'ts t2'))
    return ''.join(o)


@fig('rep_load', 360, 170)
def _():
    o = [T(0, 14, '每组做几次都能长肌肉，前提是做到接近力竭', 't tb')]
    x = lambda v: 10 + 340 * (v - 1) / 39
    o.append(R(x(1), 32, x(5) - x(1), 22, 'f-off', 5))
    o.append(R(x(5) + 2, 32, x(30) - x(5) - 4, 22, 'f-hi2', 5))
    o.append(R(x(6), 32, x(20) - x(6), 22, 'f-hi', 5))
    o.append(R(x(30), 32, x(40) - x(30), 22, 'f-off', 5))
    o.append(T((x(6) + x(20)) / 2, 47.5, '最常用', 'ts', 'middle', ' style="fill:#fff"'))
    for v in (1, 5, 10, 15, 20, 30, 40):
        o.append(T(x(v), 70, str(v), 'tn', 'middle', ' font-size="13"'))
    o.append(T(350, 86, '每组次数', 'ts t2', 'end'))
    rows = [('1–5 次', '更练力量；想靠它增肌要做更多组'), ('6–12 次', '最省时间，卧推、划船这类复合动作常用'),
            ('12–20 次', '关节压力小，侧平举、弯举和器械常用'), ('30 次以上', '也能长，但又累又耗时')]
    for i, (a, b) in enumerate(rows):
        o.append(T(0, 108 + i * 18, a, 'ts tb'))
        o.append(T(66, 108 + i * 18, b, 'ts'))
    return ''.join(o)


@fig('rest_bars', 360, 128)
def _():
    o = [T(0, 14, '组间休息多久', 't tb')]
    x0, w = 84, 168
    x = lambda m: x0 + w * m / 4
    for m in range(5):
        o.append(L(x(m), 30, x(m), 96, 'grid'))
        o.append(T(x(m), 112, f'{m} 分' if m else '0', 'ts t2', 'middle'))
    o.append(T(x0 - 10, 51, '多关节动作', 't', 'end'))
    o.append(R(x(2), 38, x(3) - x(2), 18, 'f-hi', 5))
    o.append(T(x(3) + 6, 51, '卧推、划船、腿举', 'ts t2'))
    o.append(T(x0 - 10, 83, '单关节动作', 't', 'end'))
    o.append(R(x(1), 70, x(2) - x(1), 18, 'f-hi2', 5))
    o.append(T(x(2) + 6, 83, '侧平举、弯举、下压', 'ts t2'))
    return ''.join(o)


@fig('stretch_pos', 360, 150)
def _():
    o = [T(0, 14, '同一个动作里，肌肉被拉长的那一段更值钱（示意）', 't tb')]
    o.append(R(0, 34, 118, 24, 'f-off', 6)); o.append(R(121, 34, 118, 24, 'f-hi2', 6)); o.append(R(242, 34, 118, 24, 'f-hi', 6))
    o.append(T(59, 50.5, '肌肉最短', 'ts', 'middle')); o.append(T(180, 50.5, '中段', 'ts', 'middle'))
    o.append(T(301, 50.5, '肌肉最长', 'ts', 'middle', ' style="fill:#fff"'))
    o.append(T(0, 76, '顶峰收缩', 'ts t2')); o.append(T(360, 76, '底部拉伸', 'ts t2', 'end'))
    rows = [('弯举', '每次都放到手臂接近伸直，不要只做上半程'), ('夹胸、推胸', '手向后打开到胸有拉伸感，再推回去'),
            ('腿弯举、提踵', '在最底部停半秒，再发力')]
    for i, (a, b) in enumerate(rows):
        o.append(T(0, 102 + i * 18, a, 'ts tb'))
        o.append(T(84, 102 + i * 18, b, 'ts'))
    return ''.join(o)


@fig('double_prog', 360, 252)
def _():
    x0, y0, w, h = 34, 186, 322, 136
    y = lambda v: y0 - h * (v - 6) / 7
    o = [T(0, 14, '双重进阶：以坐姿划船（40 kg 的组）为例', 't tb')]
    o.append(R(x0, y(12), w, y(8) - y(12), 'f-surf2', 6))
    o.append(T(x0 + 8, y(12) + 15, '目标区间 8–12 次', 'ts t2'))
    for v in (8, 10, 12):
        o.append(T(x0 - 7, y(v) + 4, str(v), 'tn', 'end', ' font-size="13"'))
    o.append(L(x0, y0, x0 + w, y0, 's-line', 1.2))
    cols = [('第 1 次', '40 kg', [9, 9, 8], 0), ('第 2 次', '40 kg', [10, 10], 0), ('第 3 次', '40 kg', [11, 11], 0),
            ('下一步', '40 kg', [12, 12], 1), ('再下一步', '45 kg', [8, 8], 2)]
    for i, (d, kg, reps, kind) in enumerate(cols):
        cx = x0 + 34 + i * 63
        for j, r in enumerate(reps):
            xx = cx + (j - (len(reps) - 1) / 2) * 15
            if kind == 0:
                o.append(C(xx, y(r), 6, 'f-ink'))
            else:
                o.append(C(xx, y(r), 5.2, 's-hi', ' stroke-width="2.2"'))
        o.append(T(cx, y0 + 17, d, 'ts', 'middle'))
        o.append(T(cx, y0 + 33, kg, 'tn', 'middle', ' font-size="13"' + (' style="fill:var(--fig-hi)"' if kind == 2 else '')))
    cx3, cx4 = x0 + 34 + 3 * 63, x0 + 34 + 4 * 63
    o.append(carrow(cx3 + 20, y(12) + 4, cx4 - 4, y(11), cx4 - 2, y(8) - 12, 's-hi', 1.6, 6, '3 3'))
    o.append(T(0, y0 + 56, '实心点＝已完成的组；空心圈＝按规则推出的下两步。', 'ts t2'))
    return ''.join(o)


def _node(x, y, w, h, lines, fill='var(--surface-2)', bold=False):
    o = [R(x, y, w, h, '', 10, f' style="fill:{fill}"')]
    n = len(lines)
    ty = y + h / 2 - (n - 1) * 8 + 4.5
    for i, s in enumerate(lines):
        o.append(T(x + w / 2, ty + i * 16, s, 'ts tb' if bold else 'ts', 'middle', ' style="font-size:11.5px"'))
    return ''.join(o)


@fig('prog_flow', 360, 338)
def _():
    o = [T(0, 14, '每个动作练完后，怎么决定下次做多少', 't tb')]
    D = [(30, ['所有组都到了次数上限，', '而且还留有目标余力？']),
         (116, ['比上次多做了 1 次，', '或同样次数更轻松？']),
         (202, ['已经连续 2–3 次', '没有任何进步？'])]
    O = [(30, ['下次加最小一档', '次数回到下限'], 'var(--do-soft)', '是'),
         (116, ['重量不变', '继续加次数'], 'var(--do-soft)', '是'),
         (202, ['正常波动', '照常练'], 'var(--surface-2)', '否')]
    for (y, lines), (_, ol, fill, lab) in zip(D, O):
        o.append(_node(0, y, 196, 50, lines, bold=True))
        o.append(arrow(198, y + 25, 228, y + 25, 's-ink', 1.6, 6))
        o.append(T(213, y + 18, lab, 'ts t2', 'middle'))
        o.append(_node(232, y, 128, 50, ol, fill))
    for y, lab in ((80, '否'), (166, '否'), (252, '是')):
        o.append(arrow(98, y + 2, 98, y + 32, 's-ink', 1.6, 6))
        o.append(T(108, y + 21, lab, 'ts t2'))
    o.append(_node(0, 288, 360, 46, ['先查睡眠、吃得够不够、力竭的组是不是太多；', '都没问题，再减量一周或换一个同类动作'], 'var(--warn-soft)'))
    return ''.join(o)


@fig('deload_week', 360, 184)
def _():
    o = [T(0, 14, '减量周长什么样（示意）', 't tb')]
    vals = [78, 84, 90, 96, 48, 84, 90, 96]
    x0, bw, gap, y0, h = 6, 34, 10, 148, 104
    for i, v in enumerate(vals):
        x = x0 + i * (bw + gap)
        cls = 'f-hi' if i == 4 else 'f-eq'
        o.append(R(x, y0 - h * v / 100, bw, h * v / 100, cls, 5))
        o.append(T(x + bw / 2, y0 + 16, f'第 {i + 1} 周', 'ts t2', 'middle', ' style="font-size:10px"'))
    o.append(T(x0 + 4 * (bw + gap) + bw / 2, y0 - h * .48 - 8, '组数减半', 'ts tb', 'middle', ' style="fill:var(--fig-hi)"'))
    o.append(T(0, y0 + 34, '柱高＝每周总组数。减量周重量基本不变，每组多留 1–2 次余力。', 'ts t2'))
    return ''.join(o)
