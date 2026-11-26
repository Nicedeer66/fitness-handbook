"""动作示意图：用胶囊形小人画起始和结束两个姿势。
侧面小人一律面朝右。角度约定：0° 指向右，90° 指向下，-90° 指向上。"""
import math
from .base import *


def _v(a, l):
    r = math.radians(a)
    return (l * math.cos(r), l * math.sin(r))


def _add(p, v):
    return (p[0] + v[0], p[1] + v[1])


def J(hip, torso=-90, uarm=90, farm=90, thigh=90, shin=90, foot=0, head=None, el=None, hand=None,
      knee=None, ankle=None, S=1.0):
    sh = _add(hip, _v(torso, 40 * S))
    hd = _add(sh, _v(torso if head is None else head, 17 * S))
    el = el or _add(sh, _v(uarm, 23 * S))
    hand = hand or _add(el, _v(farm, 21 * S))
    kn = knee or _add(hip, _v(thigh, 34 * S))
    an = ankle or _add(kn, _v(shin, 32 * S))
    toe = _add(an, _v(foot, 12 * S))
    return dict(hip=hip, sh=sh, head=hd, el=el, hand=hand, knee=kn, ankle=an, toe=toe, S=S)


def _seg(a, b, w, cls):
    return L(a[0], a[1], b[0], b[1], cls, w)


def _ov(a, b, t0, t1, off, w, cls):
    dx, dy = b[0] - a[0], b[1] - a[1]
    n = math.hypot(dx, dy) or 1
    px, py = -dy / n, dx / n
    return L(a[0] + dx * t0 + px * off, a[1] + dy * t0 + py * off,
             a[0] + dx * t1 + px * off, a[1] + dy * t1 + py * off, cls, w)


def man(j, hi=(), hi2=(), far=None, bend=0):
    """画一个侧面小人。hi 主要发力部位，hi2 协同部位；far 是远侧肢体的关节；bend>0 表示弓背。"""
    S = j['S']
    o = []
    hip, sh, el, hand, kn, an, toe = j['hip'], j['sh'], j['el'], j['hand'], j['knee'], j['ankle'], j['toe']
    if far:
        o += [_seg(hip, far['knee'], 10 * S, 's-body'), _seg(far['knee'], far['ankle'], 8 * S, 's-body'),
              _seg(far['ankle'], far['toe'], 6 * S, 's-body'),
              _seg(sh, far['el'], 7 * S, 's-body'), _seg(far['el'], far['hand'], 6 * S, 's-body')]
    if bend:
        dx, dy = sh[0] - hip[0], sh[1] - hip[1]
        n = math.hypot(dx, dy)
        mx, my = (hip[0] + sh[0]) / 2 + dy / n * bend, (hip[1] + sh[1]) / 2 - dx / n * bend
        o.append(P(f'M{hip[0]:.1f},{hip[1]:.1f} Q{mx:.1f},{my:.1f} {sh[0]:.1f},{sh[1]:.1f}', 's-eq', 14 * S))
    else:
        o.append(_seg(hip, sh, 14 * S, 's-eq'))
    o.append(C(j['head'][0], j['head'][1], 8 * S, 'f-eq'))

    def lay(name, a, b, t0, t1, off, w):
        if name in hi:
            o.append(_ov(a, b, t0, t1, off * S, w * S, 's-hi'))
        elif name in hi2:
            o.append(_ov(a, b, t0, t1, off * S, w * S, 's-hi2'))
    if not bend:
        lay('chest', hip, sh, .58, .93, 4, 5)
        lay('abs', hip, sh, .1, .5, 4, 5)
        lay('lats', hip, sh, .38, .85, -4, 5)
        lay('erector', hip, sh, .05, .42, -4, 5)
    o += [_seg(hip, kn, 11 * S, 's-eq'), _seg(kn, an, 9 * S, 's-eq'), _seg(an, toe, 6 * S, 's-eq')]
    lay('quads', hip, kn, .12, .9, -3, 5)
    lay('hams', hip, kn, .12, .9, 3, 5)
    lay('calves', kn, an, .06, .62, 2.5, 4)
    for name in ('glutes',):
        if name in hi or name in hi2:
            o.append(C(hip[0], hip[1], 6.5 * S, 'f-hi' if name in hi else 'f-hi2'))
    o += [_seg(sh, el, 10.5 * S, 's-bg'), _seg(el, hand, 9.5 * S, 's-bg')]
    o += [_seg(sh, el, 8 * S, 's-eq'), _seg(el, hand, 7 * S, 's-eq')]
    lay('biceps', sh, el, .18, .9, -2.2, 3.6)
    lay('triceps', sh, el, .12, .9, 2.2, 3.6)
    if 'delt' in hi or 'delt' in hi2:
        o.append(C(sh[0], sh[1], 5.5 * S, 'f-hi' if 'delt' in hi else 'f-hi2'))
    return ''.join(o)


# ---- 器械小件 ----
def floor(y, x1=4, x2=172):
    return L(x1, y, x2, y, 's-line', 1.5)


def pad(p1, p2, w=8):
    return L(p1[0], p1[1], p2[0], p2[1], 's-far', w)


def frame(p1, p2, w=1.6):
    return L(p1[0], p1[1], p2[0], p2[1], 's-ink', w)


def barbell(p, r=13):
    return (C(p[0], p[1], r, 'f-surf2', ' stroke="var(--fig-ink)" stroke-width="1.4"') + C(p[0], p[1], 3.2, 'f-ink'))


def dumbbell(p, a=0, l=14):
    return f'<rect x="{p[0]-l/2:.1f}" y="{p[1]-3.5:.1f}" width="{l}" height="7" rx="2.5" class="f-ink" transform="rotate({a} {p[0]:.1f} {p[1]:.1f})"/>'


def cable(hand, pulley):
    return (L(hand[0], hand[1], pulley[0], pulley[1], 's-ink', 1.1) +
            C(pulley[0], pulley[1], 4, 'f-surf2', ' stroke="var(--fig-ink)" stroke-width="1.3"'))


def roller(p, r=5):
    return C(p[0], p[1], r, 'f-off', ' stroke="var(--fig-ink)" stroke-width="1.2"')


def note(x, y, s, a='start'):
    return T(x, y, s, 'ts', a, ' style="font-size:10px"')


def mv(p1, p2, bow=12):
    """红色虚线弧箭头，表示手或器械的运动方向。"""
    mx, my = (p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2
    dx, dy = p2[0] - p1[0], p2[1] - p1[1]
    n = math.hypot(dx, dy) or 1
    return carrow(p1[0], p1[1], mx - dy / n * bow, my + dx / n * bow, p2[0], p2[1], 's-hi', 1.5, 6, '3 3')


def two(a, b, h, la='起始', lb='结束'):
    return ('<g transform="translate(5,0)">' + T(0, 11, la, 'ts t2') + T(186, 11, lb, 'ts t2') +
            f'<g>{a}</g><g transform="translate(186,0)">{b}</g>' + L(181, 4, 181, h - 4, 'grid') + '</g>')


# ---- 正面 / 俯视小人 ----
def front(cx, sy, arms=(8, 8), hi=(), legs='stand', S=1.0):
    o = []
    pts = [(cx - 17 * S, sy - 2 * S), (cx + 17 * S, sy - 2 * S), (cx + 12 * S, sy + 34 * S), (cx + 13 * S, sy + 43 * S),
           (cx - 13 * S, sy + 43 * S), (cx - 12 * S, sy + 34 * S)]
    hy = sy + 43 * S
    if legs == 'stand':
        for s in (1, -1):
            o.append(L(cx + s * 7 * S, hy, cx + s * 9 * S, hy + 34 * S, 's-eq', 11 * S))
            o.append(L(cx + s * 9 * S, hy + 34 * S, cx + s * 9 * S, hy + 64 * S, 's-eq', 9 * S))
    else:
        for s in (1, -1):
            o.append(L(cx + s * 8 * S, hy, cx + s * 10 * S, hy + 10 * S, 's-eq', 12 * S))
            o.append(L(cx + s * 10 * S, hy + 10 * S, cx + s * 10 * S, hy + 38 * S, 's-eq', 9 * S))
    o.append(poly(pts, 'f-eq', ' stroke="var(--fig-eq)" stroke-width="6" stroke-linejoin="round"'))
    o.append(C(cx, sy - 19 * S, 8.5 * S, 'f-eq'))
    if 'lats' in hi:
        for s in (1, -1):
            o.append(poly([(cx + s * 18 * S, sy + 7 * S), (cx + s * 13 * S, sy + 33 * S), (cx + s * 5 * S, sy + 30 * S),
                           (cx + s * 8 * S, sy + 9 * S)], 'f-hi'))
    out = dict(hands=[], els=[], sh=[])
    for s in (1, -1):
        sh = (cx + s * 17 * S, sy)
        au, af = arms
        el = (sh[0] + s * 23 * S * math.sin(math.radians(au)), sh[1] + 23 * S * math.cos(math.radians(au)))
        hand = (el[0] + s * 21 * S * math.sin(math.radians(af)), el[1] + 21 * S * math.cos(math.radians(af)))
        o += [_seg(sh, el, 8 * S, 's-eq'), _seg(el, hand, 7 * S, 's-eq')]
        if 'delts' in hi:
            o.append(C(sh[0], sh[1], 6 * S, 'f-hi'))
        out['hands'].append(hand); out['els'].append(el); out['sh'].append(sh)
    return ''.join(o), out


def top(cx, cy, arms=(0, 0), hi=()):
    """俯视小人，面朝画面上方。手臂角度：0 向外侧平伸，-90 向正前方，90 向正后方。"""
    o = [f'<ellipse cx="{cx}" cy="{cy + 5}" rx="25" ry="10" class="f-eq"/>']
    if 'chest' in hi:
        o.append(P(f'M{cx - 19},{cy - 1} Q{cx},{cy - 9} {cx + 19},{cy - 1}', 's-hi', 5))
    if 'upback' in hi:
        o.append(P(f'M{cx - 17},{cy + 12} Q{cx},{cy + 17} {cx + 17},{cy + 12}', 's-hi2', 5))
    hands = []
    for s in (1, -1):
        sh = (cx + s * 22, cy + 5)
        au, af = arms
        el = (sh[0] + s * 23 * math.cos(math.radians(au)), sh[1] + 23 * math.sin(math.radians(au)))
        hand = (el[0] + s * 21 * math.cos(math.radians(af)), el[1] + 21 * math.sin(math.radians(af)))
        o += [_seg(sh, el, 8, 's-eq'), _seg(el, hand, 7, 's-eq')]
        if 'rdelt' in hi:
            o.append(C(sh[0] + s * 1, sh[1] + 4, 5, 'f-hi'))
        hands.append(hand)
    o.append(C(cx, cy, 9, 'f-eq', ' stroke="var(--surface)" stroke-width="1.5"'))
    o.append(poly([(cx - 3, cy - 8), (cx + 3, cy - 8), (cx, cy - 13)], 'f-eq'))
    return ''.join(o), hands


# =============== 胸 ===============
def _bench(flat=True):
    H = 150
    fl = 139

    def panel(bottom):
        o = [floor(fl)]
        if flat:
            hip = (112, 86)
            o += [pad((40, 97), (124, 97)), frame((52, 102), (52, fl)), frame((114, 102), (114, fl))]
            kw = dict(torso=180, thigh=30, shin=85, foot=0)
            j = J(hip, el=(92.7, 96), hand=(92.7, 75), **kw) if bottom else J(hip, uarm=-90, farm=-90, **kw)
        else:
            hip = (112, 100)
            d = _v(210, 1)
            back = (-0.5, 0.866)
            p1 = (hip[0] + back[0] * 9 - d[0] * 2, hip[1] + back[1] * 9 - d[1] * 2)
            p2 = (hip[0] + back[0] * 9 + d[0] * 60, hip[1] + back[1] * 9 + d[1] * 60)
            o += [pad(p1, p2), pad((114, 111), (142, 111)), frame((70, 96), (70, fl)), frame((128, 115), (128, fl))]
            kw = dict(torso=210, thigh=12, shin=82, foot=0)
            j = J(hip, el=(88, 93), hand=(88, 72), **kw) if bottom else J(hip, uarm=-90, farm=-90, **kw)
        o.append(barbell(j['hand']))
        o.append(man(j, hi=('chest',), hi2=('triceps', 'delt')))
        if bottom:
            top_hand = J(hip, uarm=-90, farm=-90, **kw)['hand']
            o.append(mv((top_hand[0] + 16, top_hand[1] + 4), (j['hand'][0] + 16, j['hand'][1] - 2), -6))
        return ''.join(o)
    return two(panel(False), panel(True), H, '顶端', '底部'), H


for _n, _flat in (('ex_bench', True), ('ex_incline', False)):
    _b, _h = _bench(_flat)
    fig(_n, 370, _h)(lambda b=_b: b)


@fig('ex_chestpress', 370, 150)
def _():
    fl = 139

    def panel(end):
        hip = (62, 102)
        o = [floor(fl), pad((54, 111), (92, 111)), pad((50, 104), (41, 52)), frame((72, 115), (72, fl)), frame((46, 60), (46, fl))]
        kw = dict(torso=-100, thigh=5, shin=85)
        j = J(hip, el=(79, 66), hand=(100, 68), **kw) if end else J(hip, el=(50, 82), hand=(71, 72), **kw)
        o.append(frame((66, 26), j['hand'], 2.2))
        o.append(C(66, 26, 3.5, 'f-ink'))
        o.append(man(j, hi=('chest',), hi2=('triceps', 'delt')))
        o.append(L(j['hand'][0], j['hand'][1] - 6, j['hand'][0], j['hand'][1] + 6, 's-ink', 3))
        if end:
            o.append(mv((74, 86), (102, 82), 6))
        return ''.join(o)
    return two(panel(False), panel(True), 150)


@fig('ex_pecdeck', 370, 132)
def _():
    def panel(end):
        o = [pad((66, 92), (110, 92), 7)]
        s, hands = top(88, 72, (-78, -138) if end else (8, -18), hi=('chest',))
        o.append(s)
        for hx, hy in hands:
            o.append(C(hx, hy, 4, 'f-ink'))
        if end:
            o.append(mv((142, 60), (106, 30), -10))
            o.append(mv((34, 60), (70, 30), 10))
        return ''.join(o)
    return two(panel(False), panel(True), 132, '起始（俯视）', '结束（俯视）') + note(5, 126, '手向后打开到胸有拉伸感即可，不必过度后展。')


@fig('ex_pushup', 370, 150)
def _():
    fl = 139

    def panel(bottom):
        o = [floor(fl)]
        if bottom:
            sh = (51, 123)
            hip = (sh[0] + 39.8, sh[1] + 3.8)
            j = J(hip, torso=185.4, thigh=5.4, shin=5.4, foot=90, el=(65, 114), hand=(58, 135), head=175)
        else:
            sh = (58, 91)
            hip = (sh[0] + 37.1, sh[1] + 15)
            j = J(hip, torso=202, thigh=22, shin=22, foot=90, uarm=90, farm=90, head=190)
        o.append(man(j, hi=('chest',), hi2=('triceps', 'abs')))
        return ''.join(o)
    return two(panel(False), panel(True), 150, '顶端', '底部：身体保持一条直线')


# =============== 背 ===============
@fig('ex_latpd', 370, 170)
def _():
    def panel(end):
        cx, sy = 88, 62
        o = [pad((cx - 26, sy + 60), (cx + 26, sy + 60), 6)]
        s, d = front(cx, sy, (45, 175) if end else (150, 170), hi=('lats',), legs='seat')
        by = d['hands'][0][1] - 2
        o.append(L(cx, 6, cx, by, 's-ink', 1.1))
        o.append(s)
        o.append(L(cx - 50, by, cx + 50, by, 's-ink', 3))
        o.append(pad((cx - 22, sy + 48), (cx + 22, sy + 48), 6))
        if end:
            o.append(mv((cx + 44, 22), (cx + 44, by - 4), -8))
            o.append(note(174, sy + 30, '肘往下、往后', 'end'))
        return ''.join(o)
    return two(panel(False), panel(True), 170, '起始（背面看）', '结束')


@fig('ex_row', 370, 150)
def _():
    fl = 139

    def panel(end):
        hip = (62, 100)
        o = [floor(fl), pad((46, 109), (100, 109)), frame((56, 113), (56, fl)), frame((92, 113), (92, fl)),
             frame((120, 132), (130, 104), 3), frame((125, 118), (150, 118)), frame((150, 70), (150, fl))]
        kw = dict(thigh=2, shin=50, foot=-72)
        j = J(hip, torso=-92, uarm=125, farm=5, **kw) if end else J(hip, torso=-80, uarm=25, farm=14, **kw)
        o.append(cable(j['hand'], (150, 84)))
        o.append(man(j, hi=('lats',), hi2=('biceps',)))
        if end:
            o.append(mv((104, 66), (80, 70), -5))

        return ''.join(o)
    return two(panel(False), panel(True), 150, '起始：让肩胛向前伸开', '结束：挺胸，肩胛向后收')


# =============== 肩 ===============
@fig('ex_latraise', 370, 172)
def _():
    def panel(end):
        cx, sy = 88, 44
        o = [floor(160, 20, 156)]
        s, d = front(cx, sy, (80, 84) if end else (7, 5), hi=('delts',))
        o.append(s)
        for hx, hy in d['hands']:
            o.append(dumbbell((hx, hy + (3 if not end else 0)), 0 if not end else 90, 13))
        if end:
            o.append(L(cx - 74, sy, cx + 74, sy, 's-hi', 1, '3 3'))
            o.append(note(cx + 76, sy + 22, '手不高过肩', 'end'))
        return ''.join(o)
    return two(panel(False), panel(True), 172)


@fig('ex_reversefly', 370, 132)
def _():
    def panel(end):
        o = [pad((66, 56), (110, 56), 7)]
        s, hands = top(88, 72, (18, 8) if end else (-78, -92), hi=('rdelt', 'upback'))
        o.append(s)
        for hx, hy in hands:
            o.append(C(hx, hy, 4, 'f-ink'))
        if end:
            o.append(mv((104, 30), (140, 62), -10))
            o.append(mv((72, 30), (36, 62), 10))
        return ''.join(o)
    return two(panel(False), panel(True), 132, '起始（俯视）', '结束（俯视）') + note(5, 126, '胸口贴住靠垫。手臂打开到与肩成一线，不用再往后甩。')


# =============== 手臂 ===============
def _stand(hipx=84, lean=-90, **kw):
    return J((hipx, 88), torso=lean, thigh=88, shin=92, foot=0, **kw)


@fig('ex_curl', 370, 170)
def _():
    fl = 158

    def panel(end):
        j = _stand(uarm=92, farm=-62 if end else 86)
        o = [floor(fl), man(j, hi=('biceps',)), dumbbell(j['hand'], 0)]
        if end:
            s = _stand(uarm=92, farm=86)['hand']
            o.append(mv((s[0] + 12, s[1] - 2), (j['hand'][0] + 12, j['hand'][1] + 6), -10))

        return ''.join(o)
    return two(panel(False), panel(True), 170, '起始：放到接近伸直', '结束：上臂不前移')


@fig('ex_pushdown', 370, 170)
def _():
    fl = 158

    def panel(end):
        j = _stand(80, -80, uarm=96, farm=84 if end else -38)
        o = [floor(fl), frame((150, 24), (150, fl)), cable(j['hand'], (150, 28)), man(j, hi=('triceps',))]
        o.append(L(j['hand'][0] - 5, j['hand'][1], j['hand'][0] + 5, j['hand'][1], 's-ink', 3))
        if end:
            o.append(mv((112, 66), (100, 98), -8))
        return ''.join(o)
    return two(panel(False), panel(True), 170, '起始', '结束：肘固定在体侧')


@fig('ex_overhead', 370, 188)
def _():
    fl = 176

    def panel(end):
        hip = (84, 108)
        far = J(hip, torso=-72, thigh=112, shin=106, foot=0, uarm=-74, farm=-58 if end else 150)
        j = J(hip, torso=-72, thigh=70, shin=100, foot=0, uarm=-74, farm=-58 if end else 150)
        o = [floor(fl), frame((16, 32), (16, fl)), cable(j['hand'], (16, 74)), man(j, hi=('triceps',), far=far)]
        if end:
            o.append(mv((80, 42), (112, 26), 8))

        return ''.join(o)
    return two(panel(False), panel(True), 188, '起始：让三头充分拉长', '结束：上臂贴近头侧不动')


# =============== 下肢 ===============
@fig('ex_legpress', 370, 150)
def _():
    fl = 139

    def panel(end):
        hip = (56, 114)
        o = [floor(fl), pad((62, 122), (38, 80)), pad((50, 124), (74, 124)), frame((60, 128), (60, fl))]
        if end:
            j = J(hip, torso=-120, thigh=-27, shin=-4, foot=-80, uarm=70, farm=40)
            px = 124
        else:
            j = J(hip, torso=-120, thigh=-66, shin=36, foot=-80, uarm=70, farm=40)
            px = 101
        o += [frame((px - 3, j['toe'][1] - 6), (px + 3, j['ankle'][1] + 8), 4), frame((px + 2, 100), (px + 34, 112)),
              frame((40, fl - 6), (166, fl - 6), 1.2)]
        o.append(man(j, hi=('quads', 'glutes')))
        if end:
            o.append(mv((104, 78), (124, 76), -4))

        return ''.join(o)
    return two(panel(False), panel(True), 150, '底部：下背和骨盆贴住靠垫', '顶端：膝盖不锁死')


@fig('ex_legext', 370, 150)
def _():
    fl = 139

    def panel(end):
        hip = (62, 98)
        o = [floor(fl), pad((54, 107), (96, 107)), pad((50, 100), (42, 50)), frame((70, 111), (70, fl))]
        j = J(hip, torso=-100, thigh=0, shin=6 if end else 98, foot=-84 if end else 8, uarm=80, farm=30)
        r = _add(j['ankle'], _v((6 if end else 98) - 90, 8))
        o += [frame((96, 100), r, 1.6), roller(r)]
        o.append(man(j, hi=('quads',)))
        if end:
            o.append(mv((102, 128), (130, 110), 8))
        return ''.join(o)
    return two(panel(False), panel(True), 150, '起始', '结束：顶端停半秒')


@fig('ex_legcurl', 370, 150)
def _():
    fl = 139

    def panel(end):
        hip = (58, 98)
        o = [floor(fl), pad((50, 107), (88, 107)), pad((46, 100), (34, 52)), frame((66, 111), (66, fl))]
        j = J(hip, torso=-106, thigh=0, shin=112 if end else 6, foot=20 if end else -84, uarm=80, farm=30)
        r = _add(j['ankle'], _v((112 if end else 6) + 90, 8))
        o += [frame((92, 104), r, 1.6), roller(r), L(78, 86, 92, 86, 's-far', 7)]
        o.append(man(j, hi=('hams',)))
        if end:
            o.append(mv((126, 112), (96, 134), -8))
        return ''.join(o)
    return two(panel(False), panel(True), 150, '起始：腿后侧被拉长', '结束')


@fig('ex_boxsquat', 370, 150)
def _():
    fl = 136

    def panel(bottom):
        o = [floor(fl), R(44, 110, 40, fl - 110, 'f-surf2', 3, ' stroke="var(--fig-line)" stroke-width="1.2"')]
        ank = (100.4, 131.5)
        if bottom:
            j = J((72, 101), torso=-64, thigh=0, knee=(106, 101), ankle=ank, el=(100, 78), hand=(96, 62))
        else:
            j = J((104.5, 66), torso=-86, knee=(101.5, 99.5), ankle=ank, el=(118, 46), hand=(114, 30))
        o.append(man(j, hi=('quads', 'glutes')))
        o.append(dumbbell((j['hand'][0] + 3, j['hand'][1] + 2), 90, 15))
        return ''.join(o)
    return two(panel(False), panel(True), 150, '站立', '轻触箱面：背挺直，往后坐')


@fig('ex_hipthrust', 370, 150)
def _():
    fl = 132

    def panel(top_):
        o = [floor(fl), R(18, 100, 42, fl - 100, 'f-surf2', 3, ' stroke="var(--fig-line)" stroke-width="1.2"')]
        sh = (58, 93)
        ank = (132, 127)
        if top_:
            hip = (98, 93)
            j = J(hip, torso=180, knee=(132, 95), ankle=ank, uarm=20, farm=10, head=200)
        else:
            hip = (88.6, 118.7)
            j = J(hip, torso=220, knee=(115.4, 99.7), ankle=ank, uarm=40, farm=60, head=215)
        o.append(man(j, hi=('glutes',), hi2=('hams',)))
        o.append(barbell((hip[0] + 3, hip[1] - 11), 10))
        return ''.join(o)
    return two(panel(False), panel(True), 150, '底部', '顶端：收紧臀部，不拱腰')


@fig('ex_calf', 370, 172)
def _():
    fl = 160

    def panel(up):
        toe = (98, 146)
        ank = (90.3, 136.8) if up else (86.7, 150.1)
        kn = (ank[0] + 1, ank[1] - 32)
        hip = (kn[0] - 1, kn[1] - 34)
        j = J(hip, torso=-88, knee=kn, ankle=ank, foot=50 if up else -20, uarm=80, farm=20)
        o = [floor(fl), R(92, 148, 40, fl - 148, 'f-surf2', 3, ' stroke="var(--fig-line)" stroke-width="1.2"'), frame((116, 30), (116, 148), 1.4)]
        o.append(man(j, hi=('calves',)))
        if not up:
            o.append(note(16, 146, '脚跟沉到最低'))
        return ''.join(o)
    return two(panel(False), panel(True), 172, '底部', '顶端')


# =============== 核心与脊柱 ===============
@fig('ex_plank', 370, 132)
def _():
    fl = 122

    def panel(bad):
        sh = (50, 92)
        o = [floor(fl)]
        if bad:
            hip = (89, 110)
            j = J(hip, torso=204.8, knee=(123, 112), ankle=(155, 114), foot=90, el=(50, 115), hand=(71, 115), head=170)
            o.append(man(j, bend=-7))
        else:
            hip = (89.1, 100.3)
            j = J(hip, torso=192, thigh=12, shin=12, foot=90, el=(50, 115), hand=(71, 115), head=185)
            o.append(man(j, hi=('abs',)))
            o.append(L(36, 86, 160, 113, 's-hi', 1, '3 3'))
        return ''.join(o)
    return two(panel(False), panel(True), 132, '要这样：耳、肩、髋、踝一条线', '不要这样：塌腰')


@fig('ex_deadbug', 370, 132)
def _():
    fl = 124

    def panel(end):
        hip = (100, 114)
        o = [floor(fl)]
        if end:
            j = J(hip, torso=180, thigh=-90, shin=0, uarm=196, farm=192)
            far = J(hip, torso=180, thigh=-22, shin=-14, foot=-70, uarm=-90, farm=-90)
        else:
            j = J(hip, torso=180, thigh=-90, shin=0, uarm=-90, farm=-90)
            far = J(hip, torso=180, thigh=-90, shin=0, uarm=-90, farm=-90)
        o.append(man(j, hi=('abs',), far=far if end else None))
        return ''.join(o)
    return two(panel(False), panel(True), 132, '起始：下背贴地', '对侧手脚伸出，下背不离地')


@fig('hinge', 370, 158)
def _():
    fl = 146

    def panel(bad):
        ank = (84, 142)
        kn = (88, 110)
        hip = (70, 82)
        o = [floor(fl)]
        if bad:
            j = J(hip, torso=-28, knee=kn, ankle=ank, uarm=88, farm=88)
            o.append(man(j, bend=9))
        else:
            j = J(hip, torso=-32, knee=kn, ankle=ank, uarm=88, farm=88)
            o.append(man(j, hi=('glutes', 'hams')))
            sh = j['sh']
            o.append(L(hip[0] - 8, hip[1] - 4 - 9, sh[0] + 16, sh[1] - 10 - 9, 's-hi', 1, '3 3'))
        o.append(dumbbell((j['hand'][0], j['hand'][1] + 3), 0))
        return ''.join(o)
    return two(panel(False), panel(True), 158, '要这样：躯干是直板，动的是髋', '不要这样：弓背')
