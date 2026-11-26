from nkit import *

LX, LYY = 300, 1396


def scA(c, t, f, g):
    k = ease(seg(t, 0.6, 1.3)); z = lerp(1.6, 1.0, k); sx, sy = scr(LX, LYY)
    ext_begin(c, f, g, z, lerp(sx + 90, 540, k), lerp(sy - 250, 960, k))
    OUT = 2.2
    stopped_bus(c, f, g, otto=('wide', 'o') if t < OUT else None, door=ease(seg(t, OUT - 0.3, OUT)))
    if t >= OUT:
        w = ease(seg(t, OUT, 3.5)); ox = lerp(600, 470, w)
        otto_full(c, ox, 1396, 0.55, 'of', f, eyes='wide', mouth='o', look=(-1, 0.6), lh=(-98, 40), rh=(98, 40), bob=abs(math.sin(g * 9)) * 6 * (1 if w < 1 else 0))
    cloudp(c, LX + 3 * math.sin(g * 40), LYY, 0.72, 'cl', f, g, mood='sad', look=(1, -0.2), sq=0.78 + 0.03 * math.sin(g * 8), rot=0.03 * math.sin(g * 6))
    if t < 1.4: txt(c, "!", 560, 1110, 110, GOLD, SERIF)
    ext_end(c, g, 0.22)
    band(c, 1 - k)
    cap2(c, t, -1, ["Something is lying in the road."], y=250, size=74, gold=True, t1=2.2)
    cap2(c, t, 2.3, ["It is soft. And it is crying."], y=250, size=78)


def scB(c, t, f, g):
    ext_begin(c, f, g)
    stopped_bus(c, f, g, otto=None, door=1.0)
    FALL = 2.1
    up = ease(seg(t, 1.3, 2.0))
    lookup = t >= FALL + 0.3
    otto_full(c, 470, 1396, 0.55, 'of', f, eyes='open', mouth='flat' if t < 1.0 else 'smile', look=(-1, 0.6) if not lookup else (-0.4, -1),
              lh=lerp2((-98, 40), (-150, -40), ease(seg(t, 0.9, 1.3))), rh=(98, 40), bob=math.sin(g * 3) * 2, tilt=-0.08 if t < FALL else 0)
    if t < 0.9: txt(c, "?", 520, 1150, 90, CREAMT, SERIF)
    cy_ = LYY - 70 * up - 8 * abs(math.sin(g * 5)) * up
    if lookup:
        fp = ease(seg(t, FALL + 0.3, FALL + 1.3))
        for i in range(12):
            u = i / 11
            if u <= fp:
                c.new_path(); c.arc(lerp(LX + 60, 690, u), lerp(cy_ - 200, 700, u) + 120 * math.sin(u * math.pi) * 0.3, 7, 0, 2 * math.pi); rgb(c, CREAMT, 0.8); c.fill()
        for i, (x, y) in enumerate(((640, 690), (840, 760))):
            cloudp(c, x + 10 * math.sin(g * 0.8 + i), y, 0.6 - 0.1 * i, ('fm', i), f, g, mood='o', look=(-0.6, 1))
    cloudp(c, LX + 30 * up, cy_, 0.72, 'cl', f, g, mood='sad' if (t < 1.2 or lookup) else 'happy', look=(1, -0.4) if not lookup else (0.4, -1), sq=0.8 + 0.1 * up)
    ext_end(c, g, 0.2)
    cap2(c, t, 0.2, ["A small cloud."], y=250, size=90, gold=True, t1=2.0)
    cap2(c, t, 2.1, ["It fell out of the sky."], y=250, size=84)


def scC(c, t, f, g):
    fare_scene(c, t, f, g, cloudp, jar, "Too full of rain to fly.", "Fare: one raindrop.", ps=0.85, pkw=dict(sq=0.84))


def pic7(c):
    c.rectangle(-200, -150, 400, 300); rgb(c, hx('27326A')); c.fill()
    c.new_path(); c.arc(-110, -70, 30, 0, 2 * math.pi); rgb(c, hx('FFF3C4')); c.fill()
    c.save(); c.translate(40, 150); c.scale(1, 0.55); c.new_path(); c.arc(0, 0, 230, math.pi, 2 * math.pi); c.restore(); rgb(c, hx('2E6A4A')); c.fill()
    for (x, y, r) in ((30, -60, 34), (70, -76, 42), (112, -56, 32), (-24, -8, 22), (4, -18, 26), (30, -6, 20)):
        c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); rgb(c, WHITE); c.fill()


def scD(c, t, f, g):
    road_scene(c, t, f, g, cloudp, pic7, "the sky above the hill.", ps=0.4, size2=76, pkw=dict(sq=0.84))


def scE(c, t, f, g):
    ext_begin(c, f, g)
    bus_ext(c, f, g, -440, 1010, 0.8, door=1.0, otto=None)
    reflect(c, g, -400, 250, 1396, n=3, depth=50)
    c.save(); c.translate(720, GY5 + 16); c.scale(1, 0.52); c.new_path(); c.arc(0, 0, 330, math.pi, 2 * math.pi); c.restore(); fs(c, hx('24503A'), 8)
    top = (720, GY5 - 152)
    RAIN0, UP0 = 1.9, 2.9
    for i, (x, y) in enumerate(((610, 760), (850, 850))):
        cloudp(c, x + 10 * math.sin(g * 0.8 + i), y, 0.95 - 0.15 * i, ('fm', i), f, g, mood='joy' if t > 3.4 else 'happy', look=(0.2 - 0.6 * i, 1))
    p = ease(seg(t, 0.1, 1.0))
    if t < UP0:
        hopv = 30 * abs(math.sin(seg(t, 1.0, 1.9) * math.pi * 2)) if 1.0 < t < 1.9 else 0
        x, y = lerp(352, top[0], p), lerp(1352, top[1], p) - 80 * math.sin(p * math.pi) - hopv
        sq = lerp(0.8, 1.0, ease(seg(t, RAIN0, UP0))); mood = 'happy' if t < 1.0 else ('o' if t < RAIN0 else 'joy')
    else:
        u = ease(seg(t, UP0, 4.0)); x, y = lerp(top[0], 742, u), lerp(top[1], 1000, u) + 8 * math.sin(g * 3); sq = 1.0; mood = 'joy'
    if RAIN0 <= t < UP0 + 0.4:
        for i in range(8):
            ph = (g * 2.2 + i / 8) % 1
            c.new_path(); c.move_to(x - 76 + i * 22, y + 6 + ph * 130); c.line_to(x - 80 + i * 22, y + 30 + ph * 130); rgb(c, hx('BFE4FF'), 0.9 * (1 - ph)); c.set_line_width(5); c.set_line_cap(RND); c.stroke()
    for i in range(5):
        fk = eback(seg(t, RAIN0 + 0.25 + i * 0.16, RAIN0 + 0.55 + i * 0.16))
        if fk > 0.01:
            fx_ = 610 + i * 55; fy_ = GY5 - 150 + abs(i - 2) * 16
            wline(c, [(fx_, fy_), (fx_, fy_ - 34 * fk)], ('st', i), f, lw=5, col=hx('5BBF6A'), amp=0.4)
            c.new_path(); c.arc(fx_, fy_ - 40 * fk, 11 * fk, 0, 2 * math.pi); fs(c, (CORAL, GOLD, PINK, GOLD, CORAL)[i], 4)
    cloudp(c, x, y, 0.62, 'cl', f, g, mood=mood, look=(0.3, -1), sq=sq)
    if 1.0 < t < RAIN0: txt(c, "?", x + 96, y - 150, 80, CREAMT, SERIF)
    for i in range(3):
        hq = seg(t, 3.2 + i * 0.3, 4.3 + i * 0.3)
        if 0 < hq < 1: heart(c, 700 + i * 60, 900 - 90 * hq, 0.6 + 0.12 * i, CORAL, 1 - ein(hq))
    otto_home(c, f, g, t, wave_t=3.1, eyes='closed' if t > 3.6 else 'open', look=(1, -1))
    ext_end(c, g, 0.14)
    cap2(c, t, 0.2, ["Too heavy to float."], y=250, size=88, t1=1.85)
    cap2(c, t, 1.95, ["So it rains. Then up it goes!"], y=250, size=76, gold=True)


def scF(c, t, f, g): pin_scene(c, t, f, g, 7)
def scG(c, t, f, g): field_scene(c, t, f, g, tease=True)


SCENES = [(0.0, 3.6, scA), (3.6, 8.0, scB), (8.0, 12.4, scC), (12.4, 16.8, scD), (16.8, 21.2, scE), (21.2, 25.6, scF), (25.6, 30.0, scG)]
draw = make_draw(SCENES)
