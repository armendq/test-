from lib import *

NIGHT = hx('1B2540'); NIGHT2 = hx('26304F'); STEEL = hx('8FA3B8'); STEELD = hx('5F728A'); BELT = hx('2B2F3A')
PURPLE = hx('9B7BEA'); SANSF = "DM Sans"
_r = random.Random(11)
BARS = [(_r.choice((5, 8, 12, 16)), _r.choice((5, 7, 10))) for _ in range(30)]


def bag(c, x, y, s, key, f, col=CORAL, face='smile', eyes='dot', rot=0.0, look=(0, 0), tag=True, sq=1.0, sw=0.0, sticker=None):
    """x, y = bottom centre"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    wline(c, [(-52, -296), (-52, -356), (52, -356), (52, -296)], (key, 'h'), f, lw=15)
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * 72, -16, 24, 0, 2 * math.pi); fs(c, hx('3A3F4F'), 8)
    rrect(c, -118, -302, 236, 282, 40); fs(c, col, 11)
    for xx in (-66, 66):
        wline(c, [(xx, -284), (xx, -40)], (key, 'r', xx), f, lw=7, col=INK, amp=0.8, a=0.22)
    facef(c, 0, -168 - (24 if sticker else 0), 98, face, look, eyes)
    if sticker:
        rrect(c, -96, -104, 192, 66, 16); fs(c, GOLD, 7); txt(c, sticker, 0, -52, 50, INK)
    if tag:
        c.save(); c.translate(52, -340); c.rotate(0.5 + sw)
        wline(c, [(0, 0), (0, 44)], (key, 'ts'), f, lw=5, amp=0.5)
        rrect(c, -24, 44, 48, 74, 9); fs(c, WHITE, 6)
        for k in range(4):
            c.rectangle(-14, 58 + k * 12, 28, 5 if k % 2 else 7); rgb(c, INK); c.fill()
        c.restore()
    c.restore()


def belt(c, x0, x1, y, g, f, sp=320, key='belt', legs=True, floor=1700):
    if legs:
        for k, xx in enumerate(range(int(x0) + 60, int(x1), 260)):
            wline(c, [(xx, y + 40), (xx, floor)], (key, 'lg', k), f, lw=14, col=STEELD, amp=0.8)
    rrect(c, x0, y, x1 - x0, 50, 25); fs(c, BELT, 9)
    n = int((x1 - x0) / 90) + 2
    for k in range(n):
        xx = x0 + ((k * 90 + g * sp) % (x1 - x0))
        if x0 + 20 < xx < x1 - 20:
            c.new_path(); c.arc(xx, y + 25, 9, 0, 2 * math.pi); rgb(c, STEEL); c.fill()


def flaps(c, x, y, w, h, g, f, push=0.0, key='fl', n=6):
    for k in range(n):
        xx = x + (k + 0.5) * w / n
        a = math.sin(g * 5 + k * 1.7) * 0.02 + push * (0.25 + 0.1 * math.sin(k * 2.1))
        c.save(); c.translate(xx, y); c.rotate(a); rrect(c, -w / n / 2 + 2, 0, w / n - 4, h, 8); fs(c, hx('3A3F4F'), 5); c.restore()


def boh(c, f, g, speed=0.0):
    bg(c, NIGHT, NIGHT2)
    for i in range(7):
        x = ((i * 230 - g * 110 * speed) % 1500) - 180
        c.rectangle(x, 520, 64, 1400); rgb(c, hx('222D50')); c.fill()
    for y in (540, 596):
        c.rectangle(-20, y, W + 40, 20); rgb(c, hx('34416B')); c.fill()
    for i in range(5):
        x = ((i * 300 - g * 160 * speed) % 1500) - 150
        gl = cairo.RadialGradient(x, 640, 8, x, 640, 190)
        gl.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.30); gl.add_color_stop_rgba(1, 1, 0.9, 0.6, 0)
        c.set_source(gl); c.rectangle(x - 200, 600, 400, 300); c.fill()
        c.new_path(); c.arc(x, 632, 16, 0, 2 * math.pi); rgb(c, hx('FFE9A8')); c.fill()
    c.rectangle(0, 1700, W, H - 1700); rgb(c, hx('141C33')); c.fill()


def hall(c, f, g):
    bg(c, hx('CFE6F5'), hx('EEF6FB'))
    rrect(c, 70, 560, 760, 420, 30); fs(c, hx('9FDCF5'), 9)
    c.save(); rrect(c, 76, 566, 748, 408, 26); c.clip()
    wcirc(c, 360 + math.sin(g * 0.4) * 6, 850, 330, 'plane', f, amp=2, ry=80); fs(c, WHITE, 8)
    wpoly(c, [(560, 800), (660, 640), (706, 640), (672, 840)], 'tail', f); fs(c, CORAL, 8)
    for k in range(6):
        c.new_path(); c.arc(150 + k * 62, 838, 13, 0, 2 * math.pi); rgb(c, hx('4C8DF6')); c.fill()
    c.rectangle(70, 920, 760, 60); rgb(c, hx('B9C7D6')); c.fill()
    c.restore()
    for x in (320, 580):
        wline(c, [(x, 562), (x, 978)], ('mul', x), f, lw=8, amp=0.8)
    c.rectangle(0, 1420, W, H - 1420); c.set_source(grad(0, 1420, 0, H, [(0, hx('C4D2E0')), (1, hx('A9BBCD'))])); c.fill()
    wline(c, [(0, 1420), (W, 1420)], 'fl', f, lw=7, amp=0.8)


# ------------------------------------------------------------------ scene 1: check-in
def s1_bag_x(t): return lerp(470, 1130, ease(seg(t, 1.25, 3.0)))


def scene1(c, t, f, g):
    bx = s1_bag_x(t)
    k = ease(seg(t, 0.35, 1.3)); z = lerp(2.3, 1.0, k); fx, fy = lerp(bx + 20, 540, k), lerp(1130, 960, k)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)
    hall(c, f, g)
    stick(c, 200, 1230, 1.0, 'trav', f, lh=(-60, -20), rh=(96 + 16 * math.sin(g * 9), -300), face='smile', eyes='closed',
          shirt=TEAL, bob=math.sin(g * 3) * 2)
    rrect(c, 320, 1100, 200, 250, 18); fs(c, hx('4C8DF6'), 9)
    rrect(c, 300, 1076, 240, 40, 14); fs(c, hx('2F6BD8'), 8)
    belt(c, 360, 1140, 1300, g, f, sp=330 if t > 1.2 else 0, floor=1420)
    push = math.sin(seg(bx, 800, 1090) * math.pi)
    moving = t > 1.25
    bag(c, bx, 1300, 0.9, 'hero', f, face='o' if moving else 'smile', eyes='big' if moving else 'dot',
        look=(1, 0) if moving else (-1, -0.3), sw=math.sin(g * 8) * 0.15 if moving else 0, rot=0.03 * math.sin(g * 14) if moving else 0)
    rrect(c, 830, 760, 330, 700, 20); fs(c, STEEL, 9)
    rrect(c, 860, 950, 200, 356, 16); rgb(c, hx('10172B')); c.fill()
    flaps(c, 860, 950, 200, 350, g, f, push)
    rrect(c, 860, 950, 200, 356, 16); rgb(c, INK); c.set_line_width(9); c.stroke()
    rrect(c, 862, 820, 196, 90, 16); fs(c, GOLD, 7); txt(c, "BAGS", 960, 884, 54, INK)
    c.restore()
    caption(c, t, -1, [[("WHERE DOES", CREAM)], [("YOUR SUITCASE GO?", GOLD)]], y=300, size=92, pop=False)
    w = ein(seg(t, 2.85, 3.2))
    if w > 0:
        c.new_path(); c.arc(960, 1150, 2300 * w, 0, 2 * math.pi); rgb(c, NIGHT); c.fill()


# ------------------------------------------------------------------ scene 2: the tag
def tag_card(c, x, y, k, f, ok):
    c.save(); c.translate(x, y); c.scale(k, k); c.rotate(-0.05)
    rrect(c, -272, -142, 560, 300, 30); rgb(c, INK, 0.35); c.fill()
    rrect(c, -280, -150, 560, 300, 30); fs(c, WHITE, 9)
    c.new_path(); c.arc(-236, 0, 16, 0, 2 * math.pi); fs(c, NIGHT, 6)
    txt(c, "TOKYO", 20, -52, 92, INK)
    x0 = -190
    for (bw, gp) in BARS:
        if x0 + bw > 232: break
        c.rectangle(x0, -20, bw, 100); rgb(c, INK); c.fill(); x0 += bw + gp
    txt(c, "0749 331 062", 20, 126, 36, INK, HAND)
    if ok > 0:
        c.save(); c.translate(268, -140); c.scale(ok, ok)
        c.new_path(); c.arc(0, 0, 58, 0, 2 * math.pi); fs(c, GREEN, 8)
        wline(c, [(-26, 2), (-8, 22), (28, -20)], 'tick', f, lw=14, col=WHITE, amp=0.5); c.restore()
    c.restore()


def scene2(c, t, f, g):
    boh(c, f, g)
    c.save(); c.translate(540, 1350); c.scale(1.25, 1.25); c.translate(-540, -1300)
    if t < 2.4: bx = lerp(-170, 540, eout(seg(t, 0.0, 1.2)))
    else: bx = lerp(540, 1290, ein(seg(t, 2.4, 4.1)))
    scan = 1.15 < t < 2.3
    for px in (400, 680):
        wline(c, [(px, 880), (px, 1300)], ('post', px), f, lw=22, col=STEELD, amp=0.8)
    belt(c, -40, W + 40, 1300, g, f, sp=0 if 1.2 < t < 2.4 else 520)
    bag(c, bx, 1300, 0.95, 'hero', f, face='flat' if scan else 'smile', eyes='big' if scan else 'dot', look=(0, -1) if scan else (1, 0),
        sw=math.sin(g * 7) * 0.12)
    if scan:
        for k in range(5):
            xx = bx - 120 + ((g * 520 + k * 60) % 240)
            c.new_path(); c.move_to(540, 880); c.line_to(xx, 1290); rgb(c, hx('FF4D4D'), 0.55); c.set_line_width(5); c.stroke()
        c.new_path(); c.move_to(540, 880); c.line_to(bx - 130, 1295); c.line_to(bx + 130, 1295); c.close_path(); rgb(c, hx('FF4D4D'), 0.12); c.fill()
    rrect(c, 370, 800, 340, 96, 20); fs(c, GOLD, 9)
    for k in range(5):
        c.new_path(); c.move_to(400 + k * 64, 890); c.line_to(440 + k * 64, 806); c.line_to(464 + k * 64, 806); c.line_to(424 + k * 64, 890)
        c.close_path(); rgb(c, INK, 0.85); c.fill()
    lamp = scan and int(g * 10) % 2 == 0
    c.new_path(); c.arc(540, 782, 24, 0, 2 * math.pi); fs(c, hx('FF4D4D') if lamp else hx('7A2A2A'), 7)
    c.restore()
    kc = eback(seg(t, 1.45, 1.75)) * (1 - ein(seg(t, 3.5, 3.75)))
    if kc > 0.01: tag_card(c, 540, 650, kc * 0.92, f, eback(seg(t, 2.05, 2.3)))
    caption(c, t, 0.25, [[("A BARCODE TAG", CREAM)], [("IS ITS ONLY ID.", GOLD)]], y=300, size=88)


# ------------------------------------------------------------------ scene 3: x-ray
def xray_items(c, f, lim):
    c.save(); c.rectangle(0, 0, lim, H); c.clip()
    rrect(c, 388, 610, 230, 250, 34); rgb(c, hx('6FE7FF'), 0.9); c.set_line_width(7); c.stroke()
    wline(c, [(455, 610), (455, 566), (551, 566), (551, 610)], 'xh', f, lw=7, col=hx('6FE7FF'), amp=0.4)
    c.new_path(); c.arc(470, 770, 40, 0, 2 * math.pi); rgb(c, hx('FF9A3D')); c.fill()
    c.new_path(); c.arc(508, 722, 26, 0, 2 * math.pi); rgb(c, hx('FF9A3D')); c.fill()
    c.new_path(); c.move_to(528, 716); c.line_to(560, 724); c.line_to(528, 736); c.close_path(); rgb(c, hx('FFD23D')); c.fill()
    c.new_path(); c.arc(514, 716, 5, 0, 2 * math.pi); rgb(c, NIGHT); c.fill()
    wline(c, [(420, 640), (420, 700), (452, 700)], 'sock', f, lw=26, col=hx('5BE38A'), amp=0.4)
    wline(c, [(560, 800), (596, 660)], 'tb', f, lw=9, col=hx('5AA8FF'), amp=0.4)
    wline(c, [(590, 684), (598, 652)], 'tb2', f, lw=20, col=hx('5AA8FF'), amp=0.4)
    c.restore()


def scene3(c, t, f, g):
    boh(c, f, g)
    c.save(); c.translate(0, 70)
    if t < 1.1: bx = lerp(-170, 410, eout(seg(t, 0.0, 1.1)))
    elif t < 3.1: bx = lerp(410, 700, seg(t, 1.1, 3.1))
    else: bx = lerp(700, 1300, ein(seg(t, 3.1, 4.7)))
    belt(c, -40, W + 40, 1300, g, f, sp=420)
    bag(c, bx, 1300, 0.9, 'hero', f, face='smile' if t > 3.1 else 'flat', eyes='closed' if t > 3.3 else 'dot', look=(1, 0),
        sw=math.sin(g * 7) * 0.1)
    rrect(c, 300, 960, 500, 350, 30); fs(c, STEEL, 10)
    rrect(c, 330, 990, 440, 90, 18); fs(c, STEELD, 7); txt(c, "X-RAY", 550, 1056, 58, CREAM)
    flaps(c, 300, 1090, 60, 214, g, f, math.sin(seg(bx, 240, 420) * math.pi), key='fa', n=2)
    flaps(c, 740, 1090, 60, 214, g, f, math.sin(seg(bx, 690, 880) * math.pi), key='fb', n=2)
    # monitor
    wline(c, [(505, 880), (505, 962)], 'mst', f, lw=18, col=STEELD, amp=0.6)
    rrect(c, 228, 548, 554, 340, 30); fs(c, hx('3A3F4F'), 10)
    rrect(c, 252, 572, 506, 292, 18); rgb(c, hx('0B1430')); c.fill()
    sw = seg(t, 1.2, 2.3)
    if sw > 0:
        c.save(); rrect(c, 252, 572, 506, 292, 18); c.clip()
        lim = 252 + 506 * sw
        xray_items(c, f, lim)
        if sw < 1:
            c.rectangle(lim - 5, 572, 10, 292); rgb(c, hx('B8F4FF'), 0.9); c.fill()
        for yy in range(580, 864, 12):
            c.rectangle(252, yy, 506, 2); rgb(c, WHITE, 0.05); c.fill()
        c.restore()
    okk = eback(seg(t, 2.9, 3.15))
    if okk > 0:
        c.save(); c.translate(752, 580); c.scale(okk, okk); c.new_path(); c.arc(0, 0, 54, 0, 2 * math.pi); fs(c, GREEN, 8)
        wline(c, [(-24, 2), (-7, 20), (26, -18)], 'tick3', f, lw=13, col=WHITE, amp=0.5); c.restore()
    surprised = 2.0 < t < 2.9
    stick(c, 950, 1250, 0.92, 'off', f, lh=(-120, -250) if t > 1.4 else (-50, -20), rh=(56, -30), face='o' if surprised else ('smile' if t >= 2.9 else 'flat'),
          eyes='big' if surprised else 'dot', shirt=BLUE, look=(-1, -0.6), hat='cap', bob=math.sin(g * 3) * 2,
          lf=(-45, 190), rf=(45, 190))
    c.restore()
    caption(c, t, 0.25, [[("EVERY BAG", CREAM)], [("GETS X-RAYED.", GOLD)]], y=300, size=92)


# ------------------------------------------------------------------ scene 4: the ride
def ty(xw): return 1270 + 62 * math.sin(xw / 250.0) + 30 * math.sin(xw / 93.0 + 1.3)


def cart(c, x, y, rot, s, key, f, col, face, eyes, g, hero=False):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    bag(c, 0, -52, 0.82, key, f, col=col, face=face, eyes=eyes, look=(1, 0), sw=-0.5 + math.sin(g * 16) * 0.12, rot=-0.05)
    rrect(c, -170, -120, 340, 100, 26); fs(c, GOLD, 10)
    for k in range(3):
        c.new_path(); c.move_to(-120 + k * 90, -26); c.line_to(-80 + k * 90, -114); c.line_to(-52 + k * 90, -114); c.line_to(-92 + k * 90, -26)
        c.close_path(); rgb(c, INK, 0.8); c.fill()
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * 110, -4, 28, 0, 2 * math.pi); fs(c, hx('3A3F4F'), 8)
        c.new_path(); c.arc(sg * 110, -4, 9, 0, 2 * math.pi); rgb(c, STEEL); c.fill()
    c.restore()


def scene4(c, t, f, g):
    boh(c, f, g, speed=2.2)
    off = g * 980
    # far track with small carts going the other way
    c.rectangle(-20, 905, W + 40, 16); rgb(c, hx('34416B')); c.fill()
    for k in range(3):
        xx = W + 200 - ((g * 420 + k * 520) % 1560)
        rrect(c, xx - 60, 862, 120, 44, 12); rgb(c, hx('3F4D7A')); c.fill()
        rrect(c, xx - 36, 800, 72, 66, 14); rgb(c, hx('4A5890')); c.fill()
    # streaks
    for k in range(9):
        xx = W + 300 - ((g * 1500 + k * 173) % 1700); yy = 700 + (k * 97) % 420
        c.rectangle(xx, yy, 150 + (k % 3) * 60, 7); rgb(c, WHITE, 0.16); c.fill()
    # supports and track
    for k in range(8):
        xx = (k * 250 - off) % 2000 - 200
        wline(c, [(xx, ty(xx + off) + 20), (xx, 1700)], ('sup', k), f, lw=18, col=STEELD, amp=0.5)
    pts = [(x, ty(x + off) + 26) for x in range(-40, W + 80, 36)]
    wline(c, pts, 'trk', f, lw=26, col=INK, amp=0.5)
    wline(c, [(x, y - 4) for x, y in pts], 'trk2', f, lw=10, col=STEEL, amp=0.4)
    def place(xs):
        y0 = ty(xs + off); sl = (ty(xs + 30 + off) - ty(xs - 30 + off)) / 60.0
        return y0, math.atan(sl)
    for xs, col, key in ((-60 + 40 * math.sin(g), TEAL, 'c2'), (1010 + 30 * math.sin(g * 1.3), GREEN, 'c3')):
        y0, r0 = place(xs); cart(c, xs, y0 + 22, r0, 0.62, key, f, col, 'smile', 'closed', g)
    xs = 500 + 26 * math.sin(g * 1.7); y0, r0 = place(xs)
    for k in range(4):
        yy = y0 - 80 - k * 62 + math.sin(g * 9 + k) * 6
        ln = 150 + (k % 2) * 80
        wline(c, [(xs - 250 - ln, yy), (xs - 250, yy)], ('spl', k), f, lw=9, col=WHITE, amp=1.0, a=0.85)
    cart(c, xs, y0 + 22, r0, 1.0, 'hero', f, CORAL, 'o' if t < 1.6 else 'grin', 'big' if t < 1.6 else 'dot', g, hero=True)
    # panel
    if t > 1.95:
        kp = eback(seg(t, 1.95, 2.2))
        c.save(); c.translate(540, 1500); c.scale(kp, kp)
        rrect(c, -302, -72, 620, 150, 30); rgb(c, CORAL); c.fill()
        rrect(c, -310, -80, 620, 150, 30); fs(c, INK, 6)
        if t < 3.85:
            n = int(round(lerp(0, 18, ease(seg(t, 2.1, 3.3)))))
            txt(c, "BELTS", -274, 14, 46, CREAM, CAP, anchor='l'); txt(c, f"{n} KM", 280, 24, 84, GOLD, CAP, anchor='r')
        else:
            v = int(round(lerp(0, 40, ease(seg(t, 3.95, 5.0)))))
            txt(c, "SPEED", -274, 14, 46, CREAM, CAP, anchor='l'); txt(c, f"{v} KM/H", 280, 22, 76, GOLD, CAP, anchor='r')
        c.restore()
    caption(c, t, 0.2, [[("AT HEATHROW", CREAM)], [("TERMINAL 5:", CREAM)]], y=300, size=88, t1=2.0)
    caption(c, t, 2.05, [[("18 KM", GOLD), (" OF BELTS.", CREAM)]], y=330, size=96, t1=3.85)
    caption(c, t, 3.9, [[("CARTS HIT", CREAM)], [("40 KM/H.", GOLD)]], y=300, size=92)


# ------------------------------------------------------------------ scene 5: sorting
CH = [(230, "TOKYO", GOLD), (540, "ROME", TEAL), (850, "LIMA", PINK)]


def bin_back(c, f, x, label, col):
    wpoly(c, [(x - 70, 950), (x + 70, 950), (x + 110, 1270), (x - 110, 1270)], ('ch', x), f); fs(c, STEELD, 8)
    rrect(c, x - 150, 1270, 300, 250, 22); fs(c, hx('3A4670'), 9)


def bin_front(c, f, x, label, col):
    rrect(c, x - 150, 1370, 300, 190, 22); fs(c, hx('4A5890'), 9)
    rrect(c, x - 120, 1420, 240, 84, 16); fs(c, col, 7); txt(c, label, x, 1482, 54, INK)


def drop(t, t0, x):
    """returns (x, y, rot) for a bag tipping at time t0 over chute x"""
    u = seg(t, t0, t0 + 0.75)
    return x + 10 * math.sin(u * math.pi), lerp(900, 1500, ein(u) * 0.55 + u * 0.45), 0.5 * math.sin(u * math.pi)


def scene5(c, t, f, g):
    boh(c, f, g)
    c.save(); c.translate(0, 30)
    for (x, lab, col) in CH: bin_back(c, f, x, lab, col)
    belt(c, -40, W + 40, 900, g, f, sp=340, legs=False)
    v = 340
    hx_ = -120 + v * t; t_h = (230 + 120) / v
    px = -400 + v * t; t_p = (850 + 400) / v
    items = [(540, 1500, 0.12, GREEN, 'smile', 'closed', 'gb', None)]
    if t < t_h: items.append((hx_, 900, 0, CORAL, 'smile', 'dot', 'hero', 'TOKYO'))
    else:
        x, y, r = drop(t, t_h, 230); items.append((x, y, r, CORAL, 'grin', 'closed' if t > t_h + 0.75 else 'dot', 'hero', 'TOKYO'))
    worried = px > 330
    if t < t_p: items.append((px, 900, 0.04 * math.sin(g * 12) if worried else 0, PURPLE, 'flat' if worried else 'smile',
                              'big' if worried else 'dot', 'pb', 'TOKYO'))
    else:
        x, y, r = drop(t, t_p, 850); items.append((x, y, r, PURPLE, 'o', 'big', 'pb', 'TOKYO'))
    for (x, y, r, col, face, eyes, key, st) in items:
        bag(c, x, y, 0.8, key, f, col=col, face=face, eyes=eyes, rot=r, look=(1, 0.3), sw=math.sin(g * 7) * 0.1, sticker=st)
    for (x, lab, col) in CH: bin_front(c, f, x, lab, col)
    if t > t_h + 0.7:
        k = eback(seg(t, t_h + 0.7, t_h + 0.95))
        c.save(); c.translate(348, 1250); c.scale(k, k); c.new_path(); c.arc(0, 0, 50, 0, 2 * math.pi); fs(c, GREEN, 8)
        wline(c, [(-22, 2), (-6, 19), (24, -17)], 'tk5', f, lw=13, col=WHITE, amp=0.5); c.restore()
    if t > t_p + 0.45:
        k = eback(seg(t, t_p + 0.45, t_p + 0.7))
        c.save(); c.translate(968, 1250); c.scale(k, k); c.new_path(); c.arc(0, 0, 54, 0, 2 * math.pi); fs(c, hx('FF4D4D'), 8)
        txt(c, "!", 0, 30, 80, WHITE); c.restore()
    c.restore()
    caption(c, t, 0.2, [[("PER 1,000", CREAM)], [("PASSENGERS...", CREAM)]], y=300, size=92, t1=2.25)
    caption(c, t, 2.3, [[("ABOUT 5 BAGS", GOLD)], [("GO ASTRAY.", CREAM)]], y=300, size=92)
    k = eout(seg(t, 2.9, 3.2))
    if k > 0:
        c.save(); c.translate(540, 560)
        rrect(c, -290, -38, 580, 72, 24); rgb(c, INK, 0.88 * k); c.fill()
        txt(c, "Most are late, not lost.", 0, 12, 40, CREAM, HAND, a=k)
        rrect(c, -372, 40, 744, 54, 20); rgb(c, INK, 0.88 * k); c.fill()
        txt(c, "Sources: SITA 2026 report, Airport Technology.", 0, 77, 29, CREAM, HAND, a=k)
        c.restore()


# ------------------------------------------------------------------ scenes 6 and 7: baggage claim
def carousel(c, f, g, cx=540, cy=1330):
    wcirc(c, cx, cy, 450, 'car', f, amp=3, k=18, ry=170); fs(c, hx('3A3F4F'), 10)
    for k in range(14):
        a = 2 * math.pi * k / 14 + g * 0.5
        c.new_path(); c.arc(cx + 385 * math.cos(a), cy + 138 * math.sin(a), 7, 0, 2 * math.pi); rgb(c, STEEL); c.fill()
    wcirc(c, cx, cy - 16, 318, 'isl', f, amp=3, k=18, ry=96); fs(c, STEEL, 9)


def on_car(a, cx=540, cy=1330): return cx + 385 * math.cos(a), cy + 138 * math.sin(a) + 30


def scene6(c, t, f, g):
    hall(c, f, g)
    carousel(c, f, g)
    back, front = [], []
    for k, (col, a0) in enumerate(((TEAL, 5.6), (GREEN, 4.1))):
        a = a0 - g * 0.5
        (back if math.sin(a) < 0 else front).append((a, col, 'ob%d' % k))
    for (a, col, key) in back:
        x, y = on_car(a); bag(c, x, y, 0.5, key, f, col=col, face='smile', eyes='closed')
    # hatch
    rrect(c, 110, 1000, 250, 250, 20); fs(c, STEELD, 9)
    rrect(c, 140, 1040, 190, 210, 14); rgb(c, hx('10172B')); c.fill()
    a_h = lerp(math.radians(196), math.radians(18), ease(seg(t, 0.45, 2.25)))
    hx_, hy_ = on_car(a_h)
    hugging = t >= 2.75
    arms = (900 - 44, 1330 - 138)
    if t < 2.25: hp = (hx_, hy_, 0.0)
    elif t < 2.75:
        u = seg(t, 2.25, 2.75); p0 = on_car(math.radians(18)); hp = (lerp(p0[0], arms[0], u), lerp(p0[1], arms[1] + 150, u) - 190 * math.sin(u * math.pi), -0.5 * math.sin(u * math.pi))
    else: hp = (arms[0], arms[1] + 150, 0.04 * math.sin(g * 6))
    if t < 0.75:
        bag(c, hx_, hy_, 0.66, 'hero', f, face='smile', eyes='dot', look=(1, 0))
    flaps(c, 140, 1040, 190, 206, g, f, math.sin(seg(t, 0.3, 0.9) * math.pi), key='fh', n=5)
    for (a, col, key) in front:
        x, y = on_car(a); bag(c, x, y, 0.5, key, f, col=col, face='smile', eyes='closed')
    sees = t > 0.9
    if not hugging:
        stick(c, 900, 1330, 0.95, 'trav', f, lh=(-80 + (10 * math.sin(g * 9) if sees else 0), -300 if sees else -20), rh=(60, -30),
              face='grin' if sees else 'flat', eyes='dot', shirt=TEAL, look=(-1, 0.2), bob=math.sin(g * 3) * 2)
        if t >= 0.75: bag(c, hp[0], hp[1], 0.66, 'hero', f, face='grin', eyes='dot', rot=hp[2], look=(1, -0.3), sw=math.sin(g * 8) * 0.12)
    else:
        bag(c, hp[0], hp[1], 0.66, 'hero', f, face='grin', eyes='closed', rot=hp[2])
        stick(c, 900, 1330, 0.95, 'trav', f, lh=(-150, -70), rh=(-10, -60), face='grin', eyes='closed', shirt=TEAL,
              bob=math.sin(g * 6) * 3)
        for i in range(3):
            q = seg(t, 2.85 + i * 0.3, 4.2 + i * 0.3)
            if 0 < q < 1: heart(c, 800 + i * 70, 1010 - 150 * q, 0.9 + 0.2 * i, CORAL, 1 - ein(q))
    caption(c, t, 0.3, [[("YOURS?", CREAM)], [("IT MADE IT.", GOLD)]], y=300, size=96)


def scene7(c, t, f, g):
    bg(c, hx('FFE2B0'), hx('FFF1D6'))
    rrect(c, 70, 560, 760, 420, 30); fs(c, hx('9FE3F0'), 9)
    c.save(); rrect(c, 76, 566, 748, 408, 26); c.clip()
    wcirc(c, 660, 690, 70, 'sun7', f, amp=3); rgb(c, hx('FFD23D')); c.fill()
    c.rectangle(70, 900, 760, 80); rgb(c, hx('F3D38A')); c.fill()
    wline(c, [(250, 980), (270, 800), (300, 700)], 'palm', f, lw=22, col=hx('A86F45'), amp=1.0)
    for k, (dx, dy) in enumerate(((-130, 30), (-90, -60), (0, -100), (90, -50), (130, 40))):
        wline(c, [(300, 700), (300 + dx * 0.6, 700 + dy * 0.8 - 20), (300 + dx, 700 + dy)], ('fr', k), f, lw=20, col=GREEN, amp=1.0)
    c.restore()
    rrect(c, 856, 600, 196, 92, 20); fs(c, PINK, 8); txt(c, "LIMA", 954, 666, 60, INK)
    c.rectangle(0, 1420, W, H - 1420); c.set_source(grad(0, 1420, 0, H, [(0, hx('E9CFA0')), (1, hx('D8B982'))])); c.fill()
    wline(c, [(0, 1420), (W, 1420)], 'fl7', f, lw=7, amp=0.8)
    carousel(c, f, g)
    a = 2.6 - g * 0.5 + 30.0 * 0.5 - 1.2
    x, y = on_car(a)
    bag(c, x, y, 0.72, 'pb', f, col=PURPLE, face='flat', eyes='big', look=(0, -1), sw=math.sin(g * 5) * 0.1)
    for k in range(2):
        q = (g * 0.7 + k * 0.5) % 1
        txt(c, "?", x + 80 + k * 30, y - 280 - 70 * q, 70, INK, CAP, a=math.sin(q * math.pi))
    caption(c, t, 0.15, [[("HAS AN AIRLINE", CREAM)], [("LOST YOURS?", GOLD)]], y=300, size=92)


SCENES = [(0.0, 3.2, scene1), (3.2, 7.6, scene2), (7.6, 12.4, scene3), (12.4, 18.2, scene4), (18.2, 23.0, scene5),
          (23.0, 27.4, scene6), (27.4, 30.0, scene7)]
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
