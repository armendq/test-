from nkit import *

DURATION = 25.0
STICKC = hx('7A4B2A')


def bow10(c, x, y, s, rot=0.0, col=CORAL):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    for sg in (-1, 1):
        c.new_path(); c.move_to(sg * 4, 0); c.line_to(sg * 30, -17); c.line_to(sg * 30, 17); c.close_path(); fs(c, col, 4)
    c.new_path(); c.arc(0, 0, 7, 0, 2 * math.pi); fs(c, GOLD, 3)
    c.restore()


def kitep(c, x, y, s, key, f, g, mood='happy', look=(0, 0), rot=0.0, broken=True, tail=True, string=True, **kw):
    """diamond kite with a face; x, y = bottom of the frame (seat point)"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.set_line_cap(RND)
    if tail:
        pts = [(0, -20)] + [(30 * i, -20 + 22 * math.sin(g * 4 + i * 1.1) - 6 * i) for i in range(1, 6)]
        for (lw, col) in ((8, INK), (3.5, CREAMT)):
            c.new_path(); c.move_to(*pts[0])
            for p in pts[1:]: c.line_to(*p)
            rgb(c, col); c.set_line_width(lw); c.stroke()
        for i in (2, 4):
            bow10(c, pts[i][0], pts[i][1], 0.62, 0.3 * math.sin(g * 4 + i))
    if string:
        sw = 10 * math.sin(g * 3)
        for (lw, col) in ((7, INK), (3, CREAMT)):
            c.new_path(); c.move_to(4, -120); c.curve_to(-20 + sw, -70, -50 - sw, -10, -44, 26); rgb(c, col); c.set_line_width(lw); c.stroke()
        if broken:
            for a in (-0.6, 0.0, 0.6):
                c.new_path(); c.move_to(-44, 26); c.line_to(-44 + 14 * math.sin(a), 26 + 14 * math.cos(a)); rgb(c, CREAMT); c.set_line_width(3); c.stroke()
    T, R, B, L, C = (0, -262), (100, -152), (0, -20), (-100, -152), (0, -152)
    for (p, q, col) in ((T, L, CORAL), (T, R, GOLD), (B, R, CORAL), (B, L, GOLD)):
        c.new_path(); c.move_to(*C); c.line_to(*p); c.line_to(*q); c.close_path(); rgb(c, col); c.fill()
    c.new_path(); c.move_to(*T); c.line_to(*R); c.line_to(*B); c.line_to(*L); c.close_path(); rgb(c, INK); c.set_line_width(9); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    for (p, q) in ((T, B), (L, R)):
        c.new_path(); c.move_to(*p); c.line_to(*q); rgb(c, STICKC, 0.55); c.set_line_width(5); c.stroke()
    pface(c, 0, -178, 30, mood, look, r=11)
    c.restore()


def wind(c, g, n=7, a=0.5, y0=500, y1=1500, seed=4):
    r = random.Random(seed)
    for i in range(n):
        y = r.uniform(y0, y1); sp = r.uniform(700, 1100); ln = r.uniform(120, 260); ph = r.uniform(0, 1)
        x = W + 300 - ((g * sp + ph * 2000) % (W + 700))
        c.new_path(); c.move_to(x, y); c.curve_to(x + ln * 0.4, y - 16, x + ln * 0.7, y + 16, x + ln, y); rgb(c, WHITE, a); c.set_line_width(5); c.set_line_cap(RND); c.stroke()


KX, KY = 300, 1180


def scA(c, t, f, g):
    k = ease(seg(t, 0.8, 1.6)); z = lerp(2.3, 1.0, k)
    sx, sy = scr(KX, KY - 130)
    ext_begin(c, f, g, z, lerp(sx, 540, k), lerp(sy, 960, k))
    stopped_bus(c, f, g, otto=('wide', 'o') if t > 1.5 else ('open', 'smile'), look=(-1, -0.4))
    ky = KY + 22 * math.sin(g * 2.6)
    kitep(c, KX, ky, 0.9, 'hk', f, g, mood='sad', look=(1, 0.3), rot=0.18 * math.sin(g * 3.1))
    ext_end(c, g, 0.06)
    wind(c, g, 8, 0.45)
    band(c, 1.0, 470)
    cap2(c, t, -1, ["A kite with a broken string."], y=250, size=78, gold=True, t1=1.7)
    cap2(c, t, 1.8, ["It can't fly home alone."], y=250, size=82)


def scB(c, t, f, g):
    S = 0.9; ox = 372; KN = 2.2
    c.save(); rcam(c, 0.5, 23)
    rear_set(c, f, g)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    j = ease(seg(t, 0.0, 0.7))
    kx = lerp(980, GX, j); ky = lerp(820, GY_, j) - 80 * math.sin(j * math.pi)
    reach = ease(seg(t, 0.9, 1.5))
    rh = lerp2((98, 40), (150, -60), reach)
    sal = ease(seg(t, KN + 0.3, KN + 0.6))
    otto_full(c, ox, 1400, S, 'of', f, eyes='open', mouth='flat' if t < KN else 'smile', look=(1, 0.2), lh=lerp2((-98, 40), (-70, -150), sal), rh=rh, bob=math.sin(g * 3) * 2)
    kitep(c, kx, ky, 0.8, 'pk', f, g, mood='sad' if t < KN else 'joy', look=(-1, 0.1), rot=0.06 * math.sin(g * 4), broken=t < KN)
    if reach > 0.05:
        hx_, hy_ = ox + 150 * S, 1400 + (-60 - 175) * S
        ex, ey = kx - 44 * 0.8, ky + 26 * 0.8
        mx, my = lerp(hx_, ex, 0.5), max(hy_, ey) + 60
        for (lw, col) in ((7, INK), (3, CREAMT)):
            c.new_path(); c.move_to(hx_, hy_); c.curve_to(lerp(hx_, mx, reach), my, ex - 10, ey + 40, ex, ey); rgb(c, col); c.set_line_width(lw); c.set_line_cap(RND); c.stroke()
        if t >= KN:
            q = t - KN
            bow10(c, ex, ey, 0.8 * eback(seg(q, 0, 0.3)), 0.2)
            if q < 0.45: rays(c, ex, ey, 40 + 40 * q, 60 + 80 * q, 8, GOLD, 1 - q / 0.45, f, 'kn')
    if t < 1.2: txt(c, "!", ox + 118, 1400 - 392 * S - 20, 100, GOLD, SERIF)
    c.restore()
    cap2(c, t, 0.2, ["Blown far from its hill."], y=250, size=82, t1=KN - 0.1)
    cap2(c, t, KN, ["Otto ties a new knot."], y=250, size=86, gold=True)


def scC(c, t, f, g):
    fare_scene(c, t, f, g, kitep, bow10, "It pays from its tail.", "Fare: one red bow.", ps=0.8, pkw=dict(broken=False))


def pic10(c):
    c.rectangle(-200, -150, 400, 300); rgb(c, hx('27326A')); c.fill()
    c.new_path(); c.arc(-120, -84, 24, 0, 2 * math.pi); rgb(c, hx('FFF3C4')); c.fill()
    c.save(); c.translate(30, 170); c.scale(1, 0.55); c.new_path(); c.arc(0, 0, 250, math.pi, 2 * math.pi); c.restore(); rgb(c, hx('2E5A3C')); c.fill()
    c.rectangle(-10, -40, 110, 80); rgb(c, hx('E9D8B4')); c.fill()
    c.new_path(); c.move_to(-26, -40); c.line_to(45, -96); c.line_to(116, -40); c.close_path(); rgb(c, hx('9A4A3A')); c.fill()
    c.rectangle(26, -18, 40, 36); rgb(c, GOLD); c.fill()
    for (x, y) in ((120, -110), (-40, -120), (160, -50)):
        c.new_path(); c.arc(x, y, 4, 0, 2 * math.pi); rgb(c, WHITE); c.fill()


def scD(c, t, f, g):
    road_scene(c, t, f, g, kitep, pic10, "the window on the windy hill.", ps=0.36, size2=66, pkw=dict(broken=False, tail=False), pdy=-4)


HX10, HY10 = 800, 1178


def house(c, g):
    c.save(); c.translate(780, 1400); c.scale(1, 0.42); c.new_path(); c.arc(0, 0, 380, math.pi, 2 * math.pi); c.restore(); fs(c, hx('2E5A3C'), 8)
    c.rectangle(HX10 - 120, HY10 - 60, 240, 170); fs(c, hx('E9D8B4'), 8)
    c.new_path(); c.move_to(HX10 - 150, HY10 - 60); c.line_to(HX10, HY10 - 170); c.line_to(HX10 + 150, HY10 - 60); c.close_path(); fs(c, hx('9A4A3A'), 8)
    gl = cairo.RadialGradient(HX10, HY10, 10, HX10, HY10, 240)
    gl.add_color_stop_rgba(0, 1, 0.85, 0.45, 0.45); gl.add_color_stop_rgba(1, 1, 0.85, 0.45, 0)
    c.set_source(gl); c.rectangle(HX10 - 260, HY10 - 260, 520, 520); c.fill()
    c.rectangle(HX10 - 58, HY10 - 30, 116, 96); fs(c, GOLD, 7)
    for sg in (-1, 1):
        c.new_path(); c.move_to(HX10 + sg * 58, HY10 - 30); c.curve_to(HX10 + sg * 30, HY10, HX10 + sg * 40, HY10 + 40, HX10 + sg * 58, HY10 + 66); c.close_path(); rgb(c, CORAL, 0.85); c.fill()


def scE(c, t, f, g):
    ext_begin(c, f, g)
    bus_ext(c, f, g, -440, 1010, 0.8, door=1.0, otto=None)
    reflect(c, g, -400, 250, 1396, n=3, depth=50)
    house(c, g)
    ARR = 1.9
    hp = seg(t, 0.2, ARR)
    kx = lerp(352, HX10, ease(hp)); ky = lerp(1352, HY10 + 70, ease(hp)) - 260 * math.sin(hp * math.pi)
    joy = t > ARR + 0.1
    s = 0.6 if hp < 1 else 0.5
    kitep(c, kx, ky, s, 'pk', f, g, mood='joy' if joy else 'happy', look=(1, -0.2) if not joy else (0, 0), rot=(0.4 * math.sin(hp * math.pi) if hp < 1 else 0.05 * math.sin(g * 3)), broken=False)
    if joy:
        for i in range(3):
            hq = seg(t, ARR + 0.3 + i * 0.3, ARR + 1.4 + i * 0.3)
            if 0 < hq < 1: heart(c, HX10 - 80 + i * 80, HY10 - 240 - 90 * hq, 0.55 + 0.1 * i, CORAL, 1 - ein(hq))
    otto_home(c, f, g, t, wave_t=3.0, eyes='closed' if t > 3.5 else 'open', look=(1, -0.6))
    ext_end(c, g, 0.0)
    wind(c, g, 4, 0.3, 500, 1100, 9)
    cap2(c, t, 0.2, ["The window is still open."], y=250, size=80, t1=ARR)
    cap2(c, t, ARR + 0.1, ["Home on the windy hill."], y=250, size=84, gold=True)


SOUV[10] = bow10
POS[10] = (466, 742)


def scF(c, t, f, g): pin_scene(c, t, f, g, 10)


def glow(c, x, y, g, a=1.0):
    gl = cairo.RadialGradient(x, y, 2, x, y, 70)
    gl.add_color_stop_rgba(0, 1, 0.97, 0.8, 0.95 * a); gl.add_color_stop_rgba(0.35, 1, 0.9, 0.55, 0.45 * a); gl.add_color_stop_rgba(1, 1, 0.9, 0.55, 0)
    c.set_source(gl); c.rectangle(x - 80, y - 80, 160, 160); c.fill()
    fl = abs(math.sin(g * 38))
    for sg in (-1, 1):
        c.save(); c.translate(x + sg * 14, y - 4); c.rotate(sg * (0.5 + 0.6 * fl)); c.scale(1, 0.5); c.new_path(); c.arc(0, 0, 18, 0, 2 * math.pi); c.restore(); rgb(c, WHITE, 0.35 * a); c.fill()
    c.new_path(); c.arc(x, y, 6, 0, 2 * math.pi); rgb(c, WHITE, a); c.fill()


def scG(c, t, f, g):
    BRK = 0.8
    if t < BRK:
        road_base(c, t, f, g, None, otto=('open', 'smile'), look=(-1, -0.3))
        band(c, 0.6, 470)
        return
    q = t - BRK
    sh = 16 * math.exp(-6 * q) * math.sin(q * 48) if q < 0.7 else 0
    c.save(); c.translate(sh, 0)
    ext_begin(c, f, g)
    stopped_bus(c, f, g, otto=('wide', 'o'), look=(-1, -0.6))
    ang = g * 4.2
    gx_, gy_ = 560 + 120 * math.cos(ang), 1180 + 60 * math.sin(ang * 1.3)
    for k in range(1, 6):
        a2 = ang - k * 0.12
        c.new_path(); c.arc(560 + 120 * math.cos(a2), 1180 + 60 * math.sin(a2 * 1.3), 5 - 0.7 * k, 0, 2 * math.pi); rgb(c, hx('FFF3C4'), 0.5 - 0.08 * k); c.fill()
    glow(c, gx_, gy_, g, ease(seg(q, 0.2, 0.6)))
    if 0.2 < q < 1.4: txt(c, "!", 760, 1060, 110, GOLD, SERIF)
    ext_end(c, g, 0.12)
    c.restore()
    band(c, 1.0, 560)
    cap2(c, t, BRK + 0.1, ["Something is circling the lights."], y=250, size=70, gold=True)
    cap2(c, t, BRK + 1.0, ["Moth, firefly or fairy? Guess!"], y=362, size=68)


SCENES = [(0.0, 3.4, scA), (3.4, 6.6, scB), (6.6, 10.4, scC), (10.4, 13.6, scD), (13.6, 17.8, scE), (17.8, 21.6, scF), (21.6, 25.0, scG)]
draw = make_draw(SCENES)
