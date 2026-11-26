from nkit import *

DURATION = 25.0
FUR6 = hx('A7AEC2'); FURD6 = hx('7E869C'); EARP = hx('F3A9B8'); WOODF = hx('B86B3A'); WOODFD = hx('7A4220')


def mouse(c, x, y, s, f, g, key, tie=CORAL, play=1.0, mood='happy', look=(0, 0), d=1, ph=0.0):
    c.save(); c.translate(x, y); c.scale(s * d, s)
    c.new_path(); c.move_to(-26, -24); c.curve_to(-70, -20, -78, -64, -54, -80); rgb(c, INK); c.set_line_width(9); c.set_line_cap(RND); c.stroke()
    c.new_path(); c.move_to(-26, -24); c.curve_to(-70, -20, -78, -64, -54, -80); rgb(c, EARP); c.set_line_width(4); c.stroke()
    for lx in (-14, 14):
        c.new_path(); c.arc(lx, -4, 9, 0, 2 * math.pi); fs(c, EARP, 4)
    c.save(); c.translate(0, -44); c.scale(1, 1.18); c.new_path(); c.arc(0, 0, 34, 0, 2 * math.pi); c.restore(); fs(c, FUR6, 7)
    c.save(); c.translate(0, -36); c.scale(1, 1.2); c.new_path(); c.arc(0, 0, 20, 0, 2 * math.pi); c.restore(); rgb(c, hx('E3E6EF')); c.fill()
    for ex in (-24, 24):
        c.new_path(); c.arc(ex, -124, 18, 0, 2 * math.pi); fs(c, FUR6, 6)
        c.new_path(); c.arc(ex, -124, 10, 0, 2 * math.pi); rgb(c, EARP); c.fill()
    c.new_path(); c.arc(0, -96, 30, 0, 2 * math.pi); fs(c, FUR6, 7)
    lx_, ly_ = 5 * look[0], 4 * look[1]
    for sg in (-1, 1):
        if mood == 'joy':
            c.new_path(); c.arc(sg * 11 + lx_, -98 + ly_, 6, math.pi * 1.1, math.pi * 1.9); rgb(c, EYE); c.set_line_width(4); c.stroke()
        else:
            c.new_path(); c.arc(sg * 11 + lx_, -100 + ly_, 6.5 if mood == 'o' else 5.5, 0, 2 * math.pi); rgb(c, EYE); c.fill()
            c.new_path(); c.arc(sg * 11 + lx_ + 2, -102 + ly_, 2, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
    c.new_path(); c.arc(lx_ * 0.6, -86 + ly_, 5, 0, 2 * math.pi); rgb(c, hx('E86A8A')); c.fill()
    if mood == 'o':
        c.new_path(); c.arc(lx_ * 0.6, -74, 5, 0, 2 * math.pi); rgb(c, EYE); c.fill()
    elif mood == 'sad':
        c.new_path(); c.arc(lx_ * 0.6, -66, 7, math.pi * 1.2, math.pi * 1.8); rgb(c, EYE); c.set_line_width(3); c.stroke()
    else:
        c.new_path(); c.arc(lx_ * 0.6, -80, 7, 0.2 * math.pi, 0.8 * math.pi); rgb(c, EYE); c.set_line_width(3); c.stroke()
    c.new_path(); c.move_to(-12, -64); c.line_to(0, -58); c.line_to(-12, -52); c.close_path(); fs(c, tie, 3)
    c.new_path(); c.move_to(12, -64); c.line_to(0, -58); c.line_to(12, -52); c.close_path(); fs(c, tie, 3)
    # fiddle under the chin
    c.save(); c.translate(26, -58); c.rotate(-0.75)
    c.save(); c.scale(0.62, 1); c.new_path(); c.arc(0, 12, 22, 0, 2 * math.pi); c.restore(); fs(c, WOODF, 4)
    c.save(); c.scale(0.55, 1); c.new_path(); c.arc(0, -16, 16, 0, 2 * math.pi); c.restore(); fs(c, WOODF, 4)
    c.rectangle(-3, -62, 6, 48); rgb(c, WOODFD); c.fill()
    c.restore()
    bw = 14 * math.sin(g * 15 + ph) * play
    c.new_path(); c.move_to(-6 + bw, -80); c.line_to(58 + bw, -30); rgb(c, INK); c.set_line_width(4); c.stroke()
    c.new_path(); c.arc(-6 + bw, -80, 6, 0, 2 * math.pi); rgb(c, FURD6); c.fill()
    c.restore()


def micep(c, x, y, s, key, f, g, mood='happy', look=(0, 0), rot=0.0, play=1.0, **kw):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    b1 = abs(math.sin(g * 7)) * 6 * play; b2 = abs(math.sin(g * 7 + 1.6)) * 6 * play
    mouse(c, -50, -b1, 1.0, f, g, (key, 1), tie=CORAL, play=play, mood=mood, look=look)
    mouse(c, 50, -b2, 1.0, f, g, (key, 2), tie=TEAL, play=play, mood=mood, look=look, d=-1, ph=1.4)
    c.restore()


def fluff(c, x, y, s, g):
    c.save(); c.translate(x, y); b = 1 + 0.02 * math.sin(g * 3); c.scale(s, s * b)
    for (ax, ay, r) in CB:
        c.new_path(); c.arc(ax, ay, r + 8, 0, 2 * math.pi); rgb(c, INK); c.fill()
    for (ax, ay, r) in CB:
        c.new_path(); c.arc(ax, ay, r, 0, 2 * math.pi); rgb(c, SNOWW); c.fill()
    c.new_path(); c.arc(8, -44, 58, 0.25, math.pi - 0.25); rgb(c, SHADE, 0.7); c.set_line_width(9); c.stroke()
    c.restore()


def notes_up(c, x, y, g, n=4, a=1.0, spread=120):
    for k in range(n):
        ph = (g * 0.6 + k / n) % 1
        note(c, x - spread / 2 + (k * 47) % spread + 20 * math.sin(ph * 6 + k), y - 260 * ph, 0.8 + 0.4 * ph, (GOLD, CREAMT, TEAL)[k % 3], a * math.sin(ph * math.pi) ** 0.6)


def clockc(c, x, y, k, g):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k)
    c.new_path(); c.arc(0, 0, 54, 0, 2 * math.pi); fs(c, CREAMT, 7)
    for i in range(12):
        a = i * math.pi / 6
        c.new_path(); c.move_to(44 * math.cos(a), 44 * math.sin(a)); c.line_to(50 * math.cos(a), 50 * math.sin(a)); rgb(c, INK); c.set_line_width(4); c.stroke()
    c.new_path(); c.move_to(0, 0); c.line_to(0, -36); rgb(c, INK); c.set_line_width(7); c.set_line_cap(RND); c.stroke()
    a = -math.pi / 2 - 0.5 + 0.08 * math.sin(g * 8)
    c.new_path(); c.move_to(0, 0); c.line_to(42 * math.cos(a), 42 * math.sin(a)); rgb(c, CORAL); c.set_line_width(5); c.stroke()
    c.restore()


MX, MY = 756, 1398


def scA(c, t, f, g):
    k = ease(seg(t, 0.7, 1.5)); z = lerp(2.6, 1.0, k)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-lerp(712, 540, k), -lerp(1250, 960, k))
    c.rectangle(-400, -400, W + 800, H + 800); rgb(c, NAVY); c.fill()
    c.save(); rcam(c, 0.0, 46)
    rear_set(c, f, g)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    gl = cairo.RadialGradient(MX, MY - 40, 8, MX, MY - 40, 230)
    gl.add_color_stop_rgba(0, 1, 0.86, 0.45, 0.55); gl.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
    c.set_source(gl); c.rectangle(MX - 260, MY - 300, 520, 400); c.fill()
    worried = t > 1.6
    micep(c, MX, MY, 0.62, 'mi', f, g, mood='o' if worried else 'joy', look=(-1, -0.4) if worried else (0, 0), play=0.0 if worried else 1.0)
    if not worried: notes_up(c, MX, MY - 110, g, a=1.0)
    clockc(c, MX, MY - 200, eback(seg(t, 1.7, 2.0)), g)
    ox = lerp(250, 372, ease(seg(t, 0.4, 1.4)))
    otto_full(c, ox, 1400, 0.9, 'of', f, eyes='wide', mouth='o' if t < 2.4 else 'smile', look=(1, 0.9), lh=(-98, 40), rh=(98, 40), bob=abs(math.sin(g * 9)) * 6 * (1 if t < 1.4 else 0))
    c.restore(); c.restore()
    band(c, 1.0, 470)
    cap2(c, t, -1, ["Twin mice under seat 7."], y=250, size=82, gold=True, t1=1.6)
    cap2(c, t, 1.7, ["Late for their concert!"], y=250, size=84)


def pic6(c):
    c.rectangle(-200, -150, 400, 300); rgb(c, hx('27326A')); c.fill()
    c.new_path(); c.arc(-120, -80, 26, 0, 2 * math.pi); rgb(c, hx('FFF3C4')); c.fill()
    c.rectangle(-200, 110, 400, 60); rgb(c, hx('24402F')); c.fill()
    c.rectangle(-90, 10, 180, 100); rgb(c, hx('8A5A33')); c.fill()
    c.save(); c.translate(0, 10); c.scale(1, 0.25); c.new_path(); c.arc(0, 0, 90, 0, 2 * math.pi); c.restore(); rgb(c, hx('C89B63')); c.fill()
    for i in range(7):
        c.new_path(); c.arc(-90 + i * 30, -30 + 10 * math.sin(i), 6, 0, 2 * math.pi); rgb(c, (GOLD, CORAL, TEAL)[i % 3]); c.fill()
    c.new_path(); c.move_to(-90, -30); c.curve_to(-40, -10, 40, -10, 90, -30); rgb(c, CREAMT); c.set_line_width(2); c.stroke()


def scB(c, t, f, g):
    S = 0.9; ox = 372
    c.save(); rcam(c, 0.5, 23)
    rear_set(c, f, g)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    j = ease(seg(t, 0.1, 0.7))
    my = lerp(MY, GY_, j) - 140 * math.sin(j * math.pi)
    mx = lerp(MX, GX, j)
    sal = ease(seg(t, 2.3, 2.6))
    otto_full(c, ox, 1400, S, 'of', f, eyes='open', mouth='flat' if t < 2.2 else 'smile', look=(1, -0.1), lh=lerp2((-98, 40), (-70, -150), sal), rh=(98, 40), bob=math.sin(g * 3) * 2)
    micep(c, mx, my - (abs(math.sin(g * 9)) * 18 if t > 0.7 else 0), 0.78, 'mi', f, g, mood='o' if t < 2.4 else 'joy', look=(-1, -0.2), play=0.0)
    if t < 2.3: txt(c, "!", mx + 30, my - 240, 90, GOLD, SERIF)
    c.restore()
    card(c, 760, 760, eback(seg(t, 0.6, 0.9)) * 0.62, f, pic6, rot=0.05 + 0.02 * math.sin(g * 2))
    clockc(c, 920, 640, eback(seg(t, 0.8, 1.1)) * 0.9, g)
    cap2(c, t, 0.2, ["The show starts at midnight."], y=250, size=78, t1=2.2)
    cap2(c, t, 2.3, ["Otto steps on it."], y=250, size=88, gold=True)


def scC(c, t, f, g):
    fare_scene(c, t, f, g, micep, note6, "They pay in music.", "Fare: one golden note.", ps=0.78, pkw=dict(play=0.0))


def scD(c, t, f, g):
    road_scene(c, t, f, g, micep, pic6, "the old stump stage.", ps=0.36, size2=76, pkw=dict(play=0.0), pdy=-6)


STX, STY = 760, 1290


def scE(c, t, f, g):
    ext_begin(c, f, g)
    bus_ext(c, f, g, -440, 1010, 0.8, door=1.0, otto=None)
    reflect(c, g, -400, 250, 1396, n=3, depth=50)
    # the stump stage
    c.rectangle(STX - 150, STY, 300, 110); fs(c, hx('8A5A33'), 8)
    c.save(); c.translate(STX, STY); c.scale(1, 0.25); c.new_path(); c.arc(0, 0, 150, 0, 2 * math.pi); c.restore(); fs(c, hx('C89B63'), 7)
    for i in range(9):
        lx = STX - 160 + i * 40
        c.new_path(); c.arc(lx, STY - 190 + 12 * math.sin(i * 0.9), 8, 0, 2 * math.pi); rgb(c, (GOLD, CORAL, TEAL)[i % 3], 0.7 + 0.3 * math.sin(g * 6 + i)); c.fill()
    c.new_path(); c.move_to(STX - 170, STY - 190); c.curve_to(STX - 60, STY - 160, STX + 60, STY - 160, STX + 170, STY - 196); rgb(c, CREAMT); c.set_line_width(3); c.stroke()
    for i in range(6):
        ax = STX - 200 + i * 80; ay = 1452 - 10 * abs(math.sin(g * 6 + i)) * (1 if t > 2.3 else 0)
        c.save(); c.translate(ax, ay); c.scale(0.5, 0.5)
        for sg in (-1, 1):
            c.new_path(); c.arc(sg * 24, -86, 18, 0, 2 * math.pi); fs(c, FURD6, 6)
            c.new_path(); c.arc(sg * 24, -86, 9, 0, 2 * math.pi); rgb(c, EARP); c.fill()
        c.new_path(); c.arc(0, -52, 36, 0, 2 * math.pi); fs(c, FURD6, 7)
        if t > 2.3:
            for sg in (-1, 1):
                wline(c, [(sg * 34, -60), (sg * (58 + 8 * math.sin(g * 9 + i)), -110)], ('arm', i, sg), f, lw=8, col=INK, amp=0.4)
        c.restore()
    hop = seg(t, 0.2, 1.6)
    px = lerp(352, STX, ease(hop)); py = lerp(1352, STY - 6, ease(hop)) - 120 * abs(math.sin(hop * math.pi * 2))
    playing = t > 1.8
    micep(c, px, py, 0.66, 'mi', f, g, mood='joy' if playing else 'happy', look=(1, 0) if not playing else (0, 0), play=1.0 if playing else 0.0)
    if playing:
        notes_up(c, STX, STY - 160, g, n=6, spread=260)
        for i in range(3):
            hq = seg(t, 2.6 + i * 0.35, 3.8 + i * 0.35)
            if 0 < hq < 1: heart(c, STX - 160 + i * 150, 1260 - 120 * hq, 0.55 + 0.1 * i, CORAL, 1 - ein(hq))
    otto_home(c, f, g, t, wave_t=3.2, eyes='closed' if t > 2.2 else 'open', look=(1, -0.3))
    ext_end(c, g, 0.12)
    cap2(c, t, 0.2, ["Just in time."], y=250, size=90, gold=True, t1=1.75)
    cap2(c, t, 1.85, ["The show begins!"], y=250, size=90)


def scF(c, t, f, g): pin_scene(c, t, f, g, 6)


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
    stopped_bus(c, f, g, otto=('wide', 'o'), look=(-1, 0.3))
    fluff(c, 300, 1396, 0.72, g)
    if 0.2 < q < 1.4: txt(c, "!", 600, 1090, 110, GOLD, SERIF)
    ext_end(c, g, 0.2)
    c.restore()
    band(c, 1.0, 560)
    cap2(c, t, BRK + 0.1, ["Something is lying in the road."], y=250, size=74, gold=True)
    cap2(c, t, BRK + 1.0, ["Cloud, sheep or pillow? Guess!"], y=362, size=68)


SCENES = [(0.0, 3.4, scA), (3.4, 6.6, scB), (6.6, 10.4, scC), (10.4, 13.6, scD), (13.6, 17.8, scE), (17.8, 21.6, scF), (21.6, 25.0, scG)]
draw = make_draw(SCENES)
