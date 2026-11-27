from kit import *

DURATION = 24.0
RND = cairo.LINE_CAP_ROUND
PETC = hx('BFE6FF'); CAPC = hx('2F7FD8'); LABEL = hx('5BBF6A'); BINB = hx('2E6FD1'); BALE = hx('9FC9E8')
FLOORC = hx('C9CED8'); WALL = hx('E9EEF5'); BELTC = hx('3A3F4F')


def pbottle(c, x, y, s, key, f, face='smile', eyes='dot', rot=0.0, look=(0, 0), sq=1.0, tint=PETC):
    """hero PET bottle, x, y = centre, about 140 x 400"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * (2 - sq), s * sq)
    rrect(c, -30, -206, 60, 34, 8); fs(c, CAPC, 7)
    c.new_path(); c.move_to(-26, -172); c.curve_to(-30, -130, -70, -120, -70, -80); c.line_to(-70, 150); c.curve_to(-70, 180, 70, 180, 70, 150); c.line_to(70, -80); c.curve_to(70, -120, 30, -130, 26, -172); c.close_path()
    rgb(c, tint, 0.92); c.fill_preserve(); rgb(c, INK); c.set_line_width(9); c.stroke()
    c.rectangle(-70, -40, 140, 70); rgb(c, LABEL); c.fill()
    c.new_path(); c.move_to(-70, -40); c.line_to(70, -40); c.move_to(-70, 30); c.line_to(70, 30); rgb(c, INK); c.set_line_width(5); c.stroke()
    c.new_path(); c.move_to(-46, -100); c.line_to(-46, -54); rgb(c, WHITE, 0.6); c.set_line_width(10); c.set_line_cap(RND); c.stroke()
    facef(c, 0, 92, 52, face, look, eyes)
    c.restore()


def mini(c, x, y, s, rot=0.0, tint=PETC):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rrect(c, -9, -64, 18, 12, 3); fs(c, CAPC, 3)
    c.new_path(); c.move_to(-8, -52); c.curve_to(-9, -40, -20, -36, -20, -24); c.line_to(-20, 44); c.line_to(20, 44); c.line_to(20, -24); c.curve_to(20, -36, 9, -40, 8, -52); c.close_path()
    rgb(c, tint, 0.92); c.fill_preserve(); rgb(c, INK); c.set_line_width(4); c.stroke()
    c.rectangle(-20, -10, 40, 18); rgb(c, LABEL); c.fill()
    c.restore()


def rbin(c, x, y, s, lid=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.move_to(-170, -360); c.line_to(170, -360); c.line_to(145, 0); c.line_to(-145, 0); c.close_path(); fs(c, BINB, 10)
    for i in range(3):
        c.new_path(); c.move_to(-110 + i * 110, -320); c.line_to(-100 + i * 100, -40); rgb(c, INK, 0.2); c.set_line_width(8); c.stroke()
    c.save(); c.translate(-180, -360); c.rotate(-lid); rrect(c, 0, -34, 360, 40, 12); fs(c, hx('2459A8'), 10); c.restore()
    for k in range(3):
        a = k * 2 * math.pi / 3 - math.pi / 2
        c.new_path(); c.arc(60 * math.cos(a), -190 + 60 * math.sin(a), 22, 0, 2 * math.pi); rgb(c, WHITE, 0.85); c.fill()
    c.new_path(); c.arc(-130, 14, 34, 0, 2 * math.pi); fs(c, IRON, 8)
    c.restore()


def scene1(c, t, f, g):
    drop = 1.9
    k = ease(seg(t, 0.55, 1.35)); z = lerp(1.9, 1.0, k)
    c.save(); cam(c, z, lerp(560, 540, k), lerp(1010, 960, k))
    bg(c, hx('A9DDF5'), hx('EAF8FF'))
    c.rectangle(0, 1500, W, 420); fs(c, hx('B8BDC8'), 9)
    c.rectangle(0, 1320, W, 180); rgb(c, hx('7FC77A')); c.fill()
    rbin(c, 560, 1520, 1.0, lid=0.9 * (1 - ease(seg(t, drop + 0.1, drop + 0.4))))
    fall = ein(seg(t, 1.1, drop))
    if t < drop:
        by = lerp(960, 1200, fall)
        sweat(c, 540, by - 40, 1.0, g, f)
        pbottle(c, 540 + 3 * math.sin(g * 41), by, 0.9, 'hero', f, face='o', eyes='big', rot=0.2 * math.sin(g * 6) + 1.2 * fall, look=(0, 1))
    else:
        for i in range(6):
            q = (t - drop) / 0.4
            if q < 1:
                a = -math.pi + i * math.pi / 5
                wline(c, [(560 + 150 * math.cos(a), 1160 + 60 * math.sin(a)), (560 + (190 + 60 * q) * math.cos(a), 1160 + (80 + 50 * q) * math.sin(a))], ('dp', i), f, lw=8, col=WHITE, amp=0.5, a=1 - q)
    c.restore()
    caption(c, t, -1, [[("MOST RECYCLED PET", CREAM)], [("BECOMES NEW BOTTLES.", GOLD)]], y=300, size=86, pop=False)
    strip(c, 1680, ["US and Canada, 2025"], seg(t, 0.9, 1.3), size=40)


def rtruck(c, x, y, s, g):
    c.save(); c.translate(x, y); c.scale(s, s)
    bob = 3 * math.sin(g * 14)
    rrect(c, -330, -330 + bob, 430, 260, 20); fs(c, BINB, 9)
    for k in range(3):
        a = k * 2 * math.pi / 3 - math.pi / 2
        c.new_path(); c.arc(-115 + 46 * math.cos(a), -200 + bob + 46 * math.sin(a), 18, 0, 2 * math.pi); rgb(c, WHITE, 0.9); c.fill()
    rrect(c, 110, -250 + bob, 170, 180, 26); fs(c, CREAM, 9)
    rrect(c, 150, -226 + bob, 100, 70, 10); fs(c, GLASS, 6)
    for wx in (-220, 190):
        c.new_path(); c.arc(wx, -48, 52, 0, 2 * math.pi); fs(c, IRON, 9)
        c.new_path(); c.arc(wx, -48, 18, 0, 2 * math.pi); rgb(c, STEEL); c.fill()
    c.restore()


def plant(c, x, y, s, k=1.0):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    c.rectangle(-260, -380, 520, 380); fs(c, hx('D8DEE8'), 9)
    c.new_path(); c.move_to(-290, -380); c.line_to(0, -500); c.line_to(290, -380); c.close_path(); fs(c, hx('8C96A8'), 9)
    rrect(c, -110, -230, 220, 230, 10); fs(c, IRON, 8)
    for i in range(3):
        rrect(c, -220 + i * 170, -340, 100, 70, 8); fs(c, GLASS, 5)
    c.restore()


def scene2(c, t, f, g):
    bg(c, hx('A9DDF5'), hx('EAF8FF'))
    cloud(c, 260, 560, 1.0); cloud(c, 820, 660, 0.8)
    c.rectangle(0, 1400, W, 520); fs(c, hx('8C93A3'), 9)
    for i in range(6):
        c.rectangle(((i * 220 - g * 420) % (W + 300)) - 150, 1500, 120, 14); rgb(c, WHITE, 0.8); c.fill()
    plant(c, 860, 1400, 0.8, eback(seg(t, 1.6, 2.0)))
    tx = lerp(-300, 520, eout(seg(t, 0.2, 2.6)))
    rtruck(c, tx, 1420, 1.0, g)
    caption(c, t, 0.15, [[("A TRUCK TAKES IT", CREAM)], [("TO A SORTING CENTER.", GOLD)]], y=300, size=84)
    strip(c, 1700, ["Source: North Carolina DEQ, Recycling Loop."], seg(t, 1.0, 1.4), size=34)


def bale(c, x, y, s, k=1.0):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    rrect(c, -150, -260, 300, 260, 14); fs(c, BALE, 9)
    r = random.Random(3)
    for i in range(26):
        mini(c, r.uniform(-120, 120), r.uniform(-230, -30), 0.75, r.uniform(0, 6.28))
    for yy in (-190, -70):
        c.new_path(); c.move_to(-150, yy); c.line_to(150, yy); rgb(c, INK); c.set_line_width(7); c.stroke()
    c.restore()


def scene3(c, t, f, g):
    bg(c, WALL, hx('D5DCE6'))
    c.rectangle(0, 1460, W, 460); fs(c, FLOORC, 9)
    rrect(c, -40, 1080, 760, 60, 24); fs(c, BELTC, 8)
    for i in range(12):
        x = ((i * 70 + g * 260) % 760) - 40
        c.rectangle(x, 1090, 8, 40); rgb(c, hx('5A6070')); c.fill()
    sh = 1 if t < 2.2 else 0
    for i in range(6):
        x = ((i * 130 + g * 260) % 700) - 20
        if x < 640:
            col = (PETC, hx('F4E1B0'), PETC, hx('D7E9C9'), PETC, hx('F2C4C4'))[i]
            mini(c, x, 1036, 0.9, 0.0, col)
    c.rectangle(560, 860, 140, 160); fs(c, STEEL, 8)
    c.new_path(); c.arc(630, 940, 30, 0, 2 * math.pi); fs(c, GOLD if (g * 4) % 1 < 0.5 else CORAL, 6)
    prs = ease(seg(t, 1.6, 2.4))
    c.rectangle(760, 700 + 260 * prs, 280, 40); fs(c, IRON, 8)
    c.rectangle(890, 480, 24, 220 + 260 * prs); fs(c, STEELD, 6)
    if t < 2.2:
        hx_ = lerp(640, 900, ease(seg(t, 0.2, 1.4))); hy_ = lerp(1000, 1230, ease(seg(t, 0.2, 1.4)))
        pbottle(c, hx_, hy_, 0.55, 'hero', f, face='o', eyes='big', rot=0.3 * math.sin(g * 5), look=(1, 0.5), sq=1.0 - 0.35 * prs)
    else:
        bale(c, 900, 1460, 1.0, eback(seg(t, 2.2, 2.6)))
        pbottle(c, 860, 1300, 0.25, 'hero', f, face='flat', eyes='dot', rot=0.6)
    caption(c, t, 0.15, [[("MACHINES SORT THE PET", CREAM)], [("AND PRESS IT INTO BALES.", GOLD)]], y=300, size=76)
    strip(c, 1700, ["Source: North Carolina DEQ, Recycling Loop."], seg(t, 0.9, 1.3), size=34)


def flakes(c, x0, x1, y0, y1, g, n=60, seed=7, k=1.0):
    r = random.Random(seed)
    for i in range(int(n * k)):
        x = r.uniform(x0, x1); y = r.uniform(y0, y1); a = r.uniform(0, 6.28) + g * r.uniform(-1, 1)
        c.save(); c.translate(x, y); c.rotate(a)
        c.new_path(); c.move_to(-14, -8); c.line_to(12, -12); c.line_to(16, 8); c.line_to(-10, 12); c.close_path(); rgb(c, (PETC, hx('A8D8F6'), WHITE)[i % 3]); c.fill_preserve(); rgb(c, INK, 0.6); c.set_line_width(2.5); c.stroke()
        c.restore()


def scene4(c, t, f, g):
    bg(c, WALL, hx('D5DCE6'))
    c.rectangle(0, 1460, W, 460); fs(c, FLOORC, 9)
    c.new_path(); c.move_to(300, 760); c.line_to(780, 760); c.line_to(680, 1080); c.line_to(400, 1080); c.close_path(); fs(c, STEEL, 9)
    for i in range(5):
        a = g * 9 + i * 1.2
        c.new_path(); c.arc(440 + i * 50, 1040, 26, a, a + 4.5); rgb(c, INK); c.set_line_width(7); c.stroke()
    c.rectangle(400, 1080, 280, 60); fs(c, STEELD, 8)
    dk = ease(seg(t, 0.1, 0.9))
    if dk < 1:
        bale(c, 540, lerp(700, 960, dk), 0.6 * (1 - 0.6 * dk))
    for i in range(4):
        ph = (g * 1.2 + i / 4) % 1
        c.new_path(); c.arc(300 + 500 * ph, 840 - 80 * math.sin(ph * 3 + i), 18 + 10 * ph, 0, 2 * math.pi); rgb(c, hx('8FD9FA'), 0.5 * (1 - ph)); c.fill()
    pk = ease(seg(t, 0.8, 2.4))
    c.new_path(); c.move_to(360, 1460); c.line_to(720, 1460); c.line_to(680, 1460 - 180 * pk); c.line_to(400, 1460 - 180 * pk); c.close_path(); rgb(c, hx('A8D8F6'), 0.6); c.fill()
    flakes(c, 380, 700, 1460 - 180 * pk, 1450, g * 0.1, 70, 3, pk)
    for i in range(8):
        ph = (g * 1.6 + i / 8) % 1
        if pk > 0.05:
            c.save(); c.translate(440 + (i * 37) % 200, 1140 + 300 * ph); c.rotate(ph * 6)
            c.new_path(); c.move_to(-12, -7); c.line_to(10, -10); c.line_to(13, 7); c.line_to(-8, 10); c.close_path(); rgb(c, PETC); c.fill_preserve(); rgb(c, INK, 0.6); c.set_line_width(2.5); c.stroke(); c.restore()
    caption(c, t, 0.15, [[("THEN IT IS WASHED", CREAM)], [("AND CHOPPED INTO FLAKES.", GOLD)]], y=300, size=78)
    strip(c, 1700, ["Source: North Carolina DEQ, Recycling Loop."], seg(t, 0.9, 1.3), size=34)


def scene5(c, t, f, g):
    bg(c, hx('FFF3D6'), hx('FFE1A8'))
    c.rectangle(0, 1460, W, 460); fs(c, hx('D9B98A'), 9)
    rrect(c, -40, 1360, 1160, 50, 20); fs(c, BELTC, 8)
    for i in range(7):
        x = ((i * 170 + g * 200) % (W + 200)) - 100
        mini(c, x, 1300, 1.0, 0.0)
    hop = abs(math.sin(g * 6)) * 24
    pbottle(c, 540, 1150 - hop, 0.75, 'hero', f, face='grin', eyes='dot', look=(0, -0.3), rot=0.05 * math.sin(g * 6))
    v = 69 * eout(seg(t, 0.6, 2.6))
    panel(c, 540, 690, 420, 170, "{}%".format(int(round(v))), 110, eback(seg(t, 0.4, 0.75)))
    caption(c, t, 0.15, [[("69% OF IT BECAME", CREAM)], [("NEW BOTTLES.", GOLD)]], y=300, size=90)
    strip(c, 1700, ["PET recycled in the US and Canada, 2025. A record share.", "Source: NAPCOR 2025 PET Recycling Report."], seg(t, 1.0, 1.4), size=30)


def scene6(c, t, f, g):
    bg(c, hx('2B2F4A'), hx('3D4366'))
    lit = int(round(29 * eout(seg(t, 0.7, 2.4))))
    for i in range(100):
        r_, c_ = i // 10, i % 10
        x = 150 + c_ * 87; y = 640 + r_ * 92
        on = i < lit
        mini(c, x, y, 0.62, 0.0, PETC if on else hx('59607A'))
        if on and i == lit - 1 and lit < 29:
            sparkle(c, x + 24, y - 40, 22, GOLD, 1)
    caption(c, t, 0.15, [[("BUT ONLY 29% OF US PET", CREAM)], [("BOTTLES GOT COLLECTED.", GOLD)]], y=300, size=78)
    strip(c, 1700, ["By weight: 1,821 of 6,286 million pounds, 2025.", "Source: NAPCOR 2025 PET Recycling Report."], seg(t, 1.0, 1.4), size=30)


def scene7(c, t, f, g):
    bg(c, hx('FF7A5A'), hx('FFC83D'))
    hop = abs(math.sin(g * 5)) * 30
    rbin(c, 540, 1520, 0.9, lid=0.4)
    pbottle(c, 540, 1000 - hop, 1.0, 'hero', f, face='grin', look=(0, -0.3), rot=0.05 * math.sin(g * 5))
    qmarks(c, ((200, 760, -0.3), (880, 800, 0.3), (180, 1300, 0.2)), t, 0.6)
    caption(c, t, 0.1, [[("DO YOU", CREAM)], [("RECYCLE YOURS?", GOLD)]], y=300, size=100)


SCENES = [(0.0, 3.0, scene1), (3.0, 6.8, scene2), (6.8, 10.4, scene3), (10.4, 13.6, scene4), (13.6, 17.8, scene5), (17.8, 21.4, scene6), (21.4, 24.0, scene7)]
draw = make_draw(SCENES)
