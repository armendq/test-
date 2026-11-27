from nkit import *
from ep10bits import bow10
from ep11bits import petal

DURATION = 25.0
SHELL = hx('7A8F4A'); SHELLD = hx('566B30'); SKIN = hx('B7C77A'); FROST = hx('DDEBFF')


def clover(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(0, 4); c.curve_to(4, 16, 2, 26, -4, 34); rgb(c, INK); c.set_line_width(6); c.set_line_cap(RND); c.stroke()
    c.new_path(); c.move_to(0, 4); c.curve_to(4, 16, 2, 26, -4, 34); rgb(c, hx('5BBF6A')); c.set_line_width(3); c.stroke()
    for a in (-math.pi / 2, math.pi / 6, 5 * math.pi / 6):
        c.save(); c.rotate(a); c.translate(13, 0)
        for sg in (-1, 1):
            c.new_path(); c.arc(0, sg * 6, 9, 0, 2 * math.pi); fs(c, hx('5BBF6A'), 3)
        c.restore()
    c.restore()


def tortp(c, x, y, s, key, f, g, mood='happy', look=(0, 0), rot=0.0, d=1, walk=0.0, sleepy=False, **kw):
    """tortoise passenger; x, y = bottom; faces right when d=1"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * d, s)
    c.set_line_cap(RND)
    for (lx, ph) in ((-80, 0), (-30, 1.6), (40, 3.1), (90, 4.7)):
        st = 8 * math.sin(g * 7 + ph) * walk
        rrect(c, lx - 18 + st, -50, 36, 50, 14); fs(c, SKIN, 6)
    hx_, hy_ = 150, -86 - 6 * math.sin(g * 3)
    c.new_path(); c.move_to(80, -60); c.curve_to(110, -70, 120, -80, hx_ - 20, hy_); rgb(c, INK); c.set_line_width(44); c.stroke()
    c.new_path(); c.move_to(80, -60); c.curve_to(110, -70, 120, -80, hx_ - 20, hy_); rgb(c, SKIN); c.set_line_width(30); c.stroke()
    c.save(); c.translate(hx_, hy_); c.scale(1.15, 1); c.new_path(); c.arc(0, 0, 44, 0, 2 * math.pi); c.restore(); fs(c, SKIN, 7)
    c.save(); c.translate(hx_ + 6, hy_ - 4); c.scale(1 / s, 1 / s); c.scale(s, s)
    if sleepy:
        for sg in (-1, 1):
            c.new_path(); c.arc(sg * 14 + 4, -4, 8, 0.1, math.pi - 0.1); rgb(c, EYE); c.set_line_width(4); c.stroke()
        c.new_path(); c.arc(6, 16, 7, 0, 2 * math.pi); rgb(c, EYE); c.fill()
    else:
        pface(c, 4, -12, 14, mood, look, r=7)
    c.restore()
    c.save(); c.translate(0, -40); c.scale(1, 0.78); c.new_path(); c.arc(0, 0, 132, math.pi, 2 * math.pi); c.close_path(); c.restore(); fs(c, SHELL, 9)
    for (px, py, r) in ((-62, -78, 30), (0, -112, 32), (62, -78, 30), (-2, -60, 26)):
        c.new_path()
        for k in range(6):
            a = k * math.pi / 3 + math.pi / 6
            (c.move_to if k == 0 else c.line_to)(px + r * math.cos(a), py + r * math.sin(a))
        c.close_path(); rgb(c, SHELLD); c.set_line_width(5); c.stroke()
    rrect(c, -140, -48, 280, 22, 10); fs(c, hx('C9B36A'), 6)
    c.restore()


def wall(c, g, frost=0.0):
    c.rectangle(560, 1150, 560, 250); fs(c, hx('8C8FA6'), 8)
    for r in range(4):
        y = 1150 + r * 62
        c.new_path(); c.move_to(560, y); c.line_to(1120, y); rgb(c, INK, 0.35); c.set_line_width(4); c.stroke()
        for k in range(5):
            x = 560 + (0 if r % 2 else 56) + k * 112
            c.new_path(); c.move_to(x, y); c.line_to(x, y + 62); rgb(c, INK, 0.35); c.set_line_width(4); c.stroke()
    c.save(); c.translate(760, 1396); c.scale(1, 0.62); c.new_path(); c.arc(0, 0, 110, math.pi, 2 * math.pi); c.close_path(); c.restore(); rgb(c, hx('1A1426')); c.fill()
    for i in range(7):
        x = 560 + i * 80
        c.new_path(); c.arc(x, 1396, 40, math.pi, 2 * math.pi); rgb(c, hx('6B4A2E')); c.fill()
    for i in range(5):
        x = 600 + i * 110; y = 1380
        c.new_path(); c.move_to(x, y); c.line_to(x - 10, y - 40); c.move_to(x, y); c.line_to(x + 12, y - 34); rgb(c, hx('5BBF6A')); c.set_line_width(5); c.stroke()
    if frost > 0:
        r = random.Random(9)
        for i in range(30):
            sparkle(c, r.uniform(80, 1100), r.uniform(1240, 1420), 10 + 6 * math.sin(g * 4 + i), FROST, frost * (0.5 + 0.5 * math.sin(g * 3 + i)))


TX, TY = 300, 1396


def scA(c, t, f, g):
    k = ease(seg(t, 0.8, 1.6)); z = lerp(2.3, 1.0, k)
    sx, sy = scr(TX + 40, TY - 60)
    ext_begin(c, f, g, z, lerp(sx, 540, k), lerp(sy, 960, k))
    stopped_bus(c, f, g, otto=('open', 'smile') if t > 1.6 else ('wide', 'o'), door=ease(seg(t, 1.9, 2.4)), look=(-1, 0.4))
    c.rectangle(222, 1050, 12, 346); fs(c, hx('8A8FA8'), 5)
    c.new_path(); c.arc(228, 1030, 46, 0, 2 * math.pi); fs(c, hx('3F6FB5'), 6)
    txt(c, "STOP", 228, 1042, 30, WHITE, SANS)
    tortp(c, TX + 30 * seg(t, 0, 3.4), TY, 0.62, 'ht', f, g, mood='sad', look=(1, 0), walk=1.0)
    r = random.Random(4)
    for i in range(16):
        sparkle(c, r.uniform(60, 700), r.uniform(1300, 1420), 8, FROST, 0.6 + 0.4 * math.sin(g * 4 + i))
    ext_end(c, g, 0.0)
    band(c, 1.0, 470)
    cap2(c, t, -1, ["A tortoise, racing the frost."], y=250, size=78, gold=True, t1=1.8)
    cap2(c, t, 1.9, ["It must sleep before winter."], y=250, size=78)


def scB(c, t, f, g):
    S = 0.9; ox = 372; TURN = 2.2
    c.save(); rcam(c, 0.5, 23)
    rear_set(c, f, g)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    lift = ease(seg(t, 0.2, 1.2))
    if t < 1.2:
        tortp(c, lerp(560, GX - 20, lift), lerp(1396, GY_ - 6, lift) - 60 * math.sin(lift * math.pi), 0.5, 'pt', f, g, mood='o', look=(1, -0.3))
    else:
        tortp(c, GX - 20, GY_ - 6, 0.5, 'pt', f, g, mood='joy' if t > TURN else 'happy', look=(-1, 0), d=-1)
    sal = ease(seg(t, TURN + 0.1, TURN + 0.4))
    rh = lerp2((98, 40), (180, -40), lift) if t < 1.3 else lerp2((180, -40), (98, 40), ease(seg(t, 1.3, 1.7)))
    otto_full(c, ox, 1400, S, 'of', f, eyes='open', mouth='smile', look=(1, 0.2), lh=lerp2((-98, 40), (-70, -150), sal), rh=rh, bob=math.sin(g * 3) * 2)
    c.restore()
    cap2(c, t, 0.2, ["Otto gives it a lift."], y=250, size=86, t1=TURN - 0.1)
    cap2(c, t, TURN, ["Its first bus ride!"], y=250, size=90, gold=True)


def scC(c, t, f, g):
    fare_scene(c, t, f, g, tortp, clover, "It pays with a clover.", "Fare: one lucky clover.", ps=0.5, pkw=dict(d=-1))


def pic12(c):
    c.rectangle(-200, -150, 400, 300); rgb(c, hx('27326A')); c.fill()
    c.new_path(); c.arc(-120, -80, 24, 0, 2 * math.pi); rgb(c, hx('FFF3C4')); c.fill()
    c.rectangle(-170, -10, 340, 130); rgb(c, hx('8C8FA6')); c.fill()
    for r in range(3):
        c.new_path(); c.move_to(-170, -10 + r * 44); c.line_to(170, -10 + r * 44); rgb(c, INK, 0.35); c.set_line_width(3); c.stroke()
    c.save(); c.translate(10, 120); c.scale(1, 0.62); c.new_path(); c.arc(0, 0, 60, math.pi, 2 * math.pi); c.close_path(); c.restore(); rgb(c, hx('1A1426')); c.fill()
    c.rectangle(-200, 120, 400, 40); rgb(c, hx('24402F')); c.fill()


def scD(c, t, f, g):
    road_scene(c, t, f, g, tortp, pic12, "the burrow under the old wall.", ps=0.24, size2=66, pkw=dict(d=-1), pdy=-4)


def scE(c, t, f, g):
    ext_begin(c, f, g)
    bus_ext(c, f, g, -440, 1010, 0.8, door=1.0, otto=None)
    frost = ease(seg(t, 0.4, 3.6))
    wall(c, g, frost)
    ARR = 2.2
    wk = seg(t, 0.1, ARR)
    tx = lerp(352, 700, ease(wk)); s = 0.42
    if t < ARR + 0.6:
        tortp(c, tx, 1396, s, 'pt', f, g, mood='happy', look=(1, 0), walk=1.0 if wk < 1 else 0.0, sleepy=t > ARR)
    else:
        q = seg(t, ARR + 0.6, ARR + 1.4)
        c.save(); c.translate(760, 1396); c.scale(1, 0.62); c.new_path(); c.arc(0, 0, 110, math.pi, 2 * math.pi); c.close_path(); c.restore(); c.clip()
        tortp(c, lerp(700, 790, q), 1396, s, 'pt', f, g, sleepy=True)
        c.reset_clip()
        if q >= 1:
            for i in range(3):
                ph = (g * 0.5 + i / 3) % 1
                txt(c, "z", 800 + 30 * i + 20 * ph, 1300 - 120 * ph, 44 + 10 * i, CREAMT, SERIF, a=1 - ph)
    otto_home(c, f, g, t, wave_t=3.0, eyes='closed' if t > 3.6 else 'open', look=(1, -0.2))
    ext_end(c, g, 0.0)
    cap2(c, t, 0.2, ["The first frost is coming."], y=250, size=82, t1=ARR)
    cap2(c, t, ARR + 0.1, ["Home, warm and sleepy."], y=250, size=86, gold=True)


SOUV[10] = bow10; POS[10] = (466, 742)
SOUV[11] = petal; POS[11] = (60, 1100)
SOUV[12] = clover; POS[12] = (474, 620)


def scF(c, t, f, g): pin_scene(c, t, f, g, 12)


def lantern(c, x, y, s, g):
    c.save(); c.translate(x, y); c.scale(s, s)
    gl = cairo.RadialGradient(0, -50, 6, 0, -50, 140)
    gl.add_color_stop_rgba(0, 1, 0.9, 0.55, 0.8 + 0.15 * math.sin(g * 9)); gl.add_color_stop_rgba(1, 1, 0.85, 0.45, 0)
    c.set_source(gl); c.rectangle(-150, -190, 300, 300); c.fill()
    c.new_path(); c.arc(0, -110, 18, math.pi, 2 * math.pi); rgb(c, INK); c.set_line_width(6); c.stroke()
    rrect(c, -34, -96, 68, 90, 10); rgb(c, hx('FFE08A')); c.fill_preserve(); rgb(c, INK); c.set_line_width(6); c.stroke()
    c.rectangle(-40, -10, 80, 14); rgb(c, INK); c.fill()
    c.restore()


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
    rrect(c, 140, 1290, 260, 26, 8); fs(c, hx('7A4B2A'), 6)
    for x in (170, 370):
        c.rectangle(x - 8, 1316, 16, 80); fs(c, hx('7A4B2A'), 5)
    lantern(c, 270, 1290, 0.8, g)
    if 0.2 < q < 1.4: txt(c, "!", 600, 1090, 110, GOLD, SERIF)
    ext_end(c, g, 0.15)
    c.restore()
    band(c, 1.0, 560)
    cap2(c, t, BRK + 0.1, ["Someone left a lantern behind."], y=250, size=74, gold=True)
    cap2(c, t, BRK + 1.0, ["Gnome, fairy or elf? Guess!"], y=362, size=70)


SCENES = [(0.0, 3.4, scA), (3.4, 6.6, scB), (6.6, 10.4, scC), (10.4, 13.6, scD), (13.6, 17.8, scE), (17.8, 21.6, scF), (21.6, 25.0, scG)]
draw = make_draw(SCENES)
