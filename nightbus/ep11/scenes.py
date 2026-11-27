from nkit import *
from ep10bits import bow10

DURATION = 25.0
MOTHB = hx('EADFC6'); MOTHW = hx('CDBE9E'); MOTHD = hx('9C8A68')


def petal(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(0, 26); c.curve_to(-26, 6, -20, -26, 0, -34); c.curve_to(20, -26, 26, 6, 0, 26); fs(c, WHITE, 4)
    c.new_path(); c.move_to(0, 22); c.line_to(0, -16); rgb(c, hx('BFE3C0')); c.set_line_width(4); c.stroke()
    c.restore()


def spiral(c, x, y, r, g):
    c.new_path()
    for k in range(40):
        a = k * 0.45 + g * 8; rr = r * k / 40
        (c.move_to if k == 0 else c.line_to)(x + rr * math.cos(a), y + rr * math.sin(a))
    rgb(c, EYE); c.set_line_width(3.5); c.stroke()


def mothp(c, x, y, s, key, f, g, mood='happy', look=(0, 0), rot=0.0, flap=1.0, dizzy=False, **kw):
    """moth passenger; x, y = bottom (seat point)"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.set_line_cap(RND)
    w = 0.55 + 0.45 * abs(math.sin(g * 15)) if flap > 0 else 1.0
    w = lerp(1.0, w, flap)
    for sg in (-1, 1):
        c.save(); c.translate(0, -120); c.scale(sg * w, 1)
        c.new_path(); c.move_to(4, 0); c.curve_to(60, -120, 190, -110, 170, -20); c.curve_to(150, 30, 60, 30, 4, 10); c.close_path(); fs(c, MOTHW, 7)
        c.new_path(); c.arc(110, -50, 24, 0, 2 * math.pi); fs(c, TEAL, 4)
        c.new_path(); c.arc(110, -50, 10, 0, 2 * math.pi); rgb(c, INK); c.fill()
        c.new_path(); c.move_to(4, 16); c.curve_to(50, 30, 120, 60, 96, 100); c.curve_to(70, 120, 30, 90, 4, 40); c.close_path(); fs(c, MOTHD, 6)
        c.restore()
    c.save(); c.translate(0, -90); c.scale(1, 1.4); c.new_path(); c.arc(0, 0, 44, 0, 2 * math.pi); c.restore(); fs(c, MOTHB, 7)
    for i in range(3):
        c.new_path(); c.arc(0, -70 + i * 22, 30, 0.2, math.pi - 0.2); rgb(c, MOTHD, 0.6); c.set_line_width(4); c.stroke()
    for sg in (-1, 1):
        c.new_path(); c.move_to(sg * 14, -205); c.curve_to(sg * 30, -250, sg * 60, -268, sg * 76, -262); rgb(c, INK); c.set_line_width(5); c.stroke()
        for k in range(4):
            px, py = sg * (30 + k * 12), -238 - k * 7
            c.new_path(); c.move_to(px, py); c.line_to(px + sg * 8, py - 12); rgb(c, INK); c.set_line_width(3); c.stroke()
    c.new_path(); c.arc(0, -178, 46, 0, 2 * math.pi); fs(c, MOTHB, 7)
    if dizzy:
        for sg in (-1, 1): spiral(c, sg * 18, -184, 13, g * sg)
        c.new_path(); c.arc(0, -150, 9, 0, 2 * math.pi); rgb(c, EYE); c.fill()
    else:
        pface(c, 0, -190, 19, mood, look, r=9)
    c.restore()


def bloom(c, x, y, s, g, k=1.0, glow=True):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(s * k, s * k)
    if glow:
        gl = cairo.RadialGradient(0, 0, 4, 0, 0, 90)
        gl.add_color_stop_rgba(0, 1, 1, 0.9, 0.5); gl.add_color_stop_rgba(1, 1, 1, 0.9, 0)
        c.set_source(gl); c.rectangle(-90, -90, 180, 180); c.fill()
    for i in range(5):
        a = i * 2 * math.pi / 5 + 0.05 * math.sin(g * 2)
        c.save(); c.rotate(a); c.translate(0, -30); c.scale(0.9, 1.2); c.new_path(); c.arc(0, 0, 24, 0, 2 * math.pi); c.restore(); fs(c, WHITE, 5)
    c.new_path(); c.arc(0, 0, 13, 0, 2 * math.pi); fs(c, GOLD, 4)
    c.restore()


MXL, MYL = 470, 1210


def scA(c, t, f, g):
    DIM = 1.9
    k = ease(seg(t, 0.7, 1.5)); z = lerp(2.2, 1.0, k)
    sx, sy = scr(MXL + 60, MYL - 120)
    ext_begin(c, f, g, z, lerp(sx, 540, k), lerp(sy, 960, k))
    on = t < DIM
    road2(c, 1336, 0)
    if on:
        c.new_path(); c.move_to(644, 1262); c.line_to(120, 1170); c.line_to(120, 1428); c.line_to(644, 1332); c.close_path(); rgb(c, hx('FFE9A8'), 0.22); c.fill()
        gl = cairo.RadialGradient(650, 1297, 6, 650, 1297, 160)
        gl.add_color_stop_rgba(0, 1, 0.97, 0.8, 0.9); gl.add_color_stop_rgba(1, 1, 0.95, 0.7, 0)
        c.set_source(gl); c.rectangle(490, 1137, 320, 320); c.fill()
    bus_ext(c, f, g, 640, 1010 + math.sin(g * 11) * 1.5, 0.8, door=0.0, otto=('wide', 'o') if on else ('open', 'smile'), look=(-1, 0.0))
    if on:
        a = g * 5.0
        mx, my = MXL + 110 * math.cos(a), MYL + 50 * math.sin(a * 1.4)
        mothp(c, mx, my, 0.55, 'hm', f, g, mood='o', rot=0.3 * math.sin(a), dizzy=True)
    else:
        q = t - DIM
        mothp(c, lerp(MXL + 110 * math.cos(g * 5), MXL, ease(seg(q, 0, 0.6))), MYL + 30 * math.sin(g * 2), 0.55, 'hm', f, g, mood='happy' if q > 0.6 else 'o', look=(1, 0.3), dizzy=q < 0.6)
        if q < 0.4: rays(c, 650, 1297, 30 + 60 * q, 50 + 120 * q, 8, CREAMT, 1 - q / 0.4, f, 'dim', lw=6)
    ext_end(c, g, 0.08)
    band(c, 1.0, 470)
    cap2(c, t, -1, ["A moth, dizzy from the lights."], y=250, size=76, gold=True, t1=DIM - 0.1)
    cap2(c, t, DIM, ["Otto dims them. Click."], y=250, size=84)


def scB(c, t, f, g):
    S = 0.9; ox = 372; TURN = 2.2
    c.save(); rcam(c, 0.5, 23)
    rear_set(c, f, g)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    j = ease(seg(t, 0.0, 0.8))
    mx = lerp(1000, GX, j); my = lerp(760, GY_, j) - 90 * math.sin(j * math.pi)
    mothp(c, mx, my, 0.62, 'pm', f, g, mood='sad' if t < TURN else 'joy', look=(-1, 0.2), flap=1.0 if j < 1 else 0.25)
    sal = ease(seg(t, TURN + 0.1, TURN + 0.4))
    otto_full(c, ox, 1400, S, 'of', f, eyes='open', mouth='flat' if t < TURN else 'smile', look=(1, 0.0), lh=lerp2((-98, 40), (-70, -150), sal), rh=(98, 40), bob=math.sin(g * 3) * 2)
    c.restore()
    cap2(c, t, 0.2, ["It lost its way in the dark."], y=250, size=78, t1=TURN - 0.1)
    cap2(c, t, TURN, ["Otto knows the way."], y=250, size=88, gold=True)


def scC(c, t, f, g):
    fare_scene(c, t, f, g, mothp, petal, "It pays with a petal.", "Fare: one white petal.", ps=0.6, pkw=dict(flap=0.3))


def pic11(c):
    c.rectangle(-200, -150, 400, 300); rgb(c, hx('27326A')); c.fill()
    c.new_path(); c.arc(110, -80, 28, 0, 2 * math.pi); rgb(c, hx('FFF3C4')); c.fill()
    c.rectangle(-200, 40, 400, 120); rgb(c, hx('24402F')); c.fill()
    for i in range(9):
        x = -170 + i * 42; y = 30 + 26 * math.sin(i * 1.9)
        for k in range(5):
            a = k * 2 * math.pi / 5
            c.new_path(); c.arc(x + 9 * math.cos(a), y + 9 * math.sin(a), 7, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
        c.new_path(); c.arc(x, y, 4, 0, 2 * math.pi); rgb(c, GOLD); c.fill()


def scD(c, t, f, g):
    road_scene(c, t, f, g, mothp, pic11, "the field of night flowers.", ps=0.3, size2=70, pkw=dict(flap=0.3), pdy=-2)


FL = [(560 + (i % 6) * 95 + 25 * (i // 6 % 2), 1330 - (i // 6) * 70 + 10 * math.sin(i * 2.1), 0.55 + 0.15 * ((i * 7) % 3) / 2) for i in range(18)]


def scE(c, t, f, g):
    ext_begin(c, f, g)
    bus_ext(c, f, g, -440, 1010, 0.8, door=1.0, otto=None)
    reflect(c, g, -400, 250, 1396, n=3, depth=50)
    c.save(); c.translate(800, 1400); c.scale(1, 0.3); c.new_path(); c.arc(0, 0, 360, math.pi, 2 * math.pi); c.restore(); rgb(c, hx('24402F')); c.fill()
    for i, (x, y, s) in enumerate(FL):
        c.new_path(); c.move_to(x, y); c.line_to(x + 4, 1396); rgb(c, hx('3E8F5A')); c.set_line_width(6); c.stroke()
        bloom(c, x, y, s, g + i, ease(seg(t, 0.2 + 0.04 * i, 0.6 + 0.04 * i)))
    ARR = 1.8
    hp = seg(t, 0.2, ARR)
    tx, ty = FL[8][0], FL[8][1] - 6
    mx = lerp(352, tx, ease(hp)); my = lerp(1352, ty, ease(hp)) - 220 * math.sin(hp * math.pi)
    joy = t > ARR + 0.1
    mothp(c, mx, my, 0.36, 'pm', f, g, mood='joy' if joy else 'happy', look=(1, -0.2), flap=1.0 if hp < 1 else 0.2)
    for i in range(3):
        ph = (g * 0.4 + i / 3) % 1
        mothp(c, 620 + 300 * ph + 40 * math.sin(g * 3 + i), 1140 - 60 * math.sin(ph * 6 + i), 0.18, ('om', i), f, g + i, mood='happy')
    if joy:
        for i in range(3):
            hq = seg(t, ARR + 0.3 + i * 0.3, ARR + 1.4 + i * 0.3)
            if 0 < hq < 1: heart(c, tx - 80 + i * 80, ty - 200 - 90 * hq, 0.5 + 0.1 * i, CORAL, 1 - ein(hq))
    otto_home(c, f, g, t, wave_t=3.0, eyes='closed' if t > 3.5 else 'open', look=(1, -0.3))
    ext_end(c, g, 0.0)
    cap2(c, t, 0.2, ["The flowers are still open."], y=250, size=78, t1=ARR)
    cap2(c, t, ARR + 0.1, ["Home among the night flowers."], y=250, size=76, gold=True)


SOUV[10] = bow10; POS[10] = (466, 742)
SOUV[11] = petal; POS[11] = (60, 1100)


def scF(c, t, f, g): pin_scene(c, t, f, g, 11)


def shell(c, x, y, s, g):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(1, 0.62); c.new_path(); c.arc(0, 0, 110, math.pi, 2 * math.pi); c.close_path(); c.restore(); rgb(c, hx('0A0E22')); c.fill()
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
    c.rectangle(222, 1050, 12, 346); fs(c, hx('8A8FA8'), 5)
    c.new_path(); c.arc(228, 1030, 46, 0, 2 * math.pi); fs(c, hx('3F6FB5'), 6)
    txt(c, "STOP", 228, 1042, 30, WHITE, SANS)
    creep = 6 * ease(seg(q, 0.8, 2.6))
    shell(c, 300 + creep, 1396, 0.9, g)
    if 0.2 < q < 1.4: txt(c, "!", 600, 1090, 110, GOLD, SERIF)
    if q > 1.2:
        for i in range(3):
            ph = seg(q, 1.2 + i * 0.45, 1.7 + i * 0.45)
            if 0 < ph < 1: txt(c, ".", 380 + i * 30, 1330, 70, CREAMT, SERIF, a=1 - ph * 0.3)
    ext_end(c, g, 0.2)
    c.restore()
    band(c, 1.0, 560)
    cap2(c, t, BRK + 0.1, ["Someone very slow is waiting."], y=250, size=74, gold=True)
    cap2(c, t, BRK + 1.0, ["Tortoise, rock or helmet? Guess!"], y=362, size=66)


SCENES = [(0.0, 3.4, scA), (3.4, 6.6, scB), (6.6, 10.4, scC), (10.4, 13.6, scD), (13.6, 17.8, scE), (17.8, 21.6, scF), (21.6, 25.0, scG)]
draw = make_draw(SCENES)
