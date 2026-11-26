from kit import *

SLOT = (705, 1040); HIP = (300, 1250)
_q = random.Random(5); QR = [(i, j) for i in range(7) for j in range(5) if _q.random() < 0.55]


def box(c, x, y, s, key, f, face='smile', eyes='dot', rot=0.0, look=(0, 0), sq=1.0, ret=True, col=CARD, grade=None, flaps=0.0):
    """hero parcel, x, y = centre, 240 x 200"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    if flaps > 0:
        for sg in (-1, 1):
            c.save(); c.translate(sg * 120, -100); c.rotate(sg * (0.5 + 0.9 * flaps) - (math.pi if sg > 0 else 0) * 0)
            wrect(c, -118 if sg > 0 else 0, -14, 118, 22, (key, 'fl', sg), f, 1.0); fs(c, CARDD, 7); c.restore()
    wrect(c, -120, -100, 240, 200, (key, 'b'), f, 1.5); fs(c, col, 10)
    c.rectangle(-22, -98, 44, 196); rgb(c, hx('F1D9A8'), 0.8); c.fill()
    facef(c, 0, 8, 84, face, look, eyes)
    if ret:
        c.save(); c.translate(-60, -66); c.rotate(-0.14); rrect(c, -54, -22, 108, 44, 10); fs(c, CORAL, 6); txt(c, "RETURN", 0, 10, 25, WHITE); c.restore()
    c.save(); c.translate(74, 66); rrect(c, -34, -22, 68, 44, 6); fs(c, WHITE, 5)
    for k in range(5):
        c.rectangle(-25 + k * 10, -13, 4 if k % 2 else 6, 26); rgb(c, INK); c.fill()
    c.restore()
    if grade:
        L, gcol, gk = grade
        if gk > 0.01:
            c.save(); c.translate(78, -62); c.rotate(0.2); c.scale(gk, gk); c.new_path(); c.arc(0, 0, 46, 0, 2 * math.pi); fs(c, gcol, 7)
            txt(c, L, 0, 22, 60, WHITE); c.restore()
    c.restore()


def shop(c, f, g):
    bg(c, hx('FFE9C9'), hx('FFD3A0'))
    c.save(); c.translate(250, 690); c.rotate(-0.06); rrect(c, -170, -80, 340, 160, 22); fs(c, CORAL, 9); txt(c, "SALE", 0, 38, 104, WHITE); c.restore()
    for i, x in enumerate((90, 250, 410)):
        wline(c, [(x, 560), (x, 610)], ('sl', i), f, lw=6, amp=0.6)
    floor(c, 1440, WOOD)


def kiosk(c, f, g, gape=0.0, gulp=0.0):
    c.save(); c.translate(705, 1440); c.scale(1 + 0.05 * gulp, 1 - 0.05 * gulp); c.translate(-705, -1440)
    rrect(c, 540, 880, 330, 560, 36); fs(c, TEALD, 10)
    rrect(c, 566, 902, 278, 84, 16); fs(c, GOLD, 7); txt(c, "RETURNS", 705, 963, 50, INK)
    rrect(c, 580, SLOT[1] - 36 - gape / 2, 250, 72 + gape, 24); fs(c, DARK, 8)
    rrect(c, 600, 1180, 210, 160, 14); fs(c, GLASS, 7)
    for (i, j) in QR:
        c.rectangle(618 + i * 25, 1198 + j * 25, 20, 20); rgb(c, INK); c.fill()
    c.restore()


def scene1(c, t, f, g):
    bg(c, hx('FFE9C9'), hx('FFD3A0'))
    floor(c, 1430, WOOD)
    for x, label, col in ((260, "BACK ON SALE", GREEN), (780, "ANOTHER ROUTE", CORAL)):
        sign(c, x, 1280, label, col, WHITE, size=39, padx=22)
        wline(c, [(540, 1080), (x, 1190)], ('fork', x), f, lw=18, col=INK)
    hop = 20 * math.sin(g * 7)
    box(c, 540 + 38*math.sin(g*3), 910 + hop, lerp(2.2, 1.7, ease(seg(t, 0.4, 1.6))), 'hero', f, face='o', eyes='big', look=(math.sin(g*3), 0.5), rot=0.035*math.sin(g*6))
    caption(c, t, -1, [[("RETURNED.", CREAM)], [("NOT ALWAYS RESOLD.", GOLD)]], y=300, size=84, pop=False)


BX = (130, 310, 490, 670, 850)


def scene2(c, t, f, g):
    bg(c, hx('FFE3B8'), hx('FFC98F'))
    for i, (x, y, s) in enumerate(((180, 640, 1.0), (760, 720, 0.8))):
        cloud(c, x + 20 * math.sin(g * 0.4 + i), y, s, 0.55)
    belt(c, -80, 1160, 1215, g, f, sp=160, key='b2')
    out = ein(seg(t, 2.3, 3.5)); back = ease(seg(t, 2.3, 3.5))
    for i, x in enumerate(BX):
        k = eback(seg(t, 0.25 + i * 0.22, 0.6 + i * 0.22))
        if k <= 0.01: continue
        if i < 4:
            box(c, x + 900 * out, 1215 - 56 * k, 0.56 * k, ('o', i), f, face='smile', ret=False, col=hx('E3B57E'), look=(0.6, 0))
        else:
            hop = math.sin(seg(t, 1.7, 2.3) * math.pi) * 90
            hxp = x - 310 * back
            box(c, hxp, 1215 - 56 * k - hop, 0.62 * k, 'hero', f, face='o' if t > 1.7 else 'smile', eyes='big' if t > 1.7 else 'dot',
                look=(-0.8, 0) if t > 1.7 else (0.6, 0), rot=-0.12 * math.sin(seg(t, 1.7, 2.3) * math.pi))
            a = ease(seg(t, 1.9, 2.6))
            if a > 0:
                c.save(); c.translate(hxp, 1010)
                c.new_path(); c.arc(0, 0, 92, -0.15, -0.15 - (math.pi + 0.5) * a, ) if False else None
                c.new_path(); c.arc_negative(0, 0, 92, -0.1, -0.1 - (math.pi + 0.3) * a); rgb(c, INK); c.set_line_width(34); c.set_line_cap(1); c.stroke()
                c.new_path(); c.arc_negative(0, 0, 92, -0.1, -0.1 - (math.pi + 0.3) * a); rgb(c, GOLD); c.set_line_width(18); c.stroke()
                if a > 0.95:
                    ang = -0.1 - (math.pi + 0.3); ex, ey = 92 * math.cos(ang), 92 * math.sin(ang)
                    c.new_path(); c.move_to(ex - 46, ey + 4); c.line_to(ex + 46, ey + 4); c.line_to(ex + 4, ey + 62); c.close_path(); fs(c, GOLD, 8)
                c.restore()
    caption(c, t, 0.25, [[("US ONLINE SALES:", CREAM)], [("19.3% RETURNED", GOLD)]], y=300, size=78)
    strip(c, 1450, ["2025 estimate, measured by sales value.", "Source: NRF and Happy Returns."], seg(t, 1.2, 1.6))


def scene3(c, t, f, g):
    bg(c, hx('2A2350'), hx('5A2F6E'))
    n0 = 6
    for r in range(5):
        n = n0 - r; y = 1500 - r * 134
        for i in range(n):
            idx = r * 7 + i
            k = eback(seg(t, 0.15 + idx * 0.045, 0.45 + idx * 0.045))
            if k > 0.01:
                x = 540 + (i - (n - 1) / 2) * 158
                box(c, x, y - 64 * k, 0.62 * k, ('p', idx), f, face=('smile', 'flat', 'o')[idx % 3], ret=(idx % 2 == 0),
                    col=(CARD, hx('E3B57E'), hx('C98F52'))[idx % 3], look=(0, -0.5))
    k = eback(seg(t, 1.5, 1.9))
    if k > 0.01:
        wob = 0.08 * math.sin(g * 6)
        box(c, 540, 1500 - 5 * 134 - 70 * k, 0.68 * k, 'hero', f, face='o', eyes='big', rot=wob, look=(0, -0.8))
    v = 849.9 * eout(seg(t, 0.7, 3.2))
    panel(c, 540, 570, 860, 180, "$%.1f BILLION" % v, 104, eback(seg(t, 0.5, 0.85)))
    caption(c, t, 0.2, [[("ALL US RETAIL RETURNS", CREAM)], [("2025 ESTIMATE:", GOLD)]], y=290, size=72)
    strip(c, 1560 - 110, ["2025 estimate. Source: NRF and Happy Returns."], seg(t, 1.6, 2.0), size=34)


def warehouse(c, f, g):
    bg(c, NIGHT2, NIGHT)
    for i, sx in enumerate((40, 400, 760)):
        rrect(c, sx, 600, 280, 560, 10); rgb(c, hx('313C63')); c.fill()
        for r in range(3):
            c.rectangle(sx, 760 + r * 150, 280, 12); rgb(c, hx('1B2540')); c.fill()
            for j in range(3):
                rrect(c, sx + 22 + j * 84, 760 + r * 150 - 72, 66, 72, 6); rgb(c, hx('4A5687')); c.fill()
    c.new_path(); c.move_to(540, 430); c.line_to(140, 1300); c.line_to(940, 1300); c.close_path(); rgb(c, hx('FFE9A8'), 0.10); c.fill()
    rrect(c, 500, 400, 80, 44, 12); fs(c, GOLD, 7)
    floor(c, 1470, hx('1B2540'), line=False)


def scene4(c, t, f, g):
    warehouse(c, f, g)
    rrect(c, 110, 1255, 780, 46, 12); fs(c, WOOD, 9)
    for lx in (150, 820):
        wrect(c, lx, 1300, 34, 180, ('tl', lx), f); fs(c, WOODD, 8)
    sw = math.sin(g * 2.4)
    stick(c, 270, 1262, 1.0, 'wk', f, lh=(-50, -40), rh=(150 + 70 * sw, -150), legs=False, face='flat', eyes='dot', shirt=ORANGE, hat='cap', look=(0.8, 0.3))
    fl = ease(seg(t, 0.3, 0.9))
    box(c, 610, 1255 - 96, 0.96, 'hero', f, face='o' if t < 3.2 else 'smile', eyes='big' if t < 3.2 else 'dot', look=(-0.7 + 0.3 * sw, -0.2), flaps=fl,
        rot=0.02 * math.sin(g * 26) * (1 if t < 3.2 else 0))
    if t < 3.2: sweat(c, 610, 1150, 0.9, g, f, n=3, a0=-2.3, da=0.75)
    mx, my = 270 + 150 + 70 * sw + 40, 1262 - 150 - 46
    wline(c, [(mx - 34, my + 34), (mx - 4, my + 4)], 'mgh', f, lw=14)
    c.new_path(); c.arc(mx + 30, my - 30, 50, 0, 2 * math.pi); rgb(c, GLASS, 0.55); c.fill_preserve(); rgb(c, INK); c.set_line_width(10); c.stroke()
    for i, (x, L, col, sub) in enumerate(((300, "NEW", GREEN, "SEALED?"), (540, "USED", GOLD, "WORKING?"), (780, "FIX?", CORAL, "DAMAGED?"))):
        k = eback(seg(t, 1.9 + i * 0.4, 2.2 + i * 0.4))
        if k > 0.01:
            c.save(); c.translate(x, 800); c.scale(k, k); c.new_path(); c.arc(0, 0, 76, 0, 2 * math.pi); fs(c, col, 9); fit(c, L, 0, 18, 48, 140, INK if i == 1 else WHITE); c.restore()
            fit(c, sub, x, 930, 38, 220, CREAM, a=k)
    caption(c, t, 0.2, [[("FIRST:", CREAM)], [("CHECK ITS CONDITION.", GOLD)]], y=300, size=80)


BINS = ((230, "SELL", GREEN, "RESALE"), (540, "GIVE", GOLD, "DONATION"), (850, "RECYCLE", CORAL, "RECYCLING"))


def scene5(c, t, f, g):
    warehouse(c, f, g)
    belt(c, -80, 1160, 640, g, f, sp=200, key='b5', legs=False)
    for i, (x, L, col, sub) in enumerate(BINS):
        rrect(c, x - 128, 1130, 256, 300, 26); fs(c, hx('2B2F3A'), 9)
    for i, (x, L, col, sub) in enumerate(BINS):
        t0 = 0.55 + i * 1.05
        if t > t0 - 0.5:
            d = ein(seg(t, t0, t0 + 0.5)); sl = ease(seg(t, t0 - 0.5, t0))
            bx = lerp(x - 260, x, sl); by = lerp(640 - 62, 1290, d)
            if d < 1:
                box(c, bx, by, 0.62, ('d', i), f, face=('grin', 'flat', 'o')[i], eyes=('dot', 'dot', 'big')[i], rot=d * (0.5, -0.4, 0.8)[i],
                    grade=None, col=(CARD, hx('E3B57E'), hx('B98552'))[i], look=(0, 0.8))
        land = seg(t, t0 + 0.5, t0 + 0.75); sq = 1 - 0.06 * math.sin(land * math.pi)
        c.save(); c.translate(x, 1430); c.scale(1 / sq, sq); c.translate(-x, -1430)
        rrect(c, x - 128, 1236, 256, 196, 26); fs(c, col, 9); fit(c, L, x, 1354, 56, 226, INK if i == 1 else WHITE); c.restore()
        k = eback(seg(t, t0 + 0.45, t0 + 0.75))
        sign(c, x, 1078, sub, CREAM, INK, size=36, k=k, padx=22, lw=7)
    caption(c, t, 0.2, [[("SOME POSSIBLE ROUTES:", CREAM)], [("SELL, DONATE, RECYCLE", GOLD)]], y=300, size=74)
    strip(c, 1510, ["Routes vary by seller and condition.", "Example: Amazon returns process."], seg(t, 0.8, 1.1), size=31)


def scene6(c, t, f, g):
    bg(c, hx('FFE9C9'), hx('FFD3A0'))
    floor(c, 1440, WOOD)
    for ux in (70, 700):
        rrect(c, ux, 720, 28, 720, 6); fs(c, WOODD, 7)
    for sy in (1010, 1300):
        rrect(c, 70, sy, 658, 30, 8); fs(c, WOODD, 8)
    for i, (x, col) in enumerate(((190, hx('7FB4F5')), (610, hx('F5A6C0')))):
        box(c, x, 1010 - 62, 0.6, ('s', i), f, face='smile', ret=False, col=col, look=(0.5 if i == 0 else -0.5, 0))
    for i, (x, col) in enumerate(((210, hx('C7E08A')), (400, hx('E3B57E')), (590, hx('B9A7F0')))):
        box(c, x, 1300 - 62, 0.6, ('s2', i), f, face='flat', ret=False, col=col)
    gk = eback(seg(t, 0.45, 0.75))
    walk = ease(seg(t, 1.9, 2.8)); take = ease(seg(t, 2.95, 3.5))
    bxp = lerp(1300, 880, walk)
    hand = (bxp - 120, 1250 - 150)
    hp = lerp2((400, 1010 - 86), (hand[0] - 30, hand[1] - 40), take)
    stick(c, bxp, 1250, 1.0, 'buyer', f, lh=(-120, -150) if t > 2.8 else (-40, -20), rh=(50, -20), face='grin' if take > 0.5 else 'smile', shirt=PURPLE,
          lf=(-45 + 30 * math.sin(g * 9) * (1 if 0 < walk < 1 else 0), 190), rf=(45 - 30 * math.sin(g * 9) * (1 if 0 < walk < 1 else 0), 190), look=(-0.8, 0.1))
    box(c, hp[0], hp[1], lerp(0.84, 0.6, take), 'hero', f, face='grin' if t > 0.7 else 'o', eyes='dot' if t > 0.7 else 'big', grade=None,
        look=(0.6, 0) if t > 1.9 else (0, 0), rot=0.06 * math.sin(g * 5) * take)
    if take < 0.05:
        c.save(); c.translate(400, 1070); c.rotate(-0.05); rrect(c, -92, -24, 184, 48, 10); fs(c, WHITE, 6); txt(c, "OPEN BOX", 0, 12, 30, RED); c.restore()
    for i in range(3):
        hk = seg(t, 3.5 + i * 0.2, 4.0 + i * 0.2)
        if 0 < hk:
            heart(c, hp[0] - 40 + i * 50, hp[1] - 150 - 70 * hk - 20 * i, 0.5 + 0.2 * i, CORAL, 1 - 0.5 * hk)
    caption(c, t, 0.15, [[("ONE POSSIBLE ENDING:", CREAM)], [("AN OPEN-BOX SALE.", GOLD)]], y=300, size=92, t1=2.0)
    caption(c, t, 2.1, [[("SOMEONE NEW", CREAM)], [("TAKES IT HOME.", GOLD)]], y=300, size=84)


def scene7(c, t, f, g):
    bg(c, hx('FF7A5A'), hx('FFC83D'))
    hop = abs(math.sin(g * 5)) * 46
    c.new_path(); c.save(); c.translate(540, 1215); c.scale(1, 0.25); c.arc(0, 0, 210 - hop, 0, 2 * math.pi); c.restore(); rgb(c, INK, 0.18); c.fill()
    box(c, 540, 1040 - hop, 1.5, 'hero', f, face='grin', look=(0, -0.3), grade=None, rot=0.05 * math.sin(g * 5))
    qmarks(c, ((200, 760, -0.3), (880, 800, 0.3), (250, 1330, 0.2)), t, 0.7)
    caption(c, t, 0.12, [[("WHAT DID YOU", CREAM)], [("LAST SEND BACK?", GOLD)]], y=300, size=88)
    strip(c, 1450, ["Sources: NRF / Happy Returns (2025).", "Amazon returns process (2026)."], seg(t, 1.0, 1.4), size=31)


SCENES = [(0.0, 3.6, scene1), (3.6, 8.0, scene2), (8.0, 12.4, scene3), (12.4, 16.8, scene4), (16.8, 21.2, scene5),
          (21.2, 25.6, scene6), (25.6, 30.0, scene7)]
draw = make_draw(SCENES)


# November 26 retention edit. Values: output seconds, source start, source end.
from edit import edited_draw
EDIT = [(2.4, 0, 3.6), (4, 12.4, 16.8), (4.4, 16.8, 21.2), (4.4, 21.2, 25.6), (4.4, 3.6, 8), (3, 25.6, 28.6)]
DURATION = sum(shot[0] for shot in EDIT)
draw = edited_draw(SCENES, EDIT)
