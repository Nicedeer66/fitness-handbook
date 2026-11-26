"""补充的动作图：自由重量、居家动作、原来缺图的动作和活动度练习。沿用 pose.py 的小人和器械画法。"""
from .base import *
from .pose import J, man, floor, pad, frame, barbell, dumbbell, cable, roller, note, mv, two, front, top, _add, _v


def _plate(p, r=20):
    return (C(p[0], p[1], r, 'f-surf2', ' stroke="var(--fig-ink)" stroke-width="1.4"') + C(p[0], p[1], 3.2, 'f-ink'))


# ============ 杠铃自由重量 ============
@fig('ex_bbsquat', 370, 160)
def _():
    fl = 148

    def panel(bottom):
        ank = (92, 143)
        o = [floor(fl)]
        if bottom:
            hip = (70, 110)
            j = J(hip, torso=-56, knee=(104, 108), ankle=ank, foot=0)
            bar = (j['sh'][0] - 6, j['sh'][1] + 5)
            j['el'] = (bar[0] - 12, bar[1] + 14)
            j['hand'] = (bar[0] - 3, bar[1])
        else:
            hip = (90, 77)
            j = J(hip, torso=-90, knee=(91, 110), ankle=ank, foot=0)
            bar = (j['sh'][0] - 6, j['sh'][1] + 5)
            j['el'] = (bar[0] - 10, bar[1] + 16)
            j['hand'] = (bar[0] - 3, bar[1])
        o.append(man(j, hi=('quads', 'glutes'), hi2=('erector',)))
        o.append(barbell(bar, 9))
        o.append(L(ank[0] - 2, 22, ank[0] - 2, fl, 's-hi', 1, '3 3'))
        return ''.join(o)
    return two(panel(False), panel(True), 160, '站立：杠在脚掌中部上方', '底部：杠仍在同一条竖线上')


@fig('ex_deadlift', 370, 160)
def _():
    fl = 146

    def panel(lock):
        ank = (92, 141)
        o = [floor(fl)]
        if lock:
            hip = (90, 76)
            j = J(hip, torso=-90, knee=(91, 109), ankle=ank, el=(92, 59), hand=(95, 80))
            bar = (95, 80)
        else:
            hip = (70, 96)
            j = J(hip, torso=-32, knee=(104, 114), ankle=ank, el=(103, 99), hand=(98, 124))
            bar = (98, 124)
        o.append(_plate(bar, 20))
        o.append(man(j, hi=('glutes', 'hams'), hi2=('erector', 'quads')))
        o.append(C(bar[0], bar[1], 3.2, 'f-ink'))
        return ''.join(o)
    return two(panel(False), panel(True), 160, '起始：背平直，杠贴小腿', '锁定：髋膝同时伸直，不后仰')


@fig('ex_ohp', 370, 190)
def _():
    fl = 180

    def panel(top_):
        hip = (92, 109)
        if top_:
            j = J(hip, torso=-90, knee=(92, 142), ankle=(92, 174), el=(95, 46), hand=(93, 26))
        else:
            j = J(hip, torso=-90, knee=(92, 142), ankle=(92, 174), el=(102, 89), hand=(104, 68))
        o = [floor(fl), man(j, hi=('delt',), hi2=('triceps', 'abs'))]
        o.append(barbell(j['hand'], 9))
        if top_:
            o.append(mv((122, 66), (112, 32), 6))
        return ''.join(o)
    return two(panel(False), panel(True), 190, '起始：杠在锁骨前', '顶端：杠在头顶正上方')


# ============ 居家 ============
@fig('ex_splitsquat', 370, 150)
def _():
    fl = 140

    def panel(bottom):
        o = [floor(fl)]
        fa = (124, 135)
        ra = (50, 128)
        if bottom:
            hip = (92, 102)
            far = J(hip, knee=(124, 103), ankle=fa, foot=0, uarm=95, farm=90)
            j = J(hip, torso=-90, knee=(84, 134), ankle=ra, foot=95, uarm=92, farm=88)
        else:
            hip = (100, 72)
            far = J(hip, knee=(113, 104), ankle=fa, foot=0, uarm=95, farm=90)
            j = J(hip, torso=-90, knee=(76, 98), ankle=ra, foot=95, uarm=92, farm=88)
        o.append(man(j, hi=('quads', 'glutes'), far=far))
        return ''.join(o)
    return two(panel(False), panel(True), 150, '起始', '底部：后膝接近地面，躯干直立')


@fig('ex_bandrow', 370, 136)
def _():
    fl = 126

    def panel(end):
        hip = (56, 118)
        o = [floor(fl)]
        if end:
            j = J(hip, torso=-95, thigh=0, shin=0, foot=-90, el=(38, 108), hand=(57, 110))
        else:
            j = J(hip, torso=-76, thigh=0, shin=0, foot=-90, el=(88, 96), hand=(108, 102))
        toe = j['toe']
        o.append(L(j['hand'][0], j['hand'][1], toe[0], toe[1] + 4, 's-hi2', 2.2))
        o.append(man(j, hi=('lats',), hi2=('biceps',)))
        return ''.join(o)
    return two(panel(False), panel(True), 136, '起始：弹力带绕过脚掌', '结束：挺胸，肘往后带')


# ============ 原来缺图的器械动作 ============
@fig('ex_apull', 370, 166)
def _():
    def panel(end):
        cx = 88
        sy = 40 if end else 66
        s, d = front(cx, sy, (45, 175) if end else (165, 175), hi=('lats',), legs='seat')
        by = d['hands'][0][1] - 2
        o = [L(cx - 60, by, cx + 60, by, 's-ink', 3), frame((cx - 60, by), (cx - 60, 162)), frame((cx + 60, by), (cx + 60, 162))]
        o.append(s)
        o.append(pad((cx - 24, sy + 86), (cx + 24, sy + 86), 7))
        o.append(frame((cx, sy + 90), (cx, 162), 1.4))
        if end:
            o.append(mv((cx + 44, 76), (cx + 44, 50), -6))
        return ''.join(o)
    return two(panel(False), panel(True), 166, '起始：手臂伸直（背面看）', '结束：下巴过杆，膝盖压在垫上')


@fig('ex_csrow', 370, 150)
def _():
    fl = 140

    def panel(end):
        hip = (62, 108)
        kw = dict(torso=-45, knee=(78, 128), ankle=(70, 136), foot=0)
        if end:
            j = J(hip, el=(74, 96), hand=(88, 108), **kw)
        else:
            j = J(hip, el=(98, 110), hand=(100, 131), **kw)
        sh = j['sh']
        o = [floor(fl), pad((hip[0] + 8, hip[1] + 4), (sh[0] + 9, sh[1] + 9), 9), frame((88, 112), (88, fl)), frame((52, 112), (52, fl))]
        o.append(man(j, hi=('lats',), hi2=('biceps', 'delt')))
        o.append(L(j['hand'][0] - 5, j['hand'][1], j['hand'][0] + 5, j['hand'][1], 's-ink', 3))
        if end:
            o.append(mv((120, 128), (98, 110), 6))
        return ''.join(o)
    return two(panel(False), panel(True), 150, '起始：胸贴靠垫，手臂垂直', '结束：肘向后，肩胛收紧')


@fig('ex_facepull', 370, 150)
def _():
    def panel(end):
        o = [C(88, 30, 4, 'f-surf2', ' stroke="var(--fig-ink)" stroke-width="1.3"')]
        s, hands = top(88, 100, (-40, -130) if end else (-82, -96), hi=('rdelt', 'upback'))
        for hx, hy in hands:
            o.append(L(hx, hy, 88, 32, 's-ink', 1.1))
        o.append(s)
        for hx, hy in hands:
            o.append(C(hx, hy, 3.5, 'f-ink'))
        return ''.join(o)
    return two(panel(False), panel(True), 150, '起始（俯视）', '结束：手到耳侧，肘抬高')


# ============ 核心 ============
@fig('ex_sideplank', 370, 132)
def _():
    """侧桥动作示意：要这样，头、肩、髋、踝一条线；不要这样，髋往下掉"""
    fl = 124

    def panel(bad):
        o = [floor(fl)]
        sh = (52, 92)
        hip = (100, 116) if bad else (100, 104)
        ank = (152, 118)
        import math
        ta = math.degrees(math.atan2(sh[1] - hip[1], sh[0] - hip[0]))
        j = J(hip, torso=ta, knee=((hip[0] + ank[0]) / 2, (hip[1] + ank[1]) / 2 + (3 if bad else 0)), ankle=ank, foot=-70,
              el=(52, 118), hand=(74, 119), head=ta + (20 if bad else 0))
        o.append(man(j, hi=() if bad else ('abs',)))
        if not bad:
            o.append(L(36, 86, 162, 116, 's-hi', 1, '3 3'))
        return ''.join(o)
    return two(panel(False), panel(True), 132, '要这样：头、肩、髋、踝一条线', '不要这样：髋往下掉')


@fig('ex_birddog', 370, 132)
def _():
    """鸟狗式动作示意：从四点跪姿起始，伸出对侧手脚，背平，骨盆不转"""
    fl = 124

    def panel(ext):
        o = [floor(fl)]
        hip = (66, 90)
        far_leg = dict(knee=(66, 120), ankle=(36, 121)) if not ext else dict(knee=(32, 90), ankle=(4, 92))
        far = J(hip, el=(106, 105), hand=(106, 120), foot=180, **far_leg)
        if ext:
            j = J(hip, torso=0, knee=(66, 120), ankle=(36, 121), foot=180, el=(128, 87), hand=(149, 84), head=-8)
        else:
            j = J(hip, torso=0, knee=(66, 120), ankle=(36, 121), foot=180, el=(106, 105), hand=(108, 120), head=20)
        o.append(man(j, hi=('abs', 'erector') if ext else (), hi2=('glutes',) if ext else (), far=far))
        if ext:
            o.append(L(0, 88, 160, 88, 's-hi', 1, '3 3'))
        return ''.join(o)
    return two(panel(False), panel(True), 132, '起始：四点跪姿', '伸出对侧手脚：背平，骨盆不转')


@fig('ex_bridge', 370, 132)
def _():
    fl = 124

    def panel(top_):
        sh = (34, 117)
        ank = (112, 119)
        if top_:
            hip = (73, 99)
            kn = (106, 88)
        else:
            hip = (73, 115)
            kn = (100, 92)
        import math
        ta = math.degrees(math.atan2(sh[1] - hip[1], sh[0] - hip[0]))
        j = J(hip, torso=ta, knee=kn, ankle=ank, foot=0, el=(56, 121), hand=(76, 121), head=180)
        o = [floor(fl), man(j, hi=('glutes',) if top_ else (), hi2=('hams',) if top_ else ())]
        if top_:
            o.append(L(28, 119, 112, 84, 's-hi', 1, '3 3'))
        return ''.join(o)
    return two(panel(False), panel(True), 132, '起始：仰卧屈膝', '顶端：肩、髋、膝一条线，不拱腰')


# ============ 活动度 ============
@fig('mob_hipflexor', 370, 150)
def _():
    fl = 140

    def panel(push):
        o = [floor(fl)]
        hip = (96, 100) if push else (88, 100)
        far = J(hip, knee=(126, 102), ankle=(124, 135), foot=0, uarm=92, farm=90)
        j = J(hip, torso=-90, knee=(70, 134), ankle=(40, 134), foot=180, uarm=100, farm=80)
        o.append(man(j, hi=('quads',) if push else (), far=far))
        if push:
            o.append(arrow(80, 82, 100, 82, 's-hi', 1.6, 6))
        return ''.join(o)
    return two(panel(False), panel(True), 150, '起始：半跪，躯干直立', '髋向前送，后腿前侧有拉伸感')


@fig('mob_doorway', 370, 124)
def _():
    def panel(fwd):
        cy = 70 if not fwd else 62
        o = [L(30, 54, 30, 120, 's-ink', 4), L(146, 54, 146, 120, 's-ink', 4)]
        s, hands = top(88, cy, (-8, -84), hi=('chest',) if fwd else ())
        o.append(s)
        if fwd:
            o.append(arrow(88, 106, 88, 92, 's-hi', 1.6, 6))
        return ''.join(o)
    return two(panel(False), panel(True), 124, '俯视：前臂贴住门框', '身体向前迈半步，胸前有拉伸感即可')


@fig('mob_tspine', 370, 132)
def _():
    fl = 124

    def panel(ext):
        o = [floor(fl), roller((66, 114), 9)]
        hip = (112, 118)
        sh = (74, 103) if not ext else (74, 106)
        import math
        ta = math.degrees(math.atan2(sh[1] - hip[1], sh[0] - hip[0]))
        j = J(hip, torso=ta, knee=(136, 96), ankle=(142, 123), foot=0, el=(60, 88), hand=(58, 104),
              head=(ta + 25) if ext else (ta - 15))
        o.append(man(j))
        return ''.join(o)
    return two(panel(False), panel(True), 132, '泡沫轴放在上背，双手抱头', '上背沿着泡沫轴向后伸展，腰不离地')
