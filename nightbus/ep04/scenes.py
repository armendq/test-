from ep2 import *

HOG = hx('8A6A4A'); HOGD = hx('5E452E'); HOGL = hx('F1DFC0'); CASE = hx('B5533C'); CASED = hx('7E3626'); STRAP = hx('E8C27A')
LEAFC = [hx('E8873A'), hx('D9542F'), hx('F2B33D'), hx('C96A2B'), hx('E9A23B')]
HEDGE = hx('2F5A3C'); HEDGEL = hx('3F7650'); OWLL = hx('EBDCBE'); OWLD = hx('5E452E')


# ------------------------------------------------------------------ helpers copied from episode 3
def feather(c, x, y, s, rot, f, key='fe'):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.save(); c.scale(0.34, 1.0); c.new_path(); c.arc(0, -50, 52, 0, 2 * math.pi); c.restore(); fs(c, OWLL, 5)
    wline(c, [(0, 10), (0, -100)], (key, 'q'), f, lw=5, col=OWLD, amp=0.3)
    c.restore()


def souvenirs(c, f):
    kid_drawing(c, 196, 560, 0.52, f, rot=-0.07)
    c.save(); c.translate(330, 742); c.rotate(0.12)
    rrect(c, -44, -60, 88, 120, 10); fs(c, WHITE, 6)
    for k in range(3):
        c.rectangle(-28, -36 + k * 26, 56, 9); rgb(c, CORAL if k == 0 else hx('B9C0D6')); c.fill()
    c.new_path(); c.arc(0, -60, 9, 0, 2 * math.pi); fs(c, TEAL, 4)
    c.restore()


# ------------------------------------------------------------------ the hedgehog and its things
def hog(c, x, y, s, key, f, face=1, eyes='open', mouth='smile', look=(0, 0), cap=None, arms=None, blush=False, rot=0.0, leafhat=False):
    """x, y = feet. face=1 looks right. cap = how far the big driver's cap has slipped (0 on the head, 1 over the eyes)."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * face, s)
    pts = []; n = 30
    for i in range(n + 1):
        a = math.radians(150 + 204 * i / n); r = 126 if i % 2 else 98
        pts.append((-24 + r * math.cos(a), -108 + r * math.sin(a)))
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path(); fs(c, HOG, 8)
    for i, (vx, vy) in enumerate(((-96, -120), (-78, -170), (-40, -200), (-104, -70), (-64, -128))):
        wline(c, [(vx - 9, vy + 8), (vx, vy - 8), (vx + 9, vy + 8)], (key, 'sp', i), f, lw=5, col=HOGD, amp=0.3)
    for sg in (-1, 1):
        c.new_path(); c.arc(8 + sg * 30, -8, 17, 0, 2 * math.pi); fs(c, HOGD, 6)
    for ex in (-30, 50):
        c.new_path(); c.arc(ex, -170, 16, 0, 2 * math.pi); fs(c, HOGD, 5)
    wcirc(c, 10, -92, 74, (key, 'b'), f, ry=88); fs(c, HOGL, 8)
    if arms:
        for i, hd in enumerate(arms):
            sg = -1 if i == 0 else 1
            wline(c, [(10 + sg * 54, -92), hd], (key, 'arm', i), f, lw=24, col=INK, amp=0.6)
            wline(c, [(10 + sg * 54, -92), hd], (key, 'arm2', i), f, lw=14, col=HOGL, amp=0.4)
            c.new_path(); c.arc(hd[0], hd[1], 12, 0, 2 * math.pi); fs(c, HOGD, 5)
    c.save(); c.translate(76, -110); c.rotate(-0.1); c.scale(1.5, 1.0); c.new_path(); c.arc(0, 0, 26, 0, 2 * math.pi); c.restore(); fs(c, HOGL, 7)
    c.new_path(); c.arc(52, -110, 23, 0, 2 * math.pi); rgb(c, HOGL); c.fill()
    c.new_path(); c.arc(110, -114, 13, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for ex, ey in ((2, -130), (46, -132)):
        if eyes == 'closed':
            c.new_path(); c.arc(ex, ey + 6, 11, 1.15 * math.pi, 1.85 * math.pi); rgb(c, INK); c.set_line_width(6); c.stroke()
        elif eyes == 'big':
            c.new_path(); c.arc(ex, ey, 17, 0, 2 * math.pi); rgb(c, WHITE); c.fill_preserve(); rgb(c, INK); c.set_line_width(4); c.stroke()
            c.new_path(); c.arc(ex + look[0] * 5, ey + look[1] * 5, 10, 0, 2 * math.pi); rgb(c, INK); c.fill()
            c.new_path(); c.arc(ex + look[0] * 5 - 3, ey + look[1] * 5 - 4, 3.5, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
        else:
            c.new_path(); c.arc(ex + look[0] * 3, ey + look[1] * 3, 9, 0, 2 * math.pi); rgb(c, INK); c.fill()
            c.new_path(); c.arc(ex + look[0] * 3 - 3, ey + look[1] * 3 - 3, 3, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
    if blush:
        for ex in (-14, 62):
            c.new_path(); c.arc(ex, -100, 13, 0, 2 * math.pi); rgb(c, hx('FF8FA3'), 0.6); c.fill()
    rgb(c, INK); c.set_line_width(6)
    if mouth == 'smile':
        c.new_path(); c.arc(72, -98, 15, 0.2 * math.pi, 0.8 * math.pi); c.stroke()
    elif mouth == 'o':
        c.new_path(); c.arc(74, -82, 8, 0, 2 * math.pi); c.fill()
    if leafhat: leaf(c, 16, -186, 1.5, -0.3, LEAFC[0])
    if cap is not None:
        c.save(); c.translate(14, -178 + cap * 56); c.rotate(-0.12 + 0.07 * min(cap, 1.0)); R = 100
        c.new_path(); c.arc(0, 0, R * 0.8, math.pi, 2 * math.pi); c.close_path(); fs(c, UNID, 7)
        c.rectangle(-R * 0.8, -R * 0.13, R * 1.6, R * 0.14); rgb(c, GOLD); c.fill()
        wline(c, [(-R * 0.98, R * 0.03), (R * 0.98, R * 0.03)], (key, 'brim'), f, lw=R * 0.13, col=INK, amp=0.6)
        c.restore()
    c.restore()


def ltag(c, x, y, s, rot, f, key='lt', string=True):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if string: wline(c, [(0, -44), (0, -80)], (key, 's'), f, lw=5, amp=0.5)
    c.new_path(); c.move_to(-24, -28); c.line_to(0, -48); c.line_to(24, -28); c.line_to(24, 46); c.line_to(-24, 46); c.close_path(); fs(c, PAPER, 6)
    c.new_path(); c.arc(0, -27, 6, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.rectangle(-14, -8, 28, 9); rgb(c, CORAL); c.fill()
    c.rectangle(-14, 10, 28, 5); rgb(c, INK, 0.5); c.fill(); c.rectangle(-14, 24, 18, 5); c.fill()
    c.restore()


def leaf(c, x, y, s, rot, col):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-26, 0); c.curve_to(-10, -20, 12, -20, 28, 0); c.curve_to(12, 18, -10, 18, -26, 0); c.close_path()
    rgb(c, col); c.fill_preserve(); rgb(c, INK); c.set_line_width(4); c.stroke()
    c.new_path(); c.move_to(-18, 0); c.line_to(18, 0); rgb(c, INK, 0.4); c.set_line_width(3); c.stroke()
    c.restore()


def suitcase(c, x, y, s, f, key='sc', lid=0.0, tag=True, rot=0.0, peek=False):
    """x, y = bottom centre. 380 wide and 290 tall at s=1. lid 0 = shut, 1 = open."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if lid < 0.02:
        wline(c, [(-52, -288), (-52, -322), (52, -322), (52, -288)], (key, 'h'), f, lw=22, col=INK, amp=0.5)
        wline(c, [(-52, -288), (-52, -322), (52, -322), (52, -288)], (key, 'h2'), f, lw=9, col=STRAP, amp=0.3)
        if peek: leaf(c, 196, -150, 1.6, 0.2, LEAFC[0]); leaf(c, 186, -168, 1.3, -0.5, LEAFC[2])
        rrect(c, -190, -290, 380, 290, 34); fs(c, CASE, 10)
        c.save(); rrect(c, -190, -290, 380, 290, 34); c.clip()
        for sx in (-110, 110):
            c.rectangle(sx - 18, -290, 36, 290); rgb(c, STRAP); c.fill()
            c.rectangle(sx - 18, -290, 4, 290); rgb(c, INK, 0.5); c.fill(); c.rectangle(sx + 14, -290, 4, 290); c.fill()
        for (cx_, cy_) in ((-190, -290), (190, -290), (-190, 0), (190, 0)):
            c.new_path(); c.arc(cx_, cy_, 52, 0, 2 * math.pi); rgb(c, CASED); c.fill()
        c.restore()
        wline(c, [(-186, -150), (186, -150)], (key, 'seam'), f, lw=7, col=INK, amp=0.5, a=0.7)
        for sx in (-110, 110):
            rrect(c, sx - 15, -168, 30, 36, 6); fs(c, GOLD, 5)
        sparkle(c, -10, -226, 26, GOLD); heart(c, 34, -62, 0.5, PINK)
        c.new_path(); c.arc(-36, -74, 22, 0, 2 * math.pi); fs(c, TEAL, 5)
        rrect(c, -190, -290, 380, 290, 34); rgb(c, INK); c.set_line_width(10); c.stroke()
        if tag: ltag(c, -76, -214, 1.0, 0.12, f, key=(key, 'tag'))
    else:
        c.save(); c.translate(-190, -150); c.rotate(-lid * 1.5)
        rrect(c, 0, -140, 380, 140, 30); fs(c, CASED, 10)
        c.restore()
        rrect(c, -190, -150, 380, 150, 26); fs(c, CASE, 10)
        c.rectangle(-172, -150, 344, 24); rgb(c, hx('3A1F18')); c.fill()
        for sx in (-110, 110):
            c.rectangle(sx - 18, -126, 36, 122); rgb(c, STRAP); c.fill()
        rrect(c, -190, -150, 380, 150, 26); rgb(c, INK); c.set_line_width(10); c.stroke()
    c.restore()


HB = ((-230, -120, 130), (-90, -200, 150), (80, -210, 150), (230, -130, 130), (0, -110, 180), (-170, -70, 110), (170, -70, 110))


def hedge(c, f, g, x, base, s=1.0, door=0.0, dx=-170):
    c.save(); c.translate(x, base); c.scale(s, s)
    gl = cairo.RadialGradient(dx, -40, 10, dx, -40, 190)
    c.save(); c.rectangle(-600, -700, 1200, 700); c.clip()
    for (ax, ay, r) in HB:
        c.new_path(); c.arc(ax, ay, r + 9, 0, 2 * math.pi); rgb(c, INK); c.fill()
    for (ax, ay, r) in HB:
        c.new_path(); c.arc(ax, ay, r, 0, 2 * math.pi); rgb(c, HEDGE); c.fill()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for (ax, ay, r, a0) in ((-90, -200, 112, 3.6), (80, -210, 112, 4.3), (230, -130, 92, 4.7), (-230, -120, 92, 3.4), (0, -110, 120, 4.0)):
        c.new_path(); c.arc(ax, ay, r, a0, a0 + 0.8); rgb(c, HEDGEL, 0.9); c.set_line_width(10); c.stroke()
    c.restore()
    gl.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.25 + 0.3 * door); gl.add_color_stop_rgba(1, 1, 0.85, 0.5, 0)
    c.set_source(gl); c.rectangle(dx - 200, -240, 400, 250); c.fill()
    c.new_path(); c.arc(dx, -44, 34, math.pi, 2 * math.pi); c.line_to(dx + 34, 0); c.line_to(dx - 34, 0); c.close_path()
    fs(c, lerp2((0.42, 0.26), (1.0, 0.85), door) + (lerp(0.14, 0.5, door),), 7)
    c.new_path(); c.arc(dx + 18, -30, 5, 0, 2 * math.pi); rgb(c, GOLD); c.fill()
    c.restore()


def bush(c, x, base, s):
    B = ((-52, -44, 52), (0, -72, 64), (56, -40, 50))
    for (ax, ay, r) in B:
        c.new_path(); c.arc(x + ax * s, base + ay * s, (r + 7) * s, math.pi, 2 * math.pi); c.close_path(); rgb(c, INK); c.fill()
    for (ax, ay, r) in B:
        c.new_path(); c.arc(x + ax * s, base + ay * s, r * s, 0, 2 * math.pi); rgb(c, HEDGE); c.fill()


def hedge_card(c, x, y, k, f, rot=0.0):
    c.save(); c.translate(x, y); c.scale(k, k); c.rotate(rot)
    rrect(c, -192, -142, 400, 300, 16); rgb(c, INK, 0.3); c.fill()
    rrect(c, -200, -150, 400, 300, 16); fs(c, PAPER, 8)
    c.save(); rrect(c, -182, -132, 364, 264, 10); c.clip()
    c.rectangle(-200, -150, 400, 300); rgb(c, hx('27326A')); c.fill()
    for (ax, ay, r) in ((-80, 60, 84), (30, 20, 108), (126, 66, 76)):
        c.new_path(); c.arc(ax, ay, r, 0, 2 * math.pi); rgb(c, HEDGEL); c.fill()
    c.rectangle(-200, 96, 400, 60); rgb(c, hx('24402F')); c.fill()
    c.new_path(); c.arc(-56, 70, 24, math.pi, 2 * math.pi); c.line_to(-32, 98); c.line_to(-80, 98); c.close_path(); rgb(c, hx('FFD98A')); c.fill()
    c.restore()
    wline(c, [(-150, -100), (-84, 24)], 'hca', f, lw=10, col=CORAL, amp=0.5)
    wline(c, [(-112, 14), (-80, 34), (-70, -2)], 'hcb', f, lw=10, col=CORAL, amp=0.5)
    c.new_path(); c.arc(0, -150, 12, 0, 2 * math.pi); fs(c, TEAL, 5)
    c.restore()


def road2(c, y, off):
    c.rectangle(-400, y, W + 800, 96); rgb(c, hx('2A3044')); c.fill()
    c.rectangle(-400, y, W + 800, 8); rgb(c, hx('4A5594')); c.fill()
    for k in range(9):
        xx = ((k * 170 + off) % 1530) - 220
        rrect(c, xx, y + 42, 90, 12, 6); rgb(c, hx('E9DFC8'), 0.8); c.fill()


def driver_sil(c, bx, by, s, duck=0.0, look=-1):
    c.save(); c.rectangle(bx + s * 40, by + s * 64, s * 122, s * 142); c.clip()
    hx0, hy0 = bx + s * 102, by + s * 168 + duck
    c.new_path(); c.arc(hx0, hy0, 44, 0, 2 * math.pi); rgb(c, hx('05070F')); c.fill()
    c.new_path(); c.arc(hx0, hy0 - 26, 42, math.pi, 2 * math.pi); c.close_path(); rgb(c, UNID); c.fill()
    c.rectangle(hx0 - 44, hy0 - 32, 88, 9); rgb(c, GOLD); c.fill()
    for sg in (-1, 1):
        c.new_path(); c.arc(hx0 + sg * 16 + look * 5, hy0 + 2, 8, 0, 2 * math.pi); rgb(c, hx('FFE14D')); c.fill()
    c.restore()


def drops(c, x, y, g, n=3):
    for k in range(n):
        ph = (g * 1.4 + k / n) % 1
        c.new_path(); c.arc(x + k * 12, y + ph * 60, 6 * (1 - ph) + 3, 0, 2 * math.pi); rgb(c, hx('BFE4FF'), 0.9 * (1 - ph)); c.fill()


# ------------------------------------------------------------------ scene A 0-3.6: the bus leaves without Otto
def scA(c, t, f, g):
    c.rectangle(0, 0, W, H); rgb(c, NAVY); c.fill()
    k = ease(seg(t, 0.6, 1.3)); z = lerp(2.0, 1.0, k)
    S = 0.55
    pan = ease(seg(t, 2.05, 3.05))
    bx = lerp(-144, -250, ease(seg(t, 0.0, 1.5))) if t < 2.05 else lerp(-250, 110, pan)
    ox = lerp(700, 690, seg(t, 0, 2.05)) if t < 2.05 else lerp(690, 706, pan)
    if t < 1.9: off = 420 * t
    else:
        d = min(t, 2.2) - 1.9; off = 798 + 420 * (d - d * d / 0.6)
    if t >= 2.05: off += bx + 250
    rolling = t < 2.15
    brake = ease(seg(t, 1.9, 2.1)) * (1 - ease(seg(t, 2.2, 2.6)))
    by = 960 + (math.sin(g * 13) * 3 + 9 * math.sin(t * 6.5) if rolling else 0)
    bxx = bx - 16 * brake
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-lerp(690, 540, k), -lerp(1290, 960, k))
    c.translate(540, 1240); c.scale(1.12, 1.12); c.translate(-520, -1180)
    country(c, f, g, 1380)
    road2(c, 1392, off)
    dr = ease(seg(t, 3.0, 3.35))
    if dr > 0.02:
        c.new_path(); c.move_to(bxx + 400, 1392); c.line_to(bxx + 548, 1392); c.line_to(bxx + 640, 1500); c.line_to(bxx + 330, 1500); c.close_path()
        rgb(c, hx('FFE7A8'), 0.2 * dr); c.fill()
    bus_ext(c, f, g, bxx, by, 0.8, door=dr, otto=None, rot=-off / 40.0)
    driver_sil(c, bxx, by, 0.8, duck=90 * ease(seg(t, 3.2, 3.35)), look=1 if t > 2.6 else -1)
    gl = cairo.RadialGradient(bxx + 694, by + 216, 4, bxx + 694, by + 216, 70)
    gl.add_color_stop_rgba(0, 1, 0.3, 0.25, 0.8); gl.add_color_stop_rgba(1, 1, 0.3, 0.25, 0)
    c.set_source(gl); c.rectangle(bxx + 610, by + 140, 170, 160); c.fill()
    rrect(c, bxx + 684, by + 196, 16, 40, 6); fs(c, hx('FF4D4D'), 5)
    if rolling or t < 2.5:
        for i in range(4):
            ph = (g * 1.1 + i / 4) % 1
            c.new_path(); c.arc(bxx + 716 + 90 * ph, by + 300 - 70 * ph, 16 + 26 * ph, 0, 2 * math.pi); rgb(c, hx('C9CFE6'), 0.5 * (1 - ph) * (1 - seg(t, 2.15, 2.5))); c.fill()
    for i, tb in enumerate((1.4, 1.68)):
        kk = eback(seg(t, tb, tb + 0.2)) * (1 - ein(seg(t, tb + 0.45, tb + 0.62)))
        if kk > 0.01:
            c.save(); c.translate(bxx + 560 + i * 90, by - 90 - i * 70); c.scale(kk, kk); c.rotate(-0.1 + 0.2 * i)
            txt(c, "BEEP!", 0, 0, 70, GOLD, SERIF); c.restore()
    run = t < 3.0
    a = math.sin(g * 16)
    otto_full(c, ox, 1396, S, 'of', f, eyes='wide' if t < 3.25 else 'open', mouth='o', look=(-1, -0.2),
              lh=(-176, -74 + (22 * a if run else 0)) if run else (-98, 30), rh=(60, -160 - (30 * a if run else 0)) if run else (98, 40),
              bob=abs(a) * 10 if run else math.sin(g * 9) * 4, tilt=-0.1 if run else 0)
    feather(c, ox + 28, 1396 - 392 * S + 174 * S, 0.36, 0.5, f, key='capf')
    drops(c, ox + 58, 1396 - 420 * S, g)
    if t < 1.0 or 3.25 < t:
        txt(c, "!" if t < 1.0 else "?", ox + 78, 1396 - 250, 100, GOLD if t < 1.0 else CREAMT, SERIF)
    if run:
        for i in range(3):
            yy = 1300 - i * 46 + 6 * math.sin(g * 9 + i)
            wline(c, [(ox + 70 + (i % 2) * 20, yy), (ox + 130 + (i % 2) * 34, yy)], ('ml', i), f, lw=6, col=WHITE, amp=1.0, a=0.6)
    rain(c, g, 0.22)
    c.restore()
    cap2(c, t, -1, ["Someone is driving Otto's bus."], y=250, size=80, gold=True, t1=2.3)
    cap2(c, t, 2.4, ["Then it stops."], y=250, size=84)


# ------------------------------------------------------------------ scene B 3.6-8: two eyes at the wheel
def scB(c, t, f, g):
    S = 0.9
    lit = ease(seg(t, 1.2, 1.38))
    u = ease(seg(t, 1.3, 1.85))
    sc = lerp(1.12, 2.0, u)
    c.save(); c.translate(lerp(-33.6, 90, u), lerp(-128, -1000, u)); c.scale(sc, sc)
    bus_int_back(c, f, g, None, moving=0.0, door=1.0)
    fall = seg(t, 3.55, 3.8)
    if t < 1.95: slip = 1.0
    elif t < 3.55: slip = lerp(1.0, 0.1, eback(seg(t, 1.95, 2.25)))
    else: slip = lerp(0.1, 1.55, eback(fall))
    up = 1.95 <= t < 3.55
    wave = 2.5 < t < 3.5
    hy = 1012 - (10 * abs(math.sin(g * 7)) if up else 0)
    suitcase(c, 140, 1250, 0.82, f)
    larm = (-22, -196) if 1.9 < t < 2.4 else (-48, -44)
    rarm = (112, -176 + 12 * math.sin(g * 11)) if wave else (86, -30)
    hog(c, 150, hy, 0.8, 'hog', f, face=1, eyes='big' if up else 'open', mouth='smile' if t < 3.55 else 'o', look=(1, 0.1), cap=slip, arms=(larm, rarm),
        blush=up)
    bus_int_front(c, f, g)
    ox = lerp(860, 700, ease(seg(t, 0.1, 0.9)))
    walking = t < 0.9
    bob = abs(math.sin(g * 9)) * 7 if walking else 0
    otto_full(c, ox, 1400, S, 'of', f, eyes='wide' if t < 1.5 else 'open', mouth='o' if t < 1.5 else 'smile', look=(-1, -0.3), lh=(-104, -40), rh=(98, 40), bob=bob)
    feather(c, ox + 52, 1400 - 392 * S, 0.62, 0.5, f, key='capf')
    hand = (ox - 104 * S, 1400 + (-40 - 175 + bob) * S)
    tgt = lerp2((330, 1390), (170, 930), ease(seg(t, 0.35, 1.15)))
    aim = math.atan2(tgt[1] - hand[1], tgt[0] - (hand[0] - 20))
    torch(c, hand[0] - 20, hand[1], aim, f)
    bxp, byp = hand[0] - 20 + 52 * math.cos(aim), hand[1] + 52 * math.sin(aim)
    L = 1300; sp = 0.2
    p1 = (bxp + L * math.cos(aim - sp), byp + L * math.sin(aim - sp)); p2 = (bxp + L * math.cos(aim + sp), byp + L * math.sin(aim + sp))
    dk = 0.8 * (1 - lit)
    if dk > 0.01:
        c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        c.new_path(); c.rectangle(-900, -900, 4000, 5000); c.move_to(bxp, byp); c.line_to(*p1); c.line_to(*p2); c.close_path()
        rgb(c, DARK, dk); c.fill(); c.set_fill_rule(cairo.FILL_RULE_WINDING)
        c.new_path(); c.move_to(bxp, byp); c.line_to(*p1); c.line_to(*p2); c.close_path(); rgb(c, hx('FFE9A8'), 0.2 * (1 - lit)); c.fill()
        blink = 0.5 < t < 0.6
        for ex in (150 + 2 * 0.8, 150 + 46 * 0.8):
            c.save(); c.translate(ex, 1012 - 100 * 0.8); c.scale(1, 0.12 if blink else 1); c.new_path(); c.arc(0, 0, 11, 0, 2 * math.pi); c.restore()
            rgb(c, hx('FFE14D'), 1 - lit); c.fill()
    if 3.55 <= t < 3.9:
        q = (t - 3.55) / 0.35
        for i in range(5):
            a = -math.pi * (0.15 + 0.7 * i / 4); r0 = 110 + 50 * q
            wline(c, [(160 + math.cos(a) * r0, 900 + math.sin(a) * r0), (160 + math.cos(a) * (r0 + 26), 900 + math.sin(a) * (r0 + 26))], ('cf', i), f, lw=6, col=WHITE,
                  amp=0.6, a=1 - q)
    c.restore()
    if 1.2 <= t < 1.32:
        c.rectangle(0, 0, W, H); rgb(c, WHITE, 0.35 * (1 - (t - 1.2) / 0.12)); c.fill()
    cap2(c, t, 0.15, ["Two eyes at the wheel."], y=250, size=84, gold=True, t1=1.2)
    cap2(c, t, 1.3, ["A hedgehog. On a suitcase."], y=250, size=80)


# ------------------------------------------------------------------ scene C 8-12.4: wrong bus, and the fare
def van(c, f):
    for sx, col, w_, h_, dy in ((-50, CASE, 84, 56, 0), (48, GOLD, 62, 44, 0), (-8, PINK, 66, 42, -50)):
        rrect(c, sx - w_ / 2, -34 - h_ + dy, w_, h_, 9); fs(c, col, 6)
    rrect(c, -136, -34, 272, 112, 24); fs(c, TEAL, 7)
    rrect(c, -122, -20, 78, 54, 12); fs(c, hx('BFE4F5'), 6)
    for wx in (-74, 78):
        c.new_path(); c.arc(wx, 80, 28, 0, 2 * math.pi); fs(c, hx('20233A'), 7)
        c.new_path(); c.arc(wx, 80, 10, 0, 2 * math.pi); rgb(c, hx('9AA3C7')); c.fill()


CLOUD = ((-150, 20, 100), (0, -40, 150), (150, 20, 104), (-64, 80, 110), (76, 84, 110))


def scC(c, t, f, g):
    S = 0.9; ox = 470
    c.save(); rear_cam(c)
    rear(c, f, g)
    for wx in (210, 500):
        rrect(c, wx, 610, 230, 320, 26); fs(c, hx('121A40'), 9)
        for k in range(6):
            yy = 620 + ((k * 0.17 + g * 0.5) % 1) * 290
            c.new_path(); c.move_to(wx + 25 + k * 36, yy); c.line_to(wx + 21 + k * 36, yy + 24); rgb(c, hx('BFD4FF'), 0.5); c.set_line_width(3); c.stroke()
    bench(c, f)
    jq = t - 3.9
    jump = 26 * math.sin(clamp(jq / 0.28) * math.pi) if jq > 0 else 0
    cx_, top = 748, 1400 - 290 * 0.8
    suitcase(c, cx_, 1400 - jump, 0.8, f, tag=t < 2.5, rot=0.03 * math.sin(jq * 30) * math.exp(-5 * jq) if jq > 0 else 0, peek=jq > 0.1)
    give = ease(seg(t, 2.5, 2.9)) * (1 - ease(seg(t, 3.3, 3.6)))
    think = 0.4 < t < 2.2
    hog(c, cx_, top - 22 - jump * 1.5, 0.6, 'hog', f, face=-1, eyes='big' if (think or jq > 0) else 'open', mouth='o' if (t < 1.4 or 0 < jq < 0.6) else 'smile',
        look=(0.3, -1) if think else (1, 0.2), arms=((-46, -50), lerp2((70, -56), (124, -112), give)), blush=1.4 < t < 2.3)
    if t < 2.6: rh = (98, 40)
    elif t < 3.3: rh = lerp2((98, 40), (150, 0), ease(seg(t, 2.6, 3.0)))
    else: rh = lerp2((150, 0), (56, -306), ease(seg(t, 3.3, 3.7)))
    sal = ease(seg(t, 3.6, 3.85))
    shake = 0.07 * math.sin(g * 9) if 1.5 < t < 2.2 else 0
    otto_full(c, ox, 1400, S, 'of', f, eyes='wide' if 0 < jq < 0.7 else 'open', mouth='flat' if t < 1.5 else ('o' if 0 < jq < 0.7 else 'smile'),
              look=(1, 0.2) if t < 3.3 or jq > 0 else (0.5, -1), lh=lerp2((-98, 40), (-70, -150), sal), rh=rh, tilt=shake)
    feather(c, ox + 52, 1400 - 392 * S, 0.62, 0.5, f, key='capf')
    hand = (ox + rh[0] * S, 1400 + (rh[1] - 175) * S)
    p0 = (cx_ - 76 * 0.8, 1400 - 214 * 0.8); ph_ = (cx_ - 124 * 0.6 - 16, top - 22 - 112 * 0.6)
    if 2.5 <= t < 2.9: tp = lerp2(p0, ph_, ease(seg(t, 2.5, 2.9)))
    elif 2.9 <= t < 3.3: tp = lerp2(ph_, (hand[0] + 6, hand[1] + 30), ease(seg(t, 2.9, 3.3)))
    else: tp = (hand[0] + 6, hand[1] + 30)
    if t >= 2.5:
        ltag(c, tp[0], tp[1], 0.9, 0.1 * math.sin(g * 6), f, key='gtag', string=False)
        if 3.7 < t < 4.2:
            q = seg(t, 3.7, 4.2)
            for i in range(6):
                a = i * math.pi / 3
                wline(c, [(tp[0] + math.cos(a) * (40 + 26 * q), tp[1] + math.sin(a) * (40 + 26 * q)), (tp[0] + math.cos(a) * (58 + 36 * q), tp[1] + math.sin(a) * (58 + 36 * q))],
                      ('tg', i), f, lw=6, col=GOLD, amp=0.5, a=1 - q)
    if 0 < jq < 0.5:
        for i in range(4):
            wline(c, [(cx_ + 150 + i * 14, 1250 - i * 36), (cx_ + 176 + i * 14, 1238 - i * 36)], ('rs', i), f, lw=6, col=WHITE, amp=1.0, a=0.8 * (1 - jq / 0.5))
    c.restore()
    kb = eback(seg(t, 0.4, 0.7)) * (1 - ein(seg(t, 2.0, 2.2)))
    if kb > 0.01:
        for i, (dx, dy, r) in enumerate(((648, 948, 13), (636, 886, 20))):
            c.new_path(); c.arc(dx, dy, r * kb, 0, 2 * math.pi); fs(c, WHITE, 6)
        c.save(); c.translate(600, 640 + 6 * math.sin(g * 2.5)); c.scale(kb, kb)
        for (dx, dy, r) in CLOUD:
            c.new_path(); c.arc(dx, dy, r + 7, 0, 2 * math.pi); rgb(c, INK); c.fill()
        for (dx, dy, r) in CLOUD:
            c.new_path(); c.arc(dx, dy, r, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
        c.save(); c.translate(-6 + 4 * math.sin(g * 9), 14); van(c, f); c.restore()
        c.restore()
        badge(c, 792, 560, eback(seg(t, 1.4, 1.65)) * kb, False, f, key='vx')
    cap2(c, t, 0.2, ["It wanted the luggage van."], y=215, size=80, t1=2.25)
    cap2(c, t, 2.35, ["Fare: one luggage tag."], y=215, size=84, gold=True)


# ------------------------------------------------------------------ scene D 12.4-16.8: to the end of the lane
def scD(c, t, f, g):
    c.rectangle(0, 0, W, H); rgb(c, NAVY); c.fill()
    c.save(); c.translate(0, 120)
    country(c, f, g, 1250)
    sp = 520
    stop = ease(seg(t, 2.9, 3.7))
    hx_ = lerp(540 + (t - 3.55) * sp, 440, stop)
    off = sp * t if t < 2.9 else sp * 2.9 + (hx_ - 202)
    hedge(c, f, g, hx_, 1250, 1.35, door=0.4 + 0.6 * stop)
    for i, tk in enumerate((0.55, 1.75)):
        bx_ = 540 + (t - tk) * sp
        if -300 < bx_ < W + 300: bush(c, bx_, 1250, 1.5 - 0.3 * i)
    road2(c, 1300, off)
    by = 1040 + (math.sin(g * 11) * 3) * (1 - stop)
    slide = -64 * math.sin(clamp(seg(t, 3.45, 4.15)) * math.pi)
    sx_, sy_ = 270 + 0.62 * 600 + slide, by + 4 - abs(math.sin(g * 11)) * 5 * (1 - stop)
    suitcase(c, sx_, sy_, 0.46, f, tag=False, rot=0.05 * math.sin(clamp(seg(t, 3.45, 4.15)) * math.pi * 2))
    for dx in (-44, 44):
        wline(c, [(sx_ + dx - 60, by + 6), (sx_ + dx, sy_ - 136), (sx_ + dx + 60, by + 6)], ('rp', dx), f, lw=6, col=STRAP, amp=0.6)
    bus_ext(c, f, g, 270, by, 0.62, door=0.0, rot=-off / 26.0, otto=('open', 'smile') if t < 3.5 or t > 4.2 else ('wide', 'o'), look=(-1, -0.4))
    c.save(); c.rectangle(270 + 0.62 * 194, by + 0.62 * 64, 0.62 * 112, 0.62 * 142); c.clip()
    hog(c, 270 + 0.62 * 246, by + 0.62 * 226, 0.36, 'hogw', f, face=-1, eyes='big', mouth='o' if t < 2.9 else 'smile', look=(1, -0.5))
    c.restore()
    reflect(c, g, 290, 780, 1396, n=4, depth=60)
    rain(c, g, 0.22)
    c.restore()
    kd = eback(seg(t, 0.3, 0.6))
    if kd > 0.01: hedge_card(c, 850, 640, kd * 0.56, f, rot=0.06 + 0.02 * math.sin(g * 2))
    badge(c, 300, 880, eback(seg(t, 3.7, 3.95)), True, f)
    cap2(c, t, 0.15, ["Stop requested:"], y=250, size=80)
    cap2(c, t, 0.85, ["the hedge at the end of the lane."], y=354, size=70, gold=True)


# ------------------------------------------------------------------ scenes E and F 16.8-25.6: the door, the suitcase, the winter bed
_lr = random.Random(4); LV = []
for _i in range(56):
    _u = _lr.uniform(-1, 1)
    LV.append(dict(vx=_lr.uniform(-560, 640), vy=_lr.uniform(-1200, -460), sp=_lr.uniform(-7, 7), col=_lr.choice(LEAFC), s=_lr.uniform(0.8, 1.3),
                   tx=660 + _u * 168, ty=1346 - (1 - _u * _u) * 140 * _lr.uniform(0.08, 1.0), d=_lr.uniform(0, 0.5), ph=_lr.uniform(0, 6.28), front=_lr.random() < 0.5))
POP = 3.85


def leaf_pos(L, T):
    e = (1 - math.exp(-2.4 * T)) / 2.4
    x = 500 + L['vx'] * e + 30 * math.sin(T * 3 + L['ph']); y = 1190 + L['vy'] * e + 150 * T * T
    k = ease(seg(T, 0.9 + L['d'], 2.0 + L['d']))
    return lerp(x, L['tx'], k), lerp(y, L['ty'], k), L['sp'] * T * (1 - k) + L['ph'] * k


def leaves(c, T, front):
    for L in LV:
        if L['front'] != front: continue
        x, y, r = leaf_pos(L, T)
        leaf(c, x, y, L['s'], r, L['col'])


def hog_fly(T): return 500 + 123 * T, 1172 - 620 * T + 560 * T * T


def yard(c, f, g, door):
    country(c, f, g, 1340)
    hedge(c, f, g, 860, 1340, 1.15, door=door)
    bus_ext(c, f, g, -330, 930, 0.8, door=1.0, otto=None)
    reflect(c, g, -300, 330, 1326, n=3, depth=50)


def scE(c, t, f, g):
    c.save(); c.translate(540, 1240); c.scale(1.5, 1.5); c.translate(-545, -1262)
    yard(c, f, g, 0.6 + 0.4 * ease(seg(t, 0.2, 0.6)))
    S = 0.5; T = t - POP
    push = ease(seg(t, 0.1, 1.5))
    if t < 2.4: cx_ = lerp(330, 470, push)
    elif t < 2.7: cx_ = lerp(470, 548, ein(seg(t, 2.4, 2.7)))
    else: cx_ = lerp(548, 500, eout(seg(t, 2.7, 3.0)))
    pushing = t < 1.5 or 2.4 <= t < 2.7
    if T < 0: ox = cx_ - 172
    else: ox = lerp(328, 262, eout(seg(T, 0, 0.35)))
    a = math.sin(g * 10)
    scratch = 2.95 < t < 3.6
    lh = (-98, 40) if not scratch else (-52, -196 + 8 * math.sin(g * 16))
    otto_full(c, ox, 1352, S, 'of', f, eyes='wide' if (2.7 <= t < 2.95 or T >= 0) else ('sleepy' if pushing else 'open'), mouth='o' if (pushing or T >= 0 or 2.7 <= t < 2.95) else 'flat',
              look=(1, 0.2) if T < 0 else (1, -0.8), lh=lh if not pushing else (60, -40), rh=(112, -60) if pushing else (98, 40),
              bob=abs(a) * 6 if pushing else math.sin(g * 3) * 2, tilt=0.14 if pushing else (-0.1 if 0 <= T < 0.4 else 0))
    feather(c, ox + 28, 1352 - 392 * S + 174 * S, 0.36, 0.5, f, key='capf')
    if pushing: drops(c, ox - 44, 1352 - 400 * S, g)
    lid = eout(seg(T, 0, 0.16)) if T >= 0 else 0
    bonk = 2.7 <= t < 3.0
    if T >= 0: leaves(c, T, False)
    suitcase(c, cx_, 1352, 0.62, f, tag=False, lid=lid, rot=-0.05 * math.sin(seg(t, 2.7, 3.0) * math.pi) if bonk else 0)
    # the hedgehog
    if t < 1.5: hxp, hyp, fc = lerp(500, 612, push), 1352 - abs(math.sin(g * 12)) * 8, 1
    elif t < 3.3: hxp, hyp, fc = 612, 1352, -1
    elif T < 0:
        uu = seg(t, 3.3, 3.7); hxp, hyp, fc = lerp(612, 500, ease(uu)), lerp(1352, 1172, ease(uu)) - 120 * math.sin(uu * math.pi), -1
    else:
        hxp, hyp = hog_fly(T); fc = 1
    hog(c, hxp, hyp, 0.42, 'hog', f, face=fc, eyes='big' if (1.5 <= t < 3.3 or T >= 0) else 'open', mouth='o' if (bonk or T >= 0) else 'smile',
        look=(1, 0.3) if t < 1.5 else ((1, 0.1) if T < 0 else (0, 1)), arms=((-46, -50), (70, -56)) if T < 0 else ((-80, -170), (96, -170)), rot=T * 5 if T >= 0 else 0)
    if T >= 0: leaves(c, T, True)
    if bonk:
        q = seg(t, 2.7, 3.0)
        for i in range(5):
            aa = -math.pi * (0.1 + 0.8 * i / 4); r0 = 30 + 60 * q
            wline(c, [(640 + math.cos(aa) * r0, 1270 + math.sin(aa) * r0), (640 + math.cos(aa) * (r0 + 26), 1270 + math.sin(aa) * (r0 + 26))], ('bk', i), f, lw=7, col=WHITE,
                  amp=0.6, a=1 - q)
    if scratch: txt(c, "?", ox + 64, 1352 - 232, 80, GOLD, SERIF)
    if 0 <= T < 0.3:
        for i in range(8):
            aa = -math.pi * (0.05 + 0.9 * i / 7); r0 = 70 + 300 * T
            wline(c, [(500 + math.cos(aa) * r0, 1230 + math.sin(aa) * r0), (500 + math.cos(aa) * (r0 + 40), 1230 + math.sin(aa) * (r0 + 40))], ('pp', i), f, lw=8, col=GOLD,
                  amp=0.6, a=1 - T / 0.3)
    rain(c, g, 0.2)
    c.restore()
    if 0 <= T < 0.1:
        c.rectangle(0, 0, W, H); rgb(c, WHITE, 0.3 * (1 - T / 0.1)); c.fill()
    cap2(c, t, 0.2, ["The door is small."], y=250, size=84, t1=2.25)
    cap2(c, t, 2.35, ["The suitcase is not."], y=250, size=84, gold=True)


def scF(c, t, f, g):
    c.save(); c.translate(540, 1240); c.scale(1.5, 1.5); c.translate(-545, -1262)
    yard(c, f, g, 1.0)
    S = 0.5; T = t + (4.4 - POP)
    ox = 262
    sal = ease(seg(t, 2.8, 3.1))
    otto_full(c, ox, 1352, S, 'of', f, eyes='wide' if t < 1.0 else ('closed' if t > 3.5 else 'open'), mouth='o' if t < 1.0 else 'smile', look=(1, -0.6) if t < 1.0 else (1, 0.3),
              lh=lerp2((-98, 40), (-70, -150), sal), rh=(98, 40), bob=math.sin(g * 3) * 2)
    feather(c, ox + 28, 1352 - 392 * S + 174 * S, 0.36, 0.5, f, key='capf')
    grow = ease(seg(T, 1.0, 2.3))
    if grow > 0.02:
        c.save(); c.translate(660, 1352); c.scale(1, 0.8 * grow); c.new_path(); c.arc(0, 0, 176, math.pi, 2 * math.pi); c.close_path(); c.restore()
        fs(c, LEAFC[3], 8)
    leaves(c, T, False)
    suitcase(c, 500, 1352, 0.62, f, tag=False, lid=1.0)
    snore = math.sin(g * 2.4)
    if T < 1.3:
        hxp, hyp = hog_fly(T)
        hog(c, hxp, hyp, 0.42, 'hog', f, face=1, eyes='big', mouth='o', look=(0.4, 1), arms=((-80, -170), (96, -170)), rot=T * 5)
    elif t >= 1.35:
        up = eback(seg(t, 1.35, 1.65))
        asleep = t > 2.5
        c.save(); c.rectangle(400, 900, 700, 1352 - 60 - 900); c.clip()
        hog(c, 660, 1352 + 40 - 150 * up + (4 * snore if asleep else 0), 0.5, 'hog', f, face=-1, eyes='closed', mouth='smile', arms=((-70, -150), (90, -150)) if not asleep else None,
            blush=True, leafhat=True)
        c.restore()
    leaves(c, T, True)
    if T < 1.6 and T >= 1.3:
        q = seg(T, 1.3, 1.6)
        for i in range(6):
            wcirc(c, 600 + i * 26 + (i - 2.5) * 40 * q, 1290 - 60 * q - (i % 2) * 20, 30 * (1 - q) + 6, ('pf', i), f, amp=3); rgb(c, WHITE, 0.8 * (1 - q)); c.fill()
    if t > 2.6:
        for k in range(3):
            ph = (g * 0.45 + k / 3) % 1
            txt(c, "z", 720 + ph * 90 + k * 8, 1180 - ph * 170, 40 + ph * 40, CREAMT, SERIF, a=math.sin(ph * math.pi))
    for i in range(3):
        q = seg(t, 2.0 + i * 0.3, 3.4 + i * 0.3)
        if 0 < q < 1: heart(c, 590 + i * 60, 1150 - 130 * q, 0.6 + 0.12 * i, CORAL, 1 - ein(q))
    lq = seg(t, 2.9, 3.6)
    if lq > 0:
        lx_, ly_ = lerp(ox + 90, ox + 8, lq) + 30 * math.sin(lq * 9) * (1 - lq), lerp(900, 1352 - 392 * S - 2, lq)
        leaf(c, lx_, ly_, 0.9, 0.4 + 2 * (1 - lq), LEAFC[2])
    rain(c, g, 0.18)
    c.restore()
    cap2(c, t, 0.2, ["It packed its winter bed."], y=250, size=82, t1=1.75)
    cap2(c, t, 1.85, ["Every passenger gets home."], y=250, size=78, gold=True)


# ------------------------------------------------------------------ scene G 25.6-30: the bell
def stop_lamp(c, x, y, on, f):
    if on:
        gl = cairo.RadialGradient(x, y, 20, x, y, 260)
        gl.add_color_stop_rgba(0, 1, 0.3, 0.25, 0.5); gl.add_color_stop_rgba(1, 1, 0.3, 0.25, 0)
        c.set_source(gl); c.rectangle(x - 280, y - 260, 560, 520); c.fill()
    rrect(c, x - 138, y - 52, 276, 104, 20); fs(c, hx('121A40'), 8)
    txt(c, "STOP", x + 30, y + 23, 64, hx('FF4D4D') if on else hx('4A2F45'), SANS)
    col = GOLD if on else hx('6B5A3A')
    c.new_path(); c.arc(x - 88, y + 2, 24, math.pi, 2 * math.pi); c.line_to(x - 58, y + 16); c.line_to(x - 118, y + 16); c.close_path(); rgb(c, col); c.fill()
    c.new_path(); c.arc(x - 88, y + 24, 7, 0, 2 * math.pi); c.fill()


def scG(c, t, f, g):
    D1, D2 = 1.4, 3.35
    rung = t >= D1
    q = t - D1; q2 = t - D2
    zz = 1 + 0.05 * ease(seg(t, D1, 4.4))
    c.save(); c.translate(700, 720); c.scale(zz, zz); c.translate(-700, -720)
    def head():
        if rung:
            jump = 24 * math.sin(clamp(q / 0.3) * math.pi) + (16 * math.sin(clamp(q2 / 0.3) * math.pi) if q2 > 0 else 0)
            otto_head(c, 150 + math.sin(g * 44) * 1.6, 935 - jump, 98, 'oh', f, eyes='wide', mouth='o', look=(0.9, -0.5) if q < 1.2 else (1.0, 0.3))
            drops(c, 54, 800, g)
        else: otto_head(c, 150 + math.sin(g * 4) * 5, 935, 98, 'oh', f, eyes='closed', mouth='smile', tilt=math.sin(g * 4) * 0.06)
    driver(c, f, g, head)
    if not rung:
        for k in range(3):
            ph = (g * 0.6 + k / 3) % 1
            x, y = 600 + k * 50 + ph * 60, 1010 - ph * 170
            c.new_path(); c.arc(x, y, 15, 0, 2 * math.pi); rgb(c, CREAMT, math.sin(ph * math.pi)); c.fill()
            c.new_path(); c.move_to(x + 13, y); c.line_to(x + 13, y - 52); c.line_to(x + 36, y - 44)
            c.set_line_width(6); rgb(c, CREAMT, math.sin(ph * math.pi)); c.stroke()
    # the collection by the seat: drawing, ticket, feather and the new luggage tag
    souvenirs(c, f)
    feather(c, 92, 830, 0.95, 0.3, f, key='pinf')
    c.new_path(); c.arc(98, 812, 9, 0, 2 * math.pi); fs(c, CORAL, 4)
    ltag(c, 212, 800 + 4 * math.sin(g * 3), 1.5, -0.08 + 0.05 * math.sin(g * 3), f, key='pint', string=False)
    c.new_path(); c.arc(212, 760, 9, 0, 2 * math.pi); fs(c, GOLD, 4)
    if t < 1.3:
        for k in range(3):
            ph = seg(t, 0.15 + k * 0.2, 0.85 + k * 0.2)
            if 0 < ph < 1: sparkle(c, 170 + k * 44, 730 + k * 46 - 20 * ph, 30 * math.sin(ph * math.pi), GOLD, 1)
    on = rung and (q < 0.5 or int(q * 4) % 2 == 0)
    stop_lamp(c, 880, 1100, on, f)
    for i, td in enumerate((D1, D2, D2 + 0.25)):
        kk = eback(seg(t, td, td + 0.16)) * (1 - ein(seg(t, td + 0.5, td + 0.7)))
        if kk > 0.01:
            c.save(); c.translate((820, 760, 890)[i], (990, 962, 926)[i]); c.scale(kk, kk); c.rotate(-0.12 + 0.1 * i)
            txt(c, "DING!", 0, 0, 72, GOLD, SERIF); c.restore()
    # the mirror shows an empty bus
    wline(c, [(790, 318), (790, 494)], 'mir', f, lw=14, amp=0.4)
    rrect(c, 548, 482, 484, 286, 44); fs(c, hx('C9CFE6'), 10)
    rrect(c, 574, 508, 432, 234, 26); fs(c, hx('0A0F24'), 8)
    c.save(); rrect(c, 578, 512, 424, 226, 22); c.clip()
    for sx in (610, 760, 910):
        dent = 14 * math.exp(-2 * q) * abs(math.sin(q * 9)) if (rung and sx == 760) else 0
        rrect(c, sx - 60, 624 + dent, 120, 200, 24); rgb(c, hx('1B2550')); c.fill()
    c.new_path(); c.move_to(600, 742); c.line_to(690, 508); c.line_to(730, 508); c.line_to(640, 742); c.close_path(); rgb(c, WHITE, 0.07); c.fill()
    sw = 0.0
    if rung: sw = 46 * math.exp(-0.9 * q) * math.sin(q * 10)
    if q2 > 0: sw += 40 * math.exp(-0.9 * q2) * math.sin(q2 * 10)
    c.new_path(); c.move_to(858, 512); c.line_to(858 + sw, 590); rgb(c, GOLD); c.set_line_width(6); c.stroke()
    c.new_path(); c.arc(858 + sw * 1.15, 604, 14, 0, 2 * math.pi); rgb(c, GOLD); c.set_line_width(6); c.stroke()
    c.restore()
    c.restore()
    cap2(c, t, 1.9, ["Who rang the bell?"], y=250, size=88, gold=True)
    cap2(c, t, 2.6, ["Ghost, mice or moth? You pick."], y=362, size=72)


SCENES = [(0.0, 3.6, scA), (3.6, 8.0, scB), (8.0, 12.4, scC), (12.4, 16.8, scD), (16.8, 21.2, scE), (21.2, 25.6, scF), (25.6, 30.0, scG)]


def draw(c, g, f):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= g < b or (i == len(SCENES) - 1 and g >= b):
            c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, g - a, f, g); c.restore()
            fa = 1 - seg(g - a, 0, 0.18)
            if i > 0 and fa > 0 and fn is not scF:
                c.rectangle(0, 0, W, H); rgb(c, NAVY, fa); c.fill()
            return
