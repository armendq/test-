from lib import *

# ------------------------------------------------------------------ fountain world (scenes 1 and 7)
TOUR_HIP = (300, 1570); TOUR_S = 1.25
HAND_UP = (70, -330); HAND_DOWN = (100, -105)


def hand_world(rel): return (TOUR_HIP[0] + rel[0] * TOUR_S, TOUR_HIP[1] + rel[1] * TOUR_S)


def flight(tt):
    u = seg(tt, -0.3, 2.3)
    p0 = hand_world(HAND_UP); p1 = (760, 1240)
    x = lerp(p0[0], p1[0], u); y = lerp(p0[1], p1[1], u) - 4 * 520 * u * (1 - u)
    return x, y, lerp(70, 34, u), u


def facade(c, f, ox=0, oy=0, sc=1.0, key='fac'):
    c.save(); c.translate(ox, oy); c.scale(sc, sc)
    wpoly(c, [(110, 400), (540, 250), (970, 400)], (key, 'ped'), f); fs(c, STONE, 9)
    wrect(c, 130, 400, 820, 650, (key, 'b'), f); fs(c, STONE, 9)
    wrect(c, 105, 392, 870, 46, (key, 'cor'), f); fs(c, STONED, 8)
    for i, cx in enumerate((290, 540, 790)):
        w = 150 if i != 1 else 210; top = 570 if i != 1 else 520
        c.new_path(); c.move_to(cx - w / 2, 1050); c.line_to(cx - w / 2, top + w / 2)
        c.arc(cx, top + w / 2, w / 2, math.pi, 2 * math.pi); c.line_to(cx + w / 2, 1050); c.close_path(); fs(c, STONED, 8)
    for cx in (412, 668):
        wrect(c, cx - 18, 470, 36, 580, (key, 'col', cx), f, 1.5); fs(c, CREAM, 7)
    wpoly(c, [(498, 745), (582, 745), (604, 1000), (476, 1000)], (key, 'stb'), f); fs(c, STONE, 7)
    wcirc(c, 540, 700, 36, (key, 'sth'), f); fs(c, STONE, 7)
    c.restore()


def fountain_world(c, f, g, rh, face, eyes, look=(0, 0)):
    bg(c, hx('9FDCF5'), hx('FFE9C9'))
    wcirc(c, 905, 300, 74, 'sun', f, amp=3); rgb(c, hx('FFE28A')); c.fill()
    for i, (x, y, r) in enumerate([(150, 620, 60), (980, 760, 50)]):  # clouds
        dx = math.sin(g * 0.3 + i) * 10
        wcirc(c, x + dx, y, r * 1.6, ('cl', i), f, ry=r * 0.55); rgb(c, WHITE, 0.85); c.fill()
    facade(c, f)
    c.rectangle(0, 1300, W, H - 1300); c.set_source(grad(0, 1300, 0, H, [(0, hx('F1DDB9')), (1, hx('E2C795'))])); c.fill()
    for i, (x, y, r) in enumerate([(205, 1085, 72), (365, 1105, 56), (705, 1105, 62), (865, 1082, 76), (540, 1112, 52)]):
        wcirc(c, x, y, r, ('rock', i), f, ry=r * 0.6); fs(c, SAND, 8)
    wcirc(c, 540, 1262, 482, 'rim', f, amp=3, k=18, ry=166); fs(c, STONE, 10)
    wcirc(c, 540, 1250, 436, 'water', f, amp=3, k=18, ry=128); fs(c, TEAL, 8)
    for i in range(4):
        ph = (g * 0.5 + i * 0.25) % 1
        c.save(); c.translate(330 + i * 140, 1250 + (i % 2) * 40 - 20); c.scale(1, 0.3)
        c.new_path(); c.arc(0, 0, 20 + 60 * ph, 0, 2 * math.pi); c.restore()
        rgb(c, WHITE, 0.7 * (1 - ph)); c.set_line_width(5); c.stroke()
    wpoly(c, [(470, 1000), (610, 1000), (650, 1190), (430, 1190)], 'casc', f); fs(c, hx('8FE3E6'), 8)
    for i in range(4):
        ph = (g * 1.4 + i * 0.25) % 1
        xx = 480 + i * 40
        wline(c, [(xx, 1010 + ph * 120), (xx - (2 - i) * 4, 1050 + ph * 120)], ('cs', i), f, lw=9, col=WHITE, amp=1.0, a=0.9)
    for i, x0 in enumerate((335, 745)):
        sgn = -1 if i == 0 else 1
        pts = [(x0 + sgn * (k * 4), 1060 + k * 20 + math.sin(g * 9 + k + i) * 2) for k in range(8)]
        wline(c, pts, ('jet', i), f, lw=14, col=WHITE, amp=2.0, a=0.9)
    for i in range(5):  # cobbles
        y = 1500 + i * 85
        wline(c, [(60 + i * 37 % 200 + k * 260, y) for k in range(2)], ('cob', i), f, lw=6, col=hx('D2B57F'), amp=1.5)
    hd = stick(c, TOUR_HIP[0], TOUR_HIP[1], TOUR_S, 'tour', f, lh=(-62, -30), rh=rh, face=face, eyes=eyes,
               shirt=CORAL, look=look, bob=math.sin(g * 3) * 2)
    return hd


def draw_hero_flight(c, f, tt):
    x, y, r, u = flight(tt)
    x2, y2, _, _ = flight(tt + 0.02)
    vx, vy = x2 - x, y2 - y; n = math.hypot(vx, vy) or 1.0; vx, vy = vx / n, vy / n
    for i in range(3):  # speed lines trail behind the coin
        off = (i - 1) * r * 0.6
        bx = x - vx * r * 1.35 - vy * off; by = y - vy * r * 1.35 + vx * off
        ln = r * (1.2 if i == 1 else 0.8)
        wline(c, [(bx, by), (bx - vx * ln, by - vy * ln)], ('sp', i), f, lw=max(4, r * 0.1), col=WHITE, amp=1.0, a=0.95)
    flipv = math.cos(2 * math.pi * 1.6 * tt)
    coin(c, x, y, r, 'hero', f, face='o', eyes='big', flip=flipv, rot=math.sin(tt * 5) * 0.15)


def scene1(c, t, f, g):
    x, y, r, u = flight(t)
    k = ease(seg(t, 0.35, 1.5)); z = lerp(2.4, 1.0, k); fx, fy = lerp(x, 540, k), lerp(y, 960, k)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)
    fountain_world(c, f, g, HAND_UP, 'smile', 'closed')
    if u < 1.0:
        draw_hero_flight(c, f, t)
    else:
        q = eout(seg(t, 2.3, 2.6))
        for i in range(11):
            a = math.pi * (1.08 + 0.84 * i / 10)
            d = (70 + 110 * (i % 3) / 2) * q
            px, py = 760 + math.cos(a) * d, 1240 + math.sin(a) * d * 1.3 + 90 * q * q
            c.new_path(); c.arc(px, py, 13 * (1 - q * 0.5), 0, 2 * math.pi); fs(c, WHITE if i % 2 else TEAL, 5)
    c.restore()
    caption(c, t, -1, [[("WHERE DOES", CREAM)], [("YOUR COIN GO?", GOLD)]], y=300, size=92, pop=False)
    w = ein(seg(t, 2.36, 2.6))
    if w > 0:
        c.new_path(); c.arc(760, 1240, 2300 * w, 0, 2 * math.pi); rgb(c, hx('2CC7C4')); c.fill()


# ------------------------------------------------------------------ scene 2: underwater
_r = random.Random(7)
PX = 440
PILE = []
for ri, (py, pn, sp) in enumerate([(1470, 7, 112), (1378, 6, 112), (1290, 5, 110), (1205, 4, 108), (1124, 3, 106)]):
    for i in range(pn):
        PILE.append((PX + (i - (pn - 1) / 2) * sp + _r.uniform(-10, 10), py + _r.uniform(-8, 8), 55 + _r.uniform(-4, 5),
                     _r.random(), _r.random()))
BUB = [(_r.uniform(60, 1020), _r.uniform(0, 1), _r.uniform(8, 22), _r.uniform(0.12, 0.3)) for _ in range(20)]


def dentures(c, x, y, s, op, key, f):
    for sg in (-1, 1):
        yy = y + sg * (14 + op * 20) * s
        wcirc(c, x, yy + sg * 12 * s, 66 * s, (key, sg), f, ry=24 * s); fs(c, PINK, 6)
        for i in range(5):
            tx = x + (-48 + i * 24) * s
            rrect(c, tx - 11 * s, yy - 13 * s, 22 * s, 24 * s, 6 * s); fs(c, WHITE, 4)


def scene2(c, t, f, g):
    bg(c, hx('2CC7C4'), hx('0A5670'))
    z = 1.0 + 0.22 * ease(seg(t, 1.5, 3.9))
    c.save(); c.translate(540, 1500); c.scale(z, z); c.translate(-540, -1500)
    for i in range(4):  # light rays
        x0 = 120 + i * 270 + math.sin(g * 0.6 + i) * 40
        c.new_path(); c.move_to(x0, 0); c.line_to(x0 + 150, 0); c.line_to(x0 + 320, 1500); c.line_to(x0 - 60, 1500); c.close_path()
        rgb(c, WHITE, 0.07); c.fill()
    for i, (bx, ph, br, sp) in enumerate(BUB):
        yy = 1600 - ((g * sp + ph) % 1.0) * 1700
        c.new_path(); c.arc(bx + math.sin(g * 2 + i) * 14, yy, br, 0, 2 * math.pi); rgb(c, WHITE, 0.55); c.set_line_width(4); c.stroke()
    pts = [(-20, 1920), (-20, 1540)] + [(i * 110, 1530 + math.sin(i * 1.3) * 14) for i in range(11)] + [(1100, 1540), (1100, 1920)]
    c.new_path(); c.move_to(*pts[0]); [c.line_to(*p) for p in pts[1:]]; c.close_path(); fs(c, hx('CDB98F'), 8)
    for (x, y, r, a, b) in PILE:
        blink = ((g * 0.5 + a) % 1.0) < 0.06
        coin(c, x, y, r, ('p', int(x), int(y)), f, face=('smile' if b > 0.6 else None) if not blink else None,
             eyes='dot', look=(0, -1))
        if b <= 0.6 and not blink:
            rgb(c, INK)
            for sg in (-1, 1):
                c.new_path(); c.arc(x + sg * r * 0.3, y - r * 0.12, r * 0.09, 0, 2 * math.pi); c.fill()
    op = 0.0
    if 2.15 < t < 3.5: op = 0.5 + 0.5 * math.sin((t - 2.15) * 34)
    dentures(c, 858, 1440, 1.3, op, 'dent', f)
    # hero
    land = 1.7
    if t < land:
        u = ease(seg(t, 0.0, land))
        hy = lerp(-140, 1040, u); hxx = PX + 110 * math.sin(t * 3.4) * (1 - u)
        coin(c, hxx, hy, 74, 'hero', f, face='o', eyes='big', rot=math.sin(t * 3.4) * 0.35, look=(0, 1))
        for i in range(3):
            c.new_path(); c.arc(hxx + (i - 1) * 40, hy - 110 - i * 46 - (t * 200 % 60), 10 + i * 3, 0, 2 * math.pi)
            rgb(c, WHITE, 0.7); c.set_line_width(4); c.stroke()
    else:
        q = seg(t, land, land + 0.35); sq = 1 + 0.28 * math.sin(q * math.pi) * (1 - q)
        looking = t > 2.2
        coin(c, PX, 1040 + (sq - 1) * 40, 74, 'hero', f, face='flat' if looking else 'smile', eyes='big' if looking else 'dot',
             sx=sq, sy=1 / sq, look=(1.3, 0.6) if looking else (0, 0))
    c.restore()
    if t > 2.25:  # tag, screen space
        k = eback(seg(t, 2.25, 2.5))
        c.save(); c.translate(770, 1090); c.scale(k, k); c.rotate(-0.05)
        rrect(c, -252, -54, 504, 104, 26); rgb(c, CREAM); c.fill_preserve(); rgb(c, INK); c.set_line_width(7); c.stroke()
        txt(c, "also in there: dentures", 0, 16, 43, INK, HAND)
        c.restore()
        wline(c, [(880, 1152), (915, 1230), (925, 1300)], 'arr', f, lw=9)
        wline(c, [(893, 1272), (925, 1302), (950, 1268)], 'arr2', f, lw=9)
    caption(c, t, 0.3, [[("TOURISTS TOSS", CREAM)], [("ABOUT €5,000 A DAY", GOLD)]], y=300, size=84)
    a = 1 - seg(t, 0, 0.25)
    if a > 0: c.rectangle(0, 0, W, H); rgb(c, hx('2CC7C4'), a); c.fill()


# ------------------------------------------------------------------ scene 3: the sweep
C3 = [800, 748, 696, 644, 592, 540, 488, 436, 384, 332]
NOZ = (285, 1392)


def scene3(c, t, f, g):
    bg(c, hx('FF9E7A'), hx('FFDDA6'))
    c.save(); c.translate(540, 850); c.scale(1.2, 1.2); c.translate(-540, -850)
    wcirc(c, 540, 600, 300, 'sun3', f, amp=4); rgb(c, hx('FFF0B8'), 0.9); c.fill()
    facade(c, f, 135, 150, 0.75, 'fac3')
    wrect(c, -120, 925, 1320, 95, 'backrim', f); fs(c, STONE, 9)
    wrect(c, -120, 1470, 1320, 560, 'floor3', f); fs(c, STONED, 9)
    # water body
    wave = [(180 + i * 58, 1020 + math.sin(g * 3 + i * 0.9) * 7) for i in range(13)]
    c.new_path(); c.move_to(180, 1470); c.line_to(180, 1020)
    for p in wave: c.line_to(*p)
    c.line_to(876, 1470); c.close_path(); rgb(c, hx('7FE0E0'), 0.85); c.fill()
    sw = seg(t, 0.5, 2.3)
    bx = lerp(860, 560, ease(sw)) + (14 * math.sin(t * 10) if 0 < sw < 1 else 0)
    order = []
    for k, x0 in enumerate(C3):
        x = min(x0, bx - 62 - 30 * k)
        ts = 2.9 + 0.17 * (9 - k)
        order.append((k, x, seg(t, ts, ts + 0.3)))
    for k, x, u in sorted(order, key=lambda o: -o[0]):
        hero = (k == 0)
        if u >= 1: continue
        r = 50 if hero else 40
        px, py = lerp(x, NOZ[0] + 20, ein(u)), lerp(1470 - r, NOZ[1], ein(u)) - 60 * math.sin(u * math.pi)
        sc = 1 - 0.65 * u
        pushed = x < C3[k] - 1
        if hero:
            coin(c, px, py, r * sc, 'hero', f, face='grin' if u > 0 else ('o' if pushed else 'smile'),
                 eyes='closed' if u > 0 else ('big' if pushed else 'dot'), rot=u * 7, sx=1 + 0.5 * u, look=(-1, 0))
        else:
            coin(c, px, py, r * sc, ('c3', k), f, face=None, rot=u * 7 + (0.25 if pushed else 0))
            if u == 0:
                rgb(c, INK)
                for sg in (-1, 1):
                    c.new_path(); c.arc(px + sg * r * 0.3, py - r * 0.1, r * 0.1, 0, 2 * math.pi); c.fill()
    c.new_path(); c.move_to(180, 1470); c.line_to(180, 1020)
    for p in wave: c.line_to(*p)
    c.line_to(876, 1470); c.close_path(); rgb(c, TEAL, 0.16); c.fill()
    wline(c, wave, 'wl', f, lw=8, col=WHITE, amp=0.5, a=0.95)
    wrect(c, -120, 1000, 305, 480, 'lw', f); fs(c, STONE, 9)
    wrect(c, 868, 1000, 330, 480, 'rw', f); fs(c, STONE, 9)
    hands = ((-70, -95), (-34, -150))
    hipx, hipy = 915, 810
    top = (hipx - 20, hipy - 185)
    wline(c, [top, (bx, 1420)], 'pole', f, lw=13, col=WOODD)
    wrect(c, bx - 48, 1418, 96, 26, 'bh', f, 1.5); fs(c, CORAL, 7)
    for i in range(7):
        wline(c, [(bx - 40 + i * 13, 1444), (bx - 44 + i * 13, 1468)], ('br', i), f, lw=5)
    stick(c, hipx, hipy, 1.0, 'work', f, lh=hands[0], rh=hands[1], face='smile', shirt=ORANGE, hat='cap',
          look=(-1, 1), bob=math.sin(t * 10) * 2 if 0 < sw < 1 else 0)
    hk = eout(seg(t, 2.3, 2.8))
    if hk > 0:
        oy = -900 * (1 - hk)
        pts = [(150, 460 + oy), (150, 1250 + oy), (170, 1340 + oy), (220, 1385 + oy), (NOZ[0], NOZ[1] + oy)]
        wline(c, pts, 'hose1', f, lw=62, col=INK, amp=0.8)
        wline(c, pts, 'hose2', f, lw=44, col=hx('5B5F97'), amp=0.5)
        if 2.85 < t < 4.8:
            for i in range(3):
                ph = (t * 3 + i / 3) % 1
                c.new_path(); c.arc(NOZ[0] + 40, NOZ[1], 30 + 70 * (1 - ph), -0.7, 0.7); rgb(c, WHITE, 0.85 * ph); c.set_line_width(6); c.stroke()
    c.restore()
    caption(c, t, 0.2, [[("TWICE A WEEK,", CREAM)], [("ROME SWEEPS IT UP", GOLD)]], y=300, size=80)


# ------------------------------------------------------------------ scene 4: the count
STX = [500, 700, 900]
SYM = [("€", BLUE), ("$", GREEN), ("£", CORAL)]
NC = 31


def scene4(c, t, f, g):
    bg(c, hx('FFF3DC'), hx('FFE0B0'))
    gl = cairo.RadialGradient(540, 670, 60, 540, 670, 640)
    gl.add_color_stop_rgba(0, 1, 1, 1, 0.75); gl.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(gl); c.rectangle(0, 0, W, H); c.fill()
    c.rectangle(0, 1760, W, 160); rgb(c, hx('E9C99A')); c.fill()
    c.save(); c.translate(540, 1250); c.scale(1.13, 1.13); c.translate(-540, -1250)
    # volunteer behind table
    cyc = (t / 0.115) % 1 if 0.5 < t < 4.0 else 0
    rhh = lerp2((66, -70), (112, -150), math.sin(cyc * math.pi))
    stick(c, 170, 1345, 1.15, 'vol', f, lh=(-60, -40), rh=rhh, face='smile', shirt=GREEN, look=(1, 0), legs=False,
          bob=math.sin(t * 6) * 2)
    # table
    for lx in (70, 950):
        wrect(c, lx, 1480, 60, 330, ('leg4', lx), f); fs(c, WOODD, 8)
    wpoly(c, [(40, 1295), (1040, 1295), (1085, 1410), (-5, 1410)], 'tab', f); fs(c, WOOD, 9)
    wrect(c, -5, 1410, 1090, 84, 'apr', f); fs(c, WOODD, 9)
    # signs
    for j, x in enumerate(STX):
        wline(c, [(x, 1335), (x, 1085)], ('sp4', j), f, lw=9, col=WOODD)
        wrect(c, x - 52, 990, 104, 100, ('sc4', j), f, 2.0); fs(c, CREAM, 7)
        txt(c, SYM[j][0], x, 1066, 76, SYM[j][1])
    # stacks
    arrived = [0, 0, 0]; flying = []
    for i in range(NC):
        ti = 0.5 + 0.115 * i
        j = i % 3
        if t >= ti + 0.42: arrived[j] += 1
        elif t >= ti: flying.append((i, j, (t - ti) / 0.42))
    hero_landed = t >= 0.5 + 0.115 * (NC - 1) + 0.42
    for j, x in enumerate(STX):
        n = min(arrived[j], 11)
        for k in range(n):
            yy = 1345 - k * 14
            c.save(); c.translate(x, yy); c.scale(1, 0.34); c.new_path(); c.arc(0, 0, 50, 0, 2 * math.pi); c.restore(); fs(c, GOLD, 5)
        if j == 0 and hero_landed:
            q = seg(t, 0.5 + 0.115 * (NC - 1) + 0.42, 0.5 + 0.115 * (NC - 1) + 0.75); sq = 1 + 0.25 * math.sin(q * math.pi)
            coin(c, x, 1345 - n * 14 - 50, 54, 'hero', f, face='grin', eyes='closed', sx=sq, sy=1 / sq)
    # heap
    for i, (dx, dy) in enumerate([(-70, 0), (0, 6), (70, 0), (-36, -44), (36, -44), (0, -86)]):
        coin(c, 215 + dx, 1300 + dy, 44, ('heap', i), f, face=None, rot=i * 0.5)
    for i, j, u in flying:
        n = min(arrived[j], 11)
        p0 = (245, 1215); p1 = (STX[j], 1345 - n * 14 - (50 if i == NC - 1 else 14))
        px = lerp(p0[0], p1[0], u); py = lerp(p0[1], p1[1], u) - 4 * 200 * u * (1 - u)
        if i == NC - 1: coin(c, px, py, 54, 'hero', f, face='o', eyes='big', rot=u * 6.283)
        else: coin(c, px, py, 40, ('fl', i), f, face=None, rot=u * 5, flip=math.cos(u * 6))
    c.restore()
    # counter
    roll = eout(seg(t, 0.9, 3.9)); val = int(round(1860000 * roll / 1000.0)) * 1000
    done = seg(t, 3.9, 4.3); pul = 1 + 0.08 * math.sin(done * math.pi)
    c.save(); c.translate(540, 660); c.scale(pul, pul)
    rrect(c, -468 + 12, -118 + 14, 936, 236, 44); rgb(c, CORAL); c.fill()
    rrect(c, -468, -118, 936, 236, 44); rgb(c, INK); c.fill()
    txt(c, "€" + format(val, ","), 0, 48, 132, GOLD)
    c.restore()
    if t >= 3.9:
        for i in range(10):
            a = i * 0.628 + 0.3; d = 300 + 260 * eout(done)
            sparkle(c, 540 + math.cos(a) * d * 1.5, 660 + math.sin(a) * d * 0.55, 34 * (1 - done) + 8, GOLD, 1 - done * 0.8)
        k = eback(seg(t, 3.95, 4.2))
        c.save(); c.translate(540, 858); c.scale(k, k); c.rotate(-0.03)
        rrect(c, -160, -46, 320, 92, 26); rgb(c, CREAM); c.fill_preserve(); rgb(c, INK); c.set_line_width(7); c.stroke()
        txt(c, "IN 2025", 0, 21, 58, INK); c.restore()
    caption(c, t, 0.2, [[("WASHED. SORTED.", CREAM)], [("COUNTED.", GOLD)]], y=300, size=80)


# ------------------------------------------------------------------ scene 5: the canteen
PEOPLE = [(430, 1400, 1.1, BLUE, 1.3), (285, 1400, 1.1, GREEN, 2.5), (152, 1452, 0.82, PINK, 3.7)]


def scene5(c, t, f, g):
    bg(c, hx('FFEBC8'), hx('FFDCA8'))
    for i in range(14):  # tile band
        for j in range(2):
            if (i + j) % 2 == 0:
                c.rectangle(i * 80, 880 + j * 80, 80, 80); rgb(c, CORAL, 0.22); c.fill()
    c.save(); c.translate(540, 1380); c.scale(1.25, 1.25); c.translate(-540, -1380)
    c.rectangle(-200, 1590, W + 400, 600); rgb(c, hx('EBCB9B')); c.fill()
    wline(c, [(-200, 1590), (W + 200, 1590)], 'fl5', f, lw=8, amp=1.0)
    # cook
    serve = 0.0
    for (_, _, _, _, tp) in PEOPLE:
        serve = max(serve, math.sin(seg(t, tp - 0.55, tp + 0.15) * math.pi))
    lh = lerp2((-185, -215), (-262, -160), serve)
    hipx, hipy, cs = 880, 1400, 1.1
    stick(c, hipx, hipy, cs, 'cook', f, lh=lh, rh=(50, -40), face='smile', eyes='closed' if serve > 0.5 else 'dot',
          shirt=WHITE, hat='chef', look=(-1, 0), bob=math.sin(t * 4) * 2)
    # counter + pot
    wrect(c, 545, 1232, 255, 360, 'ctr', f); fs(c, CORAL, 9)
    wrect(c, 528, 1205, 290, 44, 'ctop', f); fs(c, CREAM, 8)
    steam(c, 672, 1070, g, 'st5', n=3, hgt=230, a=0.9)
    for sg in (-1, 1):
        c.new_path(); c.arc(672 + sg * 84, 1128, 20, 0, 2 * math.pi); rgb(c, INK); c.set_line_width(9); c.stroke()
    wrect(c, 597, 1085, 150, 122, 'pot', f); fs(c, TEALD, 9)
    c.save(); c.translate(672, 1085); c.scale(1, 0.22); c.new_path(); c.arc(0, 0, 79, 0, 2 * math.pi); c.restore(); fs(c, SOUP, 8)
    # ladle in cook's hand
    lx, ly = hipx + lh[0] * cs, hipy + lh[1] * cs
    wline(c, [(lx, ly), (lx - 20, ly + 70)], 'ladle', f, lw=9)
    c.new_path(); c.arc(lx - 22, ly + 78, 22, 0, math.pi); c.close_path(); fs(c, CREAM, 6)
    # people
    for i, (px, py, ps, col, tp) in enumerate(PEOPLE):
        got = t >= tp
        q = eback(seg(t, tp, tp + 0.3))
        hands = ((-36, -96), (36, -96)) if got else ((-52, -28), (52, -28))
        stick(c, px, py, ps, ('p5', i), f, lh=hands[0], rh=hands[1], face='smile' if got else 'flat',
              eyes='closed' if got else 'dot', shirt=col, look=(1, 0), bob=math.sin(t * 3 + i) * 2 + (8 * math.sin(seg(t, tp, tp + 0.4) * math.pi) if got else 0))
        if got:
            bx_, by_ = px, py - 100 * ps
            if i < 2:
                c.save(); c.translate(bx_, by_); c.scale(q, q); c.translate(-bx_, -by_)
                bowl(c, bx_, by_, 0.82 * ps, 1.0); c.restore()
                steam(c, bx_, by_ - 14, g + i, ('s5', i), n=2, hgt=90, a=0.8, spread=24, lw=6)
            else:  # grocery bag for the kid
                c.save(); c.translate(bx_, by_ + 10); c.scale(q, q)
                wline(c, [(-14, -30), (-30, -92)], 'bag1', f, lw=18, col=INK); wline(c, [(-14, -30), (-30, -92)], 'bag2', f, lw=10, col=hx('F2C078'))
                wcirc(c, 22, -62, 22, 'leaf', f); fs(c, GREEN, 5)
                wrect(c, -46, -40, 92, 84, 'bag', f, 1.5); fs(c, hx('D9A066'), 6)
                c.restore()
            hq = seg(t, tp + 0.1, tp + 1.3)
            if 0 < hq < 1:
                heart(c, px + 60 * ps, py - 300 * ps - 90 * hq, (0.5 + 0.5 * eback(hq * 2)) * ps, CORAL, 1 - ein(hq))
    c.restore()
    caption(c, t, 0.15, [[("THEN ROME GIVES IT", CREAM)], [("TO CHARITY", GOLD)]], y=300, size=80, t1=3.15)
    caption(c, t, 3.2, [[("HOT MEALS, GROCERIES", CREAM)], [("FOR PEOPLE IN NEED", GOLD)]], y=300, size=72)


# ------------------------------------------------------------------ scene 6: the payoff
def scene6(c, t, f, g):
    gl = cairo.RadialGradient(540, 1100, 80, 540, 1100, 1250)
    gl.add_color_stop_rgb(0, *hx('FFF0B0')); gl.add_color_stop_rgb(1, *hx('FFB26B'))
    c.set_source(gl); c.rectangle(0, 0, W, H); c.fill()
    m = seg(t, 1.15, 1.45)
    c.save(); c.translate(540, 1370); c.scale(1.22, 1.22); c.translate(-540, -1480)
    c.save(); c.translate(720, 1380); c.rotate(g * 0.25)
    for i in range(12):
        c.new_path(); c.move_to(0, 0); a0 = i * math.pi / 6
        c.line_to(math.cos(a0) * 2400, math.sin(a0) * 2400); c.line_to(math.cos(a0 + 0.2) * 2400, math.sin(a0 + 0.2) * 2400); c.close_path()
        rgb(c, WHITE, 0.05 + 0.13 * m); c.fill()
    c.restore()
    after = t >= 1.3
    spoon = eout(seg(t, 1.7, 2.1))
    rh = lerp2((70, -50), (104, -196), spoon)
    hd = stick(c, 380, 1530, 1.7, 'kid', f, lh=(-46, -40), rh=rh, face='grin' if after else 'o',
               eyes='closed' if after else 'dot', shirt=BLUE, look=(1.2, -0.9 + 1.4 * seg(t, 0.15, 1.15)), legs=False,
               bob=(10 * math.sin(seg(t, 1.3, 1.8) * math.pi)) + math.sin(t * 3) * 2)
    if spoon > 0:
        sx_, sy_ = 380 + rh[0] * 1.7, 1530 + rh[1] * 1.7
        wline(c, [(sx_, sy_ + 10), (sx_ + 6, sy_ - 76)], 'spoon', f, lw=10)
        wcirc(c, sx_ + 8, sy_ - 100, 24, 'spb', f, ry=30); fs(c, CREAM, 6)
    # table
    wpoly(c, [(60, 1480), (1020, 1480), (1090, 1600), (-10, 1600)], 'tab6', f); fs(c, WOOD, 9)
    wrect(c, -10, 1600, 1100, 90, 'apr6', f); fs(c, WOODD, 9)
    c.rectangle(-200, 1690, W + 400, 500); rgb(c, hx('F6C98C')); c.fill()
    # bowl
    pop = 1 + 0.18 * math.sin(m * math.pi)
    c.save(); c.translate(720, 1450); c.scale(pop, pop); c.translate(-720, -1450)
    bowl(c, 720, 1440, 2.1, eback(m)); c.restore()
    if m > 0.5:
        steam(c, 720, 1400, g, 'st6', n=3, hgt=260, a=0.95, spread=50, lw=11)
    # coin
    if t < 1.45:
        u = ease(seg(t, 0.1, 1.15))
        cy = lerp(790, 1385, u); r = 112 * (1 - ein(m))
        if r > 2:
            coin(c, 720 + math.sin(t * 4) * 26 * (1 - u), cy, r, 'hero', f, face='smile', eyes='closed',
                 flip=math.cos(u * math.pi * 4), rot=math.sin(t * 4) * 0.2)
    if m > 0:
        d = eout(seg(t, 1.15, 1.9))
        for i in range(12):
            a = i * math.pi / 6 + 0.2
            sparkle(c, 720 + math.cos(a) * (140 + 330 * d), 1400 + math.sin(a) * (110 + 260 * d), 40 * (1 - d) + 6,
                    WHITE if i % 2 else GOLD, 1 - d * 0.85)
    for i in range(3):
        hq = seg(t, 1.9 + i * 0.5, 3.6 + i * 0.5)
        if 0 < hq < 1:
            heart(c, 640 + i * 90 + math.sin(t * 3 + i) * 16, 1230 - 330 * hq, 0.9 + 0.3 * i, CORAL, 1 - ein(hq))
    c.restore()
    caption(c, t, 0.08, [[("AND YOUR COIN?", CREAM)]], y=320, size=84, t1=1.3)
    caption(c, t, 1.38, [[("YOUR WISH BECAME", CREAM)], [("SOMEONE'S DINNER", GOLD)]], y=300, size=84)
    if t > 2.3:
        k = eout(seg(t, 2.3, 2.6))
        c.save(); c.translate(540, 590)
        rrect(c, -385, -34, 770, 68, 22); rgb(c, INK, 0.85 * k); c.fill()
        txt(c, "Sources: Reuters, Caritas Roma. 2025 figures.", 0, 12, 33, CREAM, HAND, a=k)
        c.restore()


# ------------------------------------------------------------------ scene 7: loop bridge
def scene7(c, t, f, g):
    tt = g - 30.0
    up = ease(seg(g, 29.3, 29.7))
    rh = lerp2(HAND_DOWN, HAND_UP, up)
    hw = hand_world(rh)
    released = tt >= -0.3
    if released: x, y, r, u = flight(tt)
    else: x, y, r = hw[0] + 6, hw[1] - 52 - 6 * math.sin(g * 9), 70
    k = ease(seg(g, 29.2, 30.0)); z = lerp(1.0, 2.4, k); fx, fy = lerp(540, x, k), lerp(960, y, k)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)
    fountain_world(c, f, g, rh, 'smile' if released else 'grin', 'closed' if released else 'dot', look=(1, -0.6))
    if released: draw_hero_flight(c, f, tt)
    else: coin(c, x, y, r, 'hero', f, face='grin', eyes='dot', rot=math.sin(g * 9) * 0.12)
    c.restore()
    caption(c, t, 0.12, [[("GOT ANOTHER", CREAM)], [("COIN?", GOLD)]], y=300, size=92)


SCENES = [(0.0, 2.6, scene1), (2.6, 6.5, scene2), (6.5, 11.5, scene3), (11.5, 16.5, scene4), (16.5, 22.5, scene5),
          (22.5, 27.5, scene6), (27.5, 30.0, scene7)]
TR = 0.22


def draw(c, g, f):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= g < b or (i == len(SCENES) - 1 and g >= b):
            loc = g - a
            if i >= 2 and loc < TR:
                o = eout(loc / TR)
                pa, pb, pfn = SCENES[i - 1]
                c.save(); c.translate(0, -H * o); c.rectangle(0, 0, W, H); c.clip(); pfn(c, pb - pa - 0.001, f, pb - 0.001); c.restore()
                c.save(); c.translate(0, H * (1 - o)); c.rectangle(0, 0, W, H); c.clip(); fn(c, loc, f, g); c.restore()
            else:
                c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, loc, f, g); c.restore()
            return
