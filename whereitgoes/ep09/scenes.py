from kit import *

BAUB = ((-70, -80, CORAL), (50, -110, GOLD), (-30, -200, BLUE), (48, -230, PINK), (0, -320, GOLD), (-96, -40, BLUE), (88, -50, CORAL))
DUSK = hx('3B3F7A'); DUSK2 = hx('8E7FC0')


def xtree(c, x, y, s, key, f, face='smile', eyes='dot', look=(0, 0), rot=0.0, deco=0.0, sq=1.0, col=PINE, plain=False):
    """x, y = foot of the trunk; about 300 wide and 470 tall at s=1"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    wline(c, [(0, 0), (0, -70)], (key, 't'), f, lw=34, col=INK, amp=0.6); wline(c, [(0, -2), (0, -70)], (key, 't2'), f, lw=20, col=hx('8A5A33'), amp=0.4)
    for k in range(3):
        w = 150 - k * 34; yb = -52 - k * 104
        wpoly(c, [(-w, yb), (0, yb - 190), (w, yb)], (key, k), f, 1.5); fs(c, col, 9)
    if not plain: facef(c, 0, -118, 58, face, look, eyes)
    if deco > 0.01:
        for i, (bx, by, bc) in enumerate(BAUB):
            c.new_path(); c.arc(bx, by, 15 * deco, 0, 2 * math.pi); fs(c, bc, 5)
        c.save(); c.translate(0, -456); c.scale(deco, deco)
        c.new_path()
        for i in range(10):
            r = 44 if i % 2 == 0 else 19; a = -math.pi / 2 + i * math.pi / 5
            (c.move_to if i == 0 else c.line_to)(r * math.cos(a), r * math.sin(a))
        c.close_path(); fs(c, GOLD, 6); c.restore()
    c.restore()


def needles(c, x, y, g, n=7, w=160, a=1.0):
    for i in range(n):
        ph = (g * 0.9 + i / n) % 1
        nx = x - w / 2 + (i * 0.37 % 1) * w + 14 * math.sin(g * 3 + i); ny = y + 190 * ph
        c.save(); c.translate(nx, ny); c.rotate(i + g * 2); c.rectangle(-9, -2.5, 18, 5); rgb(c, PINED, a * (1 - ph)); c.fill(); c.restore()


def snow(c, g, n=36, a=0.9, seed=4):
    r = random.Random(seed)
    for i in range(n):
        bx = r.uniform(0, W); by = r.uniform(0, H); sp = r.uniform(110, 240); sz = r.uniform(5, 11); ph = r.uniform(0, 6.28)
        c.new_path(); c.arc(bx + 24 * math.sin(g * 1.3 + ph), (by + g * sp) % (H + 40) - 20, sz, 0, 2 * math.pi); rgb(c, WHITE, a * (0.5 + 0.5 * sz / 11)); c.fill()


def home(c, f, x, base, col=hx('8E6FA3'), lit=True):
    wrect(c, x, base - 420, 400, 420, ('hm', x), f); fs(c, col, 9)
    wpoly(c, [(x - 40, base - 420), (x + 200, base - 600), (x + 440, base - 420)], ('rf', x), f); fs(c, hx('5A4777'), 9)
    c.new_path(); c.move_to(x - 30, base - 428); c.line_to(x + 200, base - 600); c.line_to(x + 430, base - 428)
    c.curve_to(x + 300, base - 440, x + 100, base - 470, x - 30, base - 428); rgb(c, SNOW); c.fill()
    rrect(c, x + 60, base - 330, 110, 110, 10); fs(c, hx('FFE29A') if lit else GLASS, 7)
    rrect(c, x + 240, base - 250, 110, 250, 12); fs(c, hx('B5553C'), 8)
    c.new_path(); c.arc(x + 262, base - 120, 8, 0, 2 * math.pi); rgb(c, GOLD); c.fill()


def trashcan(c, f, x, base):
    wrect(c, x - 70, base - 200, 140, 200, ('tc', x), f); fs(c, STEELD, 9)
    for i in range(3):
        wline(c, [(x - 40 + i * 40, base - 180), (x - 40 + i * 40, base - 24)], ('tcl', i), f, lw=6, amp=0.5, a=0.5)
    rrect(c, x - 86, base - 232, 172, 36, 12); fs(c, STEEL, 9)


def street(c, f, g, sky=(DUSK, DUSK2)):
    bg(c, *sky)
    home(c, f, 30, 1300)
    home(c, f, 700, 1300, hx('7868A8'), lit=False)
    c.rectangle(0, 1300, W, 110); rgb(c, SNOW); c.fill()
    c.rectangle(0, 1400, W, 520); rgb(c, hx('4A4F6E')); c.fill()
    c.move_to(0, 1400); c.line_to(W, 1400); rgb(c, INK); c.set_line_width(9); c.stroke()


def scene1(c, t, f, g):
    bg(c, hx('2E8FC4'), hx('134E7A'))
    c.rectangle(0, 1450, W, 500); rgb(c, hx('D9C08A')); c.fill()
    xtree(c, 540, 1440, 1.7, 'hero', f, face='o', eyes='big', look=(math.sin(g*2), 0), rot=0.025*math.sin(g*4))
    for i, (x, y, col, d) in enumerate(((260, 990, GOLD, 1), (820, 1200, CORAL, -1))):
        fish(c, x + 24*math.sin(g*3+i), y + 12*math.sin(g*4+i), 0.95, col, d, wag=math.sin(g*12))
    caption(c, t, -1, [[("CHRISTMAS TREES...", CREAM)], [("UNDERWATER?", GOLD)]], y=300, size=86, pop=False)


def scene2(c, t, f, g):
    bg(c, hx('1F2A5C'), hx('5B4E9A'))
    floor(c, 1420, SNOW)
    for r_ in range(3):
        for i in range(6):
            idx = r_ * 6 + i; k = eback(seg(t, 0.2 + idx * 0.07, 0.5 + idx * 0.07))
            if k > 0.01:
                xtree(c, 110 + i * 172 + (40 if r_ % 2 else 0), 990 + r_ * 150, (0.4 + 0.06 * r_) * k, ('lt', idx), f, plain=True, col=(PINE, PINED, hx('4FAE7C'))[idx % 3])
    for i in range(10):
        x = 60 + i * 107; y = 720 + 34 * math.sin(i * 0.7 + 1)
        c.new_path(); c.arc(x, y, 13, 0, 2 * math.pi); rgb(c, (CORAL, GOLD, GREEN, BLUE, PINK)[i % 5], 0.6 + 0.4 * math.sin(g * 5 + i)); c.fill()
    hk = eback(seg(t, 1.7, 2.1))
    if hk > 0.01:
        xtree(c, 540, 1470, 0.86 * hk, 'hero', f, face='grin', look=(0, -0.4), deco=ease(seg(t, 2.1, 2.6)), rot=0.03 * math.sin(g * 5))
    snow(c, g, 24, 0.7)
    caption(c, t, 0.2, [[("THE US BUYS", CREAM)], [("25 TO 30 MILLION", GOLD)], [("REAL TREES A YEAR.", CREAM)]], y=290, size=74)
    strip(c, 1560 - 30, ["Source: National Christmas Tree Association."], seg(t, 1.2, 1.6), size=32)


def scene3(c, t, f, g):
    street(c, f, g, sky=(hx('9FD3F5'), hx('E9F6FF')))
    trashcan(c, f, 900, 1392)
    tx = lerp(-340, 330, eout(seg(t, 0.2, 1.5)))
    up = ease(seg(t, 2.0, 2.9))
    hx_, hy_ = lerp(690, tx - 60, up), lerp(1392, 1392 - 290, up) - 240 * math.sin(up * math.pi)
    truck(c, tx, 1440, 1.1, f, g, col=GREEN, label=["TREE", "RECYCLING"], lsize=46)
    xtree(c, hx_, hy_, lerp(0.8, 0.5, up), 'hero', f, face='o' if t < 2.9 else 'smile', eyes='big' if t < 2.9 else 'dot', look=(-0.8, 0), rot=lerp(0.26, -1.2, up) if up < 1 else -1.3)
    wk = ease(seg(t, 1.5, 2.0))
    stick(c, lerp(tx + 120, 610, wk), 1392 - 190, 1.0, 'wk', f, lh=(-40, -30), rh=(84, -150 - 120 * math.sin(up * math.pi)), face='smile', shirt=ORANGE, hat='cap', look=(0.5, 0))
    snow(c, g, 18, 0.7)
    caption(c, t, 0.2, [[("FIRST: REMOVE DECORATIONS.", CREAM)], [("USE A LOCAL TREE PROGRAM.", GOLD)]], y=300, size=68)
    strip(c, 1560 - 30, ["Source: National Christmas Tree Association."], seg(t, 1.2, 1.6), size=32)


def scene4(c, t, f, g):
    bg(c, hx('CFEFD9'), hx('F6FFF4'))
    floor(c, 1400, hx('B9DDB0'))
    # pile
    pk = seg(t, 1.2, 4.2)
    c.save(); c.translate(880, 1400); c.scale(1, 0.55 + 0.35 * pk); c.new_path(); c.arc(0, 0, 100 + 110 * pk, math.pi, 2 * math.pi); c.close_path(); c.restore(); fs(c, hx('9A6B3F'), 8)
    # chips
    for i in range(16):
        ph = (g * 1.6 + i / 16) % 1
        if t > 1.1:
            x = 700 + 190 * ph; y = 870 - 150 * math.sin(ph * math.pi) + 430 * ph * ph
            c.save(); c.translate(x, y); c.rotate(i + g * 9); c.rectangle(-10, -5, 20, 10); rgb(c, (hx('9A6B3F'), PINE, hx('C89B63'))[i % 3]); c.fill(); c.restore()
    # trees going in
    for i, t0 in enumerate((0.5, 1.9, 3.2)):
        u = seg(t, t0, t0 + 0.9)
        if 0 < u < 1:
            x, y = lerp(60, 400, u), 1120 - 120 * math.sin(u * math.pi)
            xtree(c, x, y, 0.5 * (1 - 0.3 * ein(u)), ('in', i), f, plain=True, rot=1.57, col=(PINED, hx('4FAE7C'), PINE)[i])
    # chipper
    sh = 5 * math.sin(g * 40) * (1 if t > 0.9 else 0)
    wpoly(c, [(280, 1010 + sh), (420, 1070 + sh), (420, 1190 + sh), (280, 1250 + sh)], 'fun', f); fs(c, STEELD, 9)
    rrect(c, 410, 1000 + sh, 300, 300, 26); fs(c, ORANGE, 10)
    wpoly(c, [(600, 1010 + sh), (660, 1010 + sh), (760, 850 + sh), (700, 820 + sh)], 'chu', f); fs(c, STEELD, 9)
    facef(c, 560, 1150 + sh, 80, 'grin', (-0.6, 0), 'dot')
    for wx in (470, 650):
        c.new_path(); c.arc(wx, 1350, 50, 0, 2 * math.pi); fs(c, IRON, 9); c.new_path(); c.arc(wx, 1350, 16, 0, 2 * math.pi); rgb(c, STEEL); c.fill()
    sweat(c, 150, 1070, 0.8, g, f, n=3)
    xtree(c, 150 + 3 * math.sin(g * 40), 1400, 0.62, 'hero', f, face='o', eyes='big', look=(0.9, -0.1), rot=0.03 * math.sin(g * 28))
    caption(c, t, 0.2, [[("MANY ARE CHIPPED", CREAM)], [("INTO MULCH.", GOLD)]], y=300, size=80)
    strip(c, 1500, ["Source: National Christmas Tree Association."], seg(t, 1.2, 1.6), size=32)


def scene5(c, t, f, g):
    bg(c, hx('FFD9A0'), hx('FFF1D6'))
    c.new_path(); c.arc(260, 760, 80, 0, 2 * math.pi); rgb(c, hx('FFF3B0')); c.fill()
    c.rectangle(0, 1010, W, 150); rgb(c, GRASSD); c.fill()
    for i in range(22):
        x = 20 + i * 50; h = 60 + 30 * math.sin(i * 1.7); sw = 10 * math.sin(g * 2 + i)
        wline(c, [(x, 1020), (x + sw, 1020 - h)], ('gr', i), f, lw=9, col=GRASS, amp=0.8)
    c.rectangle(0, 1150, W, 800); rgb(c, WATER); c.fill()
    for j in range(4):
        y = 1210 + j * 90; off = (g * 70 + j * 40) % 120
        for i in range(-1, 10):
            c.new_path(); c.arc(i * 120 + off, y, 46, math.pi * 1.1, math.pi * 1.9); rgb(c, WHITE, 0.5); c.set_line_width(7); c.stroke()
    k = eout(seg(t, 0.2, 1.0))
    for i in range(5):
        tk = eback(seg(t, 0.5 + i * 0.3, 0.9 + i * 0.3))
        if tk > 0.01 and i != 2:
            xtree(c, 190 + i * 172 + 100, 1290 + 6 * math.sin(g * 3 + i), 0.44 * tk, ('m', i), f, plain=True, rot=-1.57, col=(PINED, PINE, PINE, hx('4FAE7C'), PINED)[i])
    hk = eback(seg(t, 1.1, 1.5))
    if hk > 0.01:
        xtree(c, 190 + 2 * 172 + 120, 1290 + 6 * math.sin(g * 3), 0.5 * hk, 'hero', f, face='smile', eyes='closed', rot=-1.57)
    for i in range(6):
        x = 130 + i * 172
        wrect(c, x - 14, 1150 - 110 * k, 28, 110 * k + 230, ('po', i), f); fs(c, WOODD, 8)
    for y in (1215, 1345):
        rrect(c, 110, y - 13, 900, 26, 8); fs(c, WOOD, 8)
    wv = (g * 0.9) % 1
    c.new_path(); c.arc(60 - 40 + 60 * wv, 1240, 60, math.pi, 2 * math.pi); rgb(c, WHITE, 0.7 * (1 - wv)); c.set_line_width(12); c.stroke()
    caption(c, t, 0.2, [[("IN LOUISIANA, THEY", CREAM)], [("SHIELD THE MARSH.", GOLD)]], y=300, size=78)
    strip(c, 1490, ["Jefferson Parish, Louisiana.", "Source: Jefferson Parish Environmental Affairs."], seg(t, 1.2, 1.6), size=32)


def fish(c, x, y, s, col, d=1, key='fi', f=0, wag=0.0):
    c.save(); c.translate(x, y); c.scale(s * d, s)
    c.new_path(); c.move_to(-50, 0); c.line_to(-96, -34 + 10 * wag); c.line_to(-96, 34 + 10 * wag); c.close_path(); fs(c, col, 7)
    c.save(); c.scale(1, 0.62); c.new_path(); c.arc(0, 0, 62, 0, 2 * math.pi); c.restore(); fs(c, col, 8)
    c.new_path(); c.arc(28, -8, 10, 0, 2 * math.pi); rgb(c, WHITE); c.fill(); c.new_path(); c.arc(31, -8, 5, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.restore()


def scene6(c, t, f, g):
    bg(c, hx('2E8FC4'), hx('134E7A'))
    for i in range(5):
        c.new_path(); c.move_to(120 + i * 210, 0); c.line_to(40 + i * 210 + 40 * math.sin(g + i), 1500); c.line_to(140 + i * 210 + 40 * math.sin(g + i), 1500); c.line_to(170 + i * 210, 0); c.close_path(); rgb(c, WHITE, 0.05); c.fill()
    c.rectangle(0, 1430, W, 500); rgb(c, hx('D9C08A')); c.fill()
    for i in range(7):
        sw = 14 * math.sin(g * 2 + i)
        wline(c, [(60 + i * 160, 1440), (60 + i * 160 + sw, 1330 - 30 * (i % 3))], ('wd', i), f, lw=10, col=hx('3FA37A'), amp=0.8)
    sink = eout(seg(t, 0.15, 1.5)); ty = lerp(420, 1432, sink)
    wob = 0.12 * math.sin(g * 4) * (1 - sink)
    rrect(c, 540 - 70, ty - 6, 140, 60, 10); fs(c, STEEL, 8)
    xtree(c, 540, ty, 1.0, 'hero', f, face='o' if sink < 1 else 'grin', eyes='big' if sink < 1 else 'dot', look=(0, 0.6) if sink < 1 else (math.sin(g * 2), 0), rot=wob)
    for i in range(6):
        bk = (g * 0.5 + i / 6) % 1
        c.new_path(); c.arc(540 - 110 + i * 44 + 16 * math.sin(g * 3 + i), ty - 380 - 600 * bk, 8 + 12 * bk, 0, 2 * math.pi); rgb(c, WHITE, 0.6 * (1 - bk)); c.set_line_width(4); c.stroke()
    for i, (x0, y0, x1, y1, col, d, t0) in enumerate(((-150, 900, 400, 1180, GOLD, 1, 1.9), (1250, 1000, 690, 1250, CORAL, -1, 2.3), (-150, 1150, 430, 1330, PINK, 1, 2.7))):
        u = eout(seg(t, t0, t0 + 1.0))
        if u > 0:
            fish(c, lerp(x0, x1, u), lerp(y0, y1, u) + 8 * math.sin(g * 4 + i), 0.62, col, d, wag=math.sin(g * 14 + i))
    sign(c, 540, 760, "FISH HOTEL", GOLD, INK, size=44, rot=-0.04, k=eback(seg(t, 3.0, 3.3)), padx=24)
    caption(c, t, 0.15, [[("SOME PROGRAMS SINK THEM", CREAM)], [("IN LAKES.", GOLD)]], y=300, size=84, t1=2.1)
    caption(c, t, 2.2, [[("NOW IT IS", CREAM)], [("A FISH HOTEL.", GOLD)]], y=300, size=88)
    strip(c, 1500, ["Source: Texas Parks and Wildlife."], seg(t, 1.0, 1.4), size=32)


def scene7(c, t, f, g):
    bg(c, hx('FF7A5A'), hx('FFC83D'))
    c.save(); c.translate(540, 1400); c.scale(1, 0.2); c.new_path(); c.arc(0, 0, 440, 0, 2 * math.pi); c.restore(); rgb(c, INK, 0.16); c.fill()
    hop = abs(math.sin(g * 5)) * 26
    xtree(c, 280, 1400 - hop, 1.25, 'hero', f, face='grin', look=(0.5, -0.2), deco=1.0, rot=0.04 * math.sin(g * 5))
    xtree(c, 800, 1400, 1.25, 'fake', f, face='flat', look=(-0.5, 0), col=hx('7FC9C0'), deco=1.0)
    sign(c, 280, 1470, "REAL", GREEN, WHITE, size=50, k=eback(seg(t, 0.5, 0.8)))
    sign(c, 800, 1470, "FAKE", hx('5E8FA8'), WHITE, size=50, k=eback(seg(t, 0.75, 1.05)))
    k = eback(seg(t, 0.3, 0.6))
    c.save(); c.translate(540, 1010); c.scale(k, k); c.new_path(); c.arc(0, 0, 62, 0, 2 * math.pi); fs(c, INK, 0); txt(c, "VS", 0, 20, 56, GOLD); c.restore()
    caption(c, t, 0.12, [[("REAL TREE", CREAM)], [("OR FAKE TREE?", GOLD)]], y=300, size=90)
    strip(c, 640, ["Use approved local collection programs.", "Sources: NCTA, TPWD, Jefferson Parish."], seg(t, 1.2, 1.6), size=30)


SCENES = [(0.0, 3.6, scene1), (3.6, 8.0, scene2), (8.0, 12.4, scene3), (12.4, 16.8, scene4), (16.8, 21.2, scene5),
          (21.2, 25.6, scene6), (25.6, 30.0, scene7)]
draw = make_draw(SCENES)


# November 26 retention edit. Values: output seconds, source start, source end.
from edit import edited_draw
EDIT = [(2.4, 0, 3.6), (4, 8, 12.4), (4, 12.4, 16.8), (4, 16.8, 21.2), (5.6, 21.2, 25.6), (3, 25.6, 28.6)]
DURATION = sum(shot[0] for shot in EDIT)
draw = edited_draw(SCENES, EDIT)
