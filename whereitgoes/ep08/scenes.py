from kit import *

CY = 1235


def sock(c, x, y, s, rot, col=PINK, key='sk', f=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-22, -70); c.line_to(22, -70); c.line_to(22, 10); c.curve_to(24, 30, 70, 26, 70, 48); c.curve_to(70, 74, 20, 72, -4, 66)
    c.curve_to(-22, 60, -22, 40, -22, 20); c.close_path(); fs(c, col, 7)
    c.rectangle(-22, -70, 44, 20); rgb(c, WHITE); c.fill_preserve(); rgb(c, INK); c.set_line_width(6); c.stroke(); c.restore()


def tee(c, x, y, s, rot, col=TEAL, key='te', f=0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-40, -60); c.line_to(-90, -30); c.line_to(-70, 6); c.line_to(-46, -6); c.line_to(-46, 70); c.line_to(46, 70); c.line_to(46, -6)
    c.line_to(70, 6); c.line_to(90, -30); c.line_to(40, -60); c.curve_to(20, -40, -20, -40, -40, -60); c.close_path(); fs(c, col, 7); c.restore()


def scene1(c, t, f, g):
    bg(c, hx('FFE9C9'), hx('FFD3A0'))
    floor(c, 1430, WOOD)
    sign(c, 540, 660, "UNCLAIMED LUGGAGE", CREAM, INK, size=48)
    bag(c, 520, 1420, 1.55, 'hero', f, col=CORAL, face='o', eyes='big', look=(0.8, -0.2), sw=0.18*math.sin(g*6))
    sign(c, 765, 1020 + 14*math.sin(g*5), "FOR SALE", GOLD, INK, size=49, rot=-0.1)
    caption(c, t, -1, [[("A STORE BUYS", CREAM)], [("LOST AIRLINE BAGS.", GOLD)]], y=300, size=82, pop=False)


def scene2(c, t, f, g):
    bg(c, hx('CDEBFF'), hx('F3FAFF'))
    floor(c, 1390, hx('E3D5B8'))
    for i, (x, col, sh) in enumerate(((130, TEAL, BLUE), (345, GOLD, GREEN), (560, PURPLE, ORANGE))):
        k = eback(seg(t, 0.3 + i * 0.3, 0.65 + i * 0.3))
        if k <= 0.01: continue
        stick(c, x, 1390 - 152, 0.8, ('p', i), f, lh=(-50, -20), rh=(70, -60), face='grin', shirt=sh, bob=3 * math.sin(g * 6 + i))
        bag(c, x + 96, 1390, 0.4 * k, ('b', i), f, col=col, face='grin', look=(-0.6, -0.3))
        hb = (g * 0.8 + i * 0.3) % 1
        heart(c, x + 50, 1040 - 60 * hb, 0.55, CORAL, 1 - hb)
    lone = ease(seg(t, 1.6, 2.2))
    c.new_path(); c.move_to(800, 560); c.line_to(650, 1390); c.line_to(980, 1390); c.line_to(840, 560); c.close_path(); rgb(c, hx('FFE9A8'), 0.5 * lone); c.fill()
    bag(c, 815, 1390, 0.62, 'hero', f, col=CORAL, face='flat' if t > 1.6 else 'smile', eyes='dot', look=(-0.8, 0.5), sw=0.2 * math.sin(g * 3))
    sign(c, 800, 1040, "NOT THIS ONE", CORAL, WHITE, size=40, rot=-0.05, k=eback(seg(t, 2.3, 2.6)), padx=24)
    caption(c, t, 0.25, [[("99.5% OF BAGS", GOLD)], [("REUNITE RIGHT AWAY.", CREAM)]], y=300, size=84)
    strip(c, 1470, ["Source: Unclaimed Baggage."], seg(t, 1.0, 1.4), size=34)


def storeroom(c, f, g):
    bg(c, NIGHT2, NIGHT)
    for sy in (880, 1180):
        rrect(c, 500, sy, 520, 30, 8); fs(c, hx('3D4A78'), 8)
    for ux in (500, 990):
        rrect(c, ux, 700, 30, 780, 6); fs(c, hx('3D4A78'), 7)
    floor(c, 1480, hx('1B2540'), line=False)


def scene3(c, t, f, g):
    storeroom(c, f, g)
    p = ease(seg(t, 0.5, 3.3)); day = int(round(1 + 89 * p))
    for i, (x, col) in enumerate(((610, hx('5C6FA8')), (880, hx('4E8C8A')))):
        bag(c, x, 880, 0.42, ('ob', i), f, col=col, face='flat', eyes='closed')
    bag(c, 745, 1180, 0.66, 'hero', f, col=CORAL, face='flat', eyes='closed' if p > 0.6 else 'dot', look=(-0.6, 0.3), sw=0.1 * math.sin(g * 2))
    if p > 0.3:
        a = seg(p, 0.3, 0.9)
        for j in range(4):
            wline(c, [(520, 1180 - 250), (520 + 60 + 40 * j, 1180 - 250 + 110 - 14 * j)], ('cw', j), f, lw=3, col=WHITE, amp=0.5, a=0.6 * a)
        wline(c, [(580, 930 + 100), (640, 930 + 84), (680, 930 + 60), (700, 930 + 30)], 'cw5', f, lw=3, col=WHITE, amp=0.5, a=0.6 * a)
        for j in range(3):
            zk = (g * 0.5 + j * 0.33) % 1
            txt(c, "z", 850 + 30 * j + 20 * zk, 900 - 40 * j - 50 * zk, 44 + 10 * j, WHITE, HAND, a=(1 - zk) * a)
    # calendar
    c.save(); c.translate(250, 880); c.rotate(-0.04)
    for j in range(3):
        fl = (g * 2.6 + j * 0.33) % 1
        if 0 < p < 1:
            c.save(); c.translate(120 * fl, -160 * fl + 200 * fl * fl); c.rotate(1.6 * fl); rrect(c, -110, -40, 220, 150, 10); rgb(c, WHITE, 0.8 * (1 - fl)); c.fill(); c.restore()
    rrect(c, -150, -170, 300, 340, 24); fs(c, WHITE, 9)
    c.new_path(); c.move_to(-150, -90); c.line_to(-150, -146); c.curve_to(-150, -160, -140, -170, -126, -170); c.line_to(126, -170); c.curve_to(140, -170, 150, -160, 150, -146); c.line_to(150, -90); c.close_path(); fs(c, RED, 9)
    txt(c, "DAY", 0, -108, 54, WHITE); fit(c, str(day), 0, 110, 190, 250, INK)
    c.restore()
    sw = math.sin(g * 2.2)
    stick(c, 250, 1480 - 190, 1.0, 'wk', f, lh=(-60, -30), rh=(120 + 40 * sw, -170), face='flat', shirt=BLUE, hat='cap', look=(0.8 * sw, -0.3))
    mx, my = 250 + 120 + 40 * sw + 30, 1290 - 170 - 40
    c.new_path(); c.arc(mx + 20, my - 26, 44, 0, 2 * math.pi); rgb(c, GLASS, 0.5); c.fill_preserve(); rgb(c, INK); c.set_line_width(9); c.stroke()
    caption(c, t, 0.2, [[("AIRLINES SEARCH", CREAM)], [("UP TO 90 DAYS.", GOLD)]], y=300, size=84)
    strip(c, 1490, ["Before sale: tracing and claim settlement.", "Source: Unclaimed Baggage (2026)."], seg(t, 1.2, 1.6), size=32)


def scene4(c, t, f, g):
    bg(c, hx('FFD9A0'), hx('FFF1D6'))
    c.new_path(); c.arc(830, 720, 90, 0, 2 * math.pi); rgb(c, hx('FFF3B0')); c.fill()
    for i, (x, r) in enumerate(((150, 420), (620, 520), (1050, 400))):
        c.save(); c.translate(x - (g * 30) % 60, 1330); c.scale(1, 0.45); c.new_path(); c.arc(0, 0, r, math.pi, 2 * math.pi); c.restore(); rgb(c, (GRASS, GRASSD, GRASS)[i]); c.fill()
    c.rectangle(0, 1300, W, 190); rgb(c, IRON); c.fill()
    for i in range(8):
        dx = (i * 190 - (g * 520) % 190)
        c.rectangle(dx - 40, 1388, 100, 14); rgb(c, CREAM); c.fill()
    c.rectangle(0, 1490, W, 430); rgb(c, GRASSD); c.fill()
    sx = lerp(1400, 800, eout(seg(t, 1.5, 2.6)))
    wrect(c, sx - 10, 1010, 20, 300, 'post', f); fs(c, STEEL, 6)
    rrect(c, sx - 190, 800, 380, 220, 20); fs(c, hx('2E8B57'), 9)
    rrect(c, sx - 174, 816, 348, 188, 14); rgb(c, WHITE); c.set_line_width(5); c.stroke()
    fit(c, "SCOTTSBORO", sx, 900, 54, 310, WHITE); fit(c, "ALABAMA", sx, 972, 54, 310, GOLD)
    tx = lerp(-320, 400, eout(seg(t, 0.2, 1.5)))
    bob = 3 * math.sin(g * 14)
    bag(c, tx - 80, 1296 - 262 * 1.1 + bob + 6, 0.5, 'hero', f, col=CORAL, face='o' if t < 2.2 else 'smile', eyes='big' if t < 2.2 else 'dot', look=(0.8, 0), sw=0.5 + 0.2 * math.sin(g * 8))
    truck(c, tx, 1345, 1.1, f, g, col=BLUE, label=["LOST", "BAGS"], lsize=56)
    for i in range(3):
        pk = (g * 2 + i * 0.33) % 1
        c.new_path(); c.arc(tx - 290 - 90 * pk, 1300 - 30 * pk, 16 + 22 * pk, 0, 2 * math.pi); rgb(c, WHITE, 0.6 * (1 - pk)); c.fill()
    caption(c, t, 0.2, [[("THEN ONE STORE", CREAM)], [("BUYS UNCLAIMED BAGS.", GOLD)]], y=300, size=84)
    strip(c, 1590 - 110, ["Scottsboro, Alabama. Source: Unclaimed Baggage."], seg(t, 1.2, 1.6), size=32)


def arc_pos(p0, p1, u, h):
    return lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u) - h * math.sin(u * math.pi)


def scene5(c, t, f, g):
    bg(c, hx('D8F3EE'), hx('F4FFF9'))
    floor(c, 1400, hx('BFE0D8'))
    rrect(c, 60, 1230, 440, 40, 12); fs(c, WOOD, 9)
    for lx in (90, 440):
        wrect(c, lx, 1268, 30, 134, ('l5', lx), f); fs(c, WOODD, 7)
    # washing machine
    rrect(c, 590, 930, 330, 472, 30); fs(c, WHITE, 10)
    rrect(c, 612, 952, 286, 56, 12); fs(c, hx('DDE7F0'), 6)
    for i in range(3):
        c.new_path(); c.arc(650 + i * 46, 980, 13, 0, 2 * math.pi); fs(c, (CORAL, GOLD, GREEN)[i], 5)
    c.new_path(); c.arc(755, 1200, 122, 0, 2 * math.pi); fs(c, STEEL, 10)
    c.new_path(); c.arc(755, 1200, 96, 0, 2 * math.pi); fs(c, hx('8FD9FA'), 8)
    on = seg(t, 1.6, 2.0)
    for i in range(3):
        a0 = g * 7 * on + i * 2.09
        c.new_path(); c.arc(755, 1200, 60, a0, a0 + 1.2); rgb(c, WHITE); c.set_line_width(16); c.set_line_cap(1); c.stroke()
    if on > 0:
        for i in range(5):
            bk = (g * 0.9 + i * 0.2) % 1
            c.new_path(); c.arc(650 + i * 52 + 14 * math.sin(g * 3 + i), 920 - 240 * bk, 12 + 16 * bk, 0, 2 * math.pi); rgb(c, WHITE, 0.85 * (1 - bk)); c.fill_preserve(); rgb(c, hx('8FD9FA'), 1 - bk); c.set_line_width(4); c.stroke()
    # hero, opened
    op = ease(seg(t, 0.25, 0.7))
    c.save(); c.translate(160, 1230 - 250); c.rotate(-1.0 * op); rrect(c, -8, -18, 250, 36, 14); fs(c, hx('E0503F'), 8); c.restore()
    bag(c, 270, 1230, 0.84, 'hero', f, col=CORAL, face='o' if t < 2.4 else 'smile', eyes='big' if t < 2.4 else 'dot', look=(0.7, -0.5), tag=False, sq=1 - 0.03 * math.sin(g * 20) * (1 if t < 2.2 else 0))
    items = ((0.7, 'sock', PINK), (1.0, 'tee', TEAL), (1.3, 'sock', PINK), (1.6, 'tee', GOLD))
    for i, (t0, kind, col) in enumerate(items):
        u = seg(t, t0, t0 + 0.75)
        if 0 < u < 1:
            x, y = arc_pos((270, 960), (755, 1180), u, 330)
            (sock if kind == 'sock' else tee)(c, x, y, 0.8 * (1 - 0.5 * ein(u)), u * 5 + i, col)
    caption(c, t, 0.2, [[("OPEN, SORT, CLEAN.", CREAM)], [("GIVE ITEMS A NEW LIFE.", GOLD)]], y=300, size=70)
    strip(c, 1480, ["Items are resold, repurposed or recycled.", "Source: Unclaimed Baggage."], seg(t, 1.2, 1.6), size=34)


def scene6(c, t, f, g):
    bg(c, hx('FFE9C9'), hx('FFD3A0'))
    floor(c, 1420, WOOD)
    sign(c, 540, 640, "LOST LUGGAGE STORE", GOLD, INK, size=62, k=eback(seg(t, 0.1, 0.4)))
    sign(c, 540, 748, "SINCE 1970", CREAM, INK, size=36, k=eback(seg(t, 0.35, 0.6)), padx=22, lw=6)
    wline(c, [(90, 880), (760, 880)], 'rail', f, lw=12)
    for ux in (100, 750):
        wline(c, [(ux, 880), (ux, 1420)], ('up', ux), f, lw=12)
    for i, col in enumerate((TEAL, GOLD, PINK, GREEN, PURPLE)):
        x = 170 + i * 130; swg = 0.06 * math.sin(g * 3 + i)
        k = eback(seg(t, 0.4 + i * 0.12, 0.7 + i * 0.12))
        if k > 0.01:
            wline(c, [(x, 880), (x, 915)], ('hg', i), f, lw=6, amp=0.5)
            tee(c, x, 985, 0.86 * k, swg, col)
            c.save(); c.translate(x + 44, 1050); c.rotate(0.3 + swg); rrect(c, -18, 0, 36, 50, 6); fs(c, WHITE, 4); c.restore()
    sock(c, 250, 1300, 0.9, -0.2, PINK); sock(c, 330, 1310, 0.9, 0.15, PINK)
    bag(c, 560, 1420, 0.5, 'hb', f, col=hx('5C6FA8'), face='smile', tag=False)
    for i, (x0, x1, sh, t0) in enumerate(((1250, 860, PURPLE, 0.8), (-200, 180, ORANGE, 1.6))):
        w = ease(seg(t, t0, t0 + 1.2)); x = lerp(x0, x1, w); mv = 1 if 0 < w < 1 else 0
        d = -1 if x1 < x0 else 1
        stick(c, x, 1420 - 190, 1.0, ('sh', i), f, lh=(-50 if d > 0 else -110, -40 if d > 0 else -150), rh=(110 if d > 0 else 50, -150 if d > 0 else -40), face='grin', shirt=sh,
              lf=(-45 + 30 * math.sin(g * 9) * mv, 190), rf=(45 - 30 * math.sin(g * 9) * mv, 190), look=(-0.7 * d * -1, 0))
    caption(c, t, 0.2, [[("SOMEONE ELSE", CREAM)], [("BUYS WHAT WAS LEFT.", GOLD)]], y=300, size=82)
    strip(c, 1490, ["Source: Unclaimed Baggage."], seg(t, 1.2, 1.6), size=32)


def scene7(c, t, f, g):
    bg(c, hx('FF7A5A'), hx('FFC83D'))
    c.save(); c.translate(540, 1400); c.scale(1, 0.2); c.new_path(); c.arc(0, 0, 420, 0, 2 * math.pi); c.restore(); rgb(c, INK, 0.16); c.fill()
    hop = abs(math.sin(g * 5)) * 26
    stick(c, 300, 1400 - 190 - hop, 1.0, 'own', f, lh=(-90, -230), rh=(90, -230), face='grin', shirt=PURPLE, bob=2 * math.sin(g * 10))
    sock(c, 205, 1400 - 190 - hop - 300, 0.9, -0.2, PINK); sock(c, 395, 1400 - 190 - hop - 300, 0.9, 0.2, PINK)
    bag(c, 730, 1400, 0.8, 'hero', f, col=CORAL, face='grin' if t > 1.9 else 'smile', look=(-0.5, -0.2), sw=0.3 * math.sin(g * 6), rot=0.04 * math.sin(g * 5))
    sign(c, 730, 1020, "SOLD", GREEN, WHITE, size=64, rot=0.08, k=eback(seg(t, 0.5, 0.8)) * (1 - seg(t, 1.8, 1.95)))
    qmarks(c, ((860, 900, 0.3), (140, 820, -0.3), (560, 1010, 0.15)), t, 2.2)
    caption(c, t, 0.12, [[("YOUR SOCKS?", CREAM)], [("SOLD.", GOLD)]], y=300, size=92, t1=1.85)
    caption(c, t, 1.95, [[("EVER LOST A BAG", CREAM)], [("FOR GOOD?", GOLD)]], y=300, size=86)
    strip(c, 1500, ["Sources: Unclaimed Baggage,", "How It Works and 2026 Found Report."], seg(t, 2.3, 2.7), size=30)


SCENES = [(0.0, 3.6, scene1), (3.6, 8.0, scene2), (8.0, 12.4, scene3), (12.4, 16.8, scene4), (16.8, 21.2, scene5),
          (21.2, 25.6, scene6), (25.6, 30.0, scene7)]
draw = make_draw(SCENES)


# November 26 retention edit. Values: output seconds, source start, source end.
from edit import edited_draw
EDIT = [(2.4, 0, 3.6), (3.6, 3.6, 8), (4, 8, 12.4), (4, 12.4, 16.8), (4, 16.8, 21.2), (4, 21.2, 25.6), (3, 26.9, 29.9)]
DURATION = sum(shot[0] for shot in EDIT)
draw = edited_draw(SCENES, EDIT)
