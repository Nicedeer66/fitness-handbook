"""第 10–13 章的图：安全边界、计划、营养、测量。"""
import math, random
from .base import *
from .body import bodymap

BW = 70  # 示例：70 kg、175 cm、30 岁男性
BMR = 10 * BW + 6.25 * 175 - 5 * 30 + 5  # Mifflin-St Jeor，男性
IN_LO, IN_HI = 2050, 2250


@fig('pain_scale', 360, 150)
def _():
    o = [T(0, 14, '训练中关节或腰背不适，用 0–10 分来决定怎么办', 't tb')]
    x = lambda v: 6 + 348 * v / 10
    for a, b, cls, lab in ((0, 3, 'f-green', '继续'), (3, 5, 'f-yellow', '减量'), (5, 10, 'f-red', '停掉这个动作')):
        o.append(R(x(a) + 1, 30, x(b) - x(a) - 2, 22, cls, 5))
        o.append(T((x(a) + x(b)) / 2, 45.5, lab, 'ts', 'middle', ' style="fill:#fff"'))
    for v in range(11):
        o.append(T(x(v), 70, str(v), 'tn', 'middle', ' font-size="13"'))
    o.append(T(0, 94, '0–3 分可以继续；4–5 分减重量或缩小幅度；6 分以上停掉这个动作。', 'ts'))
    o.append(T(0, 112, '同时看第二天早上：晨僵或疼痛比平时明显加重，下次同一动作减量。', 'ts'))
    o.append(T(0, 130, '锐痛、放射痛、麻木、关节肿胀不适用这把尺子，直接停止并就医。', 'ts'))
    return ''.join(o)


@fig('week_strip', 360, 150)
def _():
    o = [T(0, 14, '四次力量训练在一周里的位置（示例）', 't tb')]
    days = [('一', '上肢 A', 'f-red'), ('二', '下肢 A', 'f-blue'), ('三', '游泳或步行', 'f-surf2'), ('四', '上肢 B', 'f-red'),
            ('五', '下肢 B', 'f-blue'), ('六', '游泳或步行', 'f-surf2'), ('日', '休息', 'f-surf2')]
    cw = 360 / 7
    for i, (d, lab, cls) in enumerate(days):
        x = i * cw
        o.append(T(x + cw / 2 - 2, 38, d, 'ts t2', 'middle'))
        st = ' stroke="var(--fig-line)" stroke-width="1"' if cls == 'f-surf2' else ''
        o.append(R(x + 2, 46, cw - 6, 58, cls, 8, st))
        parts = [lab[:2], lab[2:].strip()] if cls != 'f-surf2' else ([lab[:3], lab[3:]] if len(lab) > 3 else [lab])
        col = ' style="fill:#fff"' if cls != 'f-surf2' else ''
        for k, s in enumerate(parts):
            o.append(T(x + cw / 2 - 1, 72 + k * 15 - (0 if len(parts) > 1 else -7), s, 'ts tb' if cls != 'f-surf2' else 'ts', 'middle', col))
    o.append(T(0, 126, '同类训练之间至少隔 48 小时。也可以不绑定星期几，', 'ts t2'))
    o.append(T(0, 142, '按 上A → 下A → 上B → 下B 的顺序隔天轮换。', 'ts t2'))
    return ''.join(o)


@fig('session_flow', 360, 164)
def _():
    o = [T(0, 14, '一次训练 60–75 分钟怎么分配', 't tb')]
    segs = [('热身', 8, 'f-off'), ('多关节动作', 30, 'f-hi'), ('单关节动作', 20, 'f-hi2'), ('核心', 7, 'f-eq'), ('放松', 5, 'f-off')]
    tot = sum(s[1] for s in segs)
    x = 0
    rows = []
    for i, (lab, m, cls) in enumerate(segs):
        w = 360 * m / tot
        o.append(R(x + 1, 30, w - 2, 24, cls, 5))
        o.append(T(x + w / 2, 70, f'{m}′', 'tn', 'middle', ' font-size="13"'))
        x += w
    notes = [('热身', '快走或单车 5 分钟，第一个动作先做 1–2 组轻的'), ('多关节', '推、拉、腿举。状态最好时做最重要的'),
             ('单关节', '侧平举、臂屈伸、弯举、腿弯举'), ('核心', '平板支撑、死虫，各 2 组'), ('放松', '轻柔拉伸胸、背阔肌、髋前侧')]
    for i, (a, b) in enumerate(notes):
        o.append(T(0, 92 + i * 15, a, 'ts tb', 'start', ' style="font-size:10.5px"'))
        o.append(T(46, 92 + i * 15, b, 'ts', 'start', ' style="font-size:10.5px"'))
    return ''.join(o)


@fig('energy_balance', 360, 176)
def _():
    lo, hi = BMR * 1.5, BMR * 1.6
    o = [T(0, 14, '每天的热量：估算的消耗和起步的摄入（示例）', 't tb')]
    x0, w, vmax = 8, 236, 3000
    px = lambda v: x0 + w * v / vmax
    for v in (0, 1000, 2000, 3000):
        o.append(L(px(v), 28, px(v), 118, 'grid'))
        o.append(T(px(v), 132, str(v), 'ts t2', 'middle'))
    o.append(T(360, 132, '千卡/天', 'ts t2', 'end'))
    o.append(R(px(0), 36, px(BMR) - px(0), 20, 'f-off', 4))
    o.append(R(px(BMR) + 2, 36, px(lo) - px(BMR) - 2, 20, 'f-eq', 4))
    o.append(R(px(lo), 36, px(hi) - px(lo), 20, 'f-hi2', 4))
    o.append(T((px(0) + px(BMR)) / 2, 50, f'基础代谢 ≈ {round(BMR, -1):.0f}', 'ts', 'middle', ' style="font-size:10px"'))
    o.append(T(px(hi) + 6, 50, f'总消耗 ≈ {round(lo, -1):.0f}–{round(hi, -1):.0f}', 'ts tb', 'start', ' style="font-size:10px"'))
    o.append(R(px(0), 80, px(IN_LO) - px(0), 20, 'f-off', 4))
    o.append(R(px(IN_LO), 80, px(IN_HI) - px(IN_LO), 20, 'f-hi', 4))
    o.append(T((px(0) + px(IN_LO)) / 2, 94, '起步摄入', 'ts', 'middle'))
    o.append(T(px(IN_HI) + 6, 94, f'{IN_LO}–{IN_HI}', 'ts tb'))
    o.append(T(0, 154, '摄入按总消耗的中间值少 300–500 千卡；活动系数取 1.5–1.6。', 'ts t2', 'start', ' style="font-size:10.2px"'))
    o.append(T(0, 170, '这只是起点，要用两周的体重和腰围来校准。', 'ts t2', 'start', ' style="font-size:10.2px"'))
    return ''.join(o)


@fig('protein_bar', 360, 136)
def _():
    o = [T(0, 14, f'每天吃多少蛋白质（按体重 {BW} kg 计）', 't tb')]
    x = lambda g: 8 + 344 * (g - 60) / 140
    o.append(R(x(60), 36, x(200) - x(60), 18, 'f-surf2', 5))
    o.append(R(x(1.6 * BW), 36, x(2.2 * BW) - x(1.6 * BW), 18, 'f-hi2', 5))
    for g in (80, 120, 160):
        o.append(T(x(g), 70, f'{g} g', 'ts t2', 'middle'))
    for k in (1.2, 1.6, 2.2):
        g = k * BW
        o.append(L(x(g), 30, x(g), 60, 's-ink', 1))
        o.append(T(x(g), 26, f'{k} g/kg', 'ts', 'middle', ' style="font-size:9.5px"'))
    yb = 94
    o.append(R(0, yb - 9, 12, 12, 'f-hi2', 3)); o.append(T(18, yb + 1, f'研究支持的范围 {1.6 * BW:.0f}–{2.2 * BW:.0f} g', 'ts'))
    o.append(T(0, yb + 19, '热量缺口期间，靠近范围的上半段更稳妥。', 'ts'))
    return ''.join(o)


def _wedge(cx, cy, r, a0, a1, cls):
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    large = 1 if (a1 - a0) > 180 else 0
    return (f'<path d="M{cx},{cy} L{p0[0]:.1f},{p0[1]:.1f} A{r},{r} 0 {large} 1 {p1[0]:.1f},{p1[1]:.1f} Z" class="{cls}" '
            f'stroke="var(--surface)" stroke-width="3"/>')


@fig('plate', 360, 190)
def _():
    o = [T(0, 14, '食堂一餐怎么打', 't tb')]
    cx, cy, r = 96, 104, 72
    o.append(C(cx, cy, r + 6, 'f-surf2'))
    o.append(_wedge(cx, cy, r, -90, 90, 'f-green'))
    o.append(_wedge(cx, cy, r, 90, 180, 'f-hi'))
    o.append(_wedge(cx, cy, r, 180, 270, 'f-yellow'))
    o.append(T(cx + 34, cy + 4, '蔬菜', 't tb', 'middle', ' style="fill:#fff"'))
    o.append(T(cx - 30, cy + 34, '蛋白质', 't tb', 'middle', ' style="fill:#fff"'))
    o.append(T(cx - 30, cy - 22, '主食', 't tb', 'middle', ' style="fill:#fff"'))
    rows = [('蛋白质', '一掌到一掌半：鸡、鱼、牛肉、', '蛋、豆腐。先定这一格'), ('主食', '一拳到一拳半：米饭、面、', '杂粮。训练日多一点'),
            ('蔬菜', '两拳以上。少要汤汁', '')]
    y = 52
    for a, b, c in rows:
        o.append(T(196, y, a, 'ts tb'))
        o.append(T(196, y + 16, b, 'ts'))
        if c:
            o.append(T(196, y + 31, c, 'ts'))
        y += 50 if c else 34
    return ''.join(o)


@fig('weight_trend', 360, 204)
def _():
    random.seed(7)
    days = 35
    base = [76.6 - 0.045 * d for d in range(days)]
    daily = [b + random.uniform(-0.55, 0.55) + (0.5 if d % 7 == 6 else 0) for d, b in enumerate(base)]
    avg = [sum(daily[max(0, i - 6):i + 1]) / len(daily[max(0, i - 6):i + 1]) for i in range(days)]
    x0, y0, w, h = 34, 160, 320, 124
    lo, hi = 74.5, 77.8
    px = lambda d: x0 + w * d / (days - 1)
    py = lambda v: y0 - h * (v - lo) / (hi - lo)
    o = [T(0, 14, '每天的体重上下跳，七天平均线才是趋势（示意数据）', 't tb')]
    for v in (75, 76, 77):
        o.append(L(x0, py(v), x0 + w, py(v), 'grid'))
        o.append(T(x0 - 6, py(v) + 4, str(v), 'ts t2', 'end'))
    for wk in range(6):
        o.append(T(px(min(wk * 7, days - 1)), y0 + 16, f'第 {wk + 1} 周' if wk < 5 else '', 'ts t2', 'start', ' style="font-size:10px"'))
    o.append(L(x0, y0, x0 + w, y0, 's-line', 1.2))
    o.append('<path d="M' + ' L'.join(f'{px(d):.1f},{py(v):.1f}' for d, v in enumerate(daily)) + '" class="s-line" stroke-width="1.2"/>')
    for d, v in enumerate(daily):
        o.append(C(px(d), py(v), 2.2, 'f-eq'))
    o.append('<path d="M' + ' L'.join(f'{px(d):.1f},{py(v):.1f}' for d, v in enumerate(avg) if d >= 6) + '" class="s-hi" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>')
    yb = 192
    o.append(C(6, yb - 3, 3, 'f-eq')); o.append(T(16, yb + 1, '每天晨重', 'ts'))
    o.append(L(86, yb - 3, 106, yb - 3, 's-hi', 2.6)); o.append(T(112, yb + 1, '七天平均：五周下降约 1.5 kg，每周约 0.3 kg', 'ts'))
    return ''.join(o)


@fig('measure_sites', 360, 420)
def _():
    body, h = bodymap('front', [], '', (0, 400), 1.0)
    o = [T(0, 14, '皮尺量哪里', 't tb'), f'<g transform="translate(0,14)">{body}</g>']
    top = 14 + 4
    sites = [(88, '胸围', '乳头高度，呼气末', 'R'), (116, '上臂围', '上臂中点，放松下垂', 'L'), (146, '腰围', '最下肋骨和髂骨上缘的中点', 'R'),
             (192, '臀围', '臀部最宽处', 'L'), (236, '大腿围', '大腿中点，站立放松', 'R')]
    for y, name, how, side in sites:
        gy = top + y
        if name == '上臂围':
            o.append(L(180 - 62, gy, 180 - 38, gy, 's-hi', 2, '4 3'))
        elif name == '大腿围':
            o.append(L(180 + 6, gy, 180 + 36, gy, 's-hi', 2, '4 3'))
        else:
            half = {'胸围': 36, '腰围': 28, '臀围': 34}[name]
            o.append(L(180 - half, gy, 180 + half, gy, 's-hi', 2, '4 3'))
        if side == 'R':
            o.append(T(262, gy - 2, name, 'ts tb'))
            for k, part in enumerate([how[i:i + 9] for i in range(0, len(how), 9)]):
                o.append(T(262, gy + 12 + k * 13, part, 'ts t2', 'start', ' style="font-size:10px"'))
        else:
            o.append(T(98, gy - 2, name, 'ts tb', 'end'))
            for k, part in enumerate([how[i:i + 9] for i in range(0, len(how), 9)]):
                o.append(T(98, gy + 12 + k * 13, part, 'ts t2', 'end', ' style="font-size:10px"'))
    return ''.join(o)
