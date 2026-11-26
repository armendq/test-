from nkit import *


def flakes(c, g, n=26, a=0.9, seed=3, x0=0, x1=W, y0=0, y1=H):
    r = random.Random(seed)
    for i in range(n):
        bx = r.uniform(x0, x1); by = r.uniform(0, y1 - y0); sp = r.uniform(70, 150); sz = r.uniform(4, 9); ph = r.uniform(0, 6.28)
        c.new_path(); c.arc(bx + 20 * math.sin(g * 1.3 + ph), y0 + (by + g * sp) % (y1 - y0), sz, 0, 2 * math.pi); rgb(c, WHITE, a); c.fill()


def scA(c, t, f, g):
    bg(c, NAVY, hx('27345A'))
    c.rectangle(0, 1420, W, 500); rgb(c, FLOOR); c.fill()
    snowp(c, 450, 1400, 2.7, 'hook-snow', f, g, mood='sad', sq=0.84, melt=1.0, look=(1, 0.6))
    rrect(c, 755, 1200, 160, 190, 18); fs(c, hx('FF8A3D'), 8)
    for i in range(4):
        c.rectangle(773+i*34, 1220, 14, 150); rgb(c, GOLD); c.fill()
    for i in range(3):
        ph=(g*1.4+i/3)%1
        wline(c, [(790+i*36,1180-170*ph),(803+i*36,1160-170*ph),(788+i*36,1140-170*ph)], ('heat-hook',i), f, lw=7, col=CORAL, a=1-ph)
    cap2(c, t, -1, ["The heater is melting him."], y=270, size=84, gold=True)



def scB(c, t, f, g):
    S = 0.9; ox = 372; OFF = 2.7
    on = t < OFF
    c.save(); rcam(c, 0.0, 46)
    rear_set(c, f, g); badge3(c)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    dk = 1 - ease(seg(t, 0.25, 0.45))
    c.save(); c.translate(752, 1404); c.scale(1, 0.2); c.new_path(); c.arc(0, 0, 150 * (1 - 0.5 * ease(seg(t, OFF, 4.3))), 0, 2 * math.pi); c.restore(); rgb(c, hx('BFE4FF'), 0.85); c.fill()
    rrect(c, 690, 1322, 132, 54, 12); fs(c, hx('FF8A3D') if on else hx('5A4A55'), 7)
    for i in range(4):
        c.rectangle(704 + i * 28, 1332, 12, 34); rgb(c, hx('FFD23D') if on else hx('3A3040')); c.fill()
    if on:
        for i in range(3):
            ph = (g * 0.9 + i / 3) % 1
            wline(c, [(710 + i * 44, 1310 - 70 * ph), (722 + i * 44, 1290 - 70 * ph), (706 + i * 44, 1268 - 70 * ph)], ('ht', i), f, lw=5, col=hx('FF8A3D'), amp=1.0, a=0.8 * (1 - ph))
    sq = 0.84 if on else lerp(0.84, 1.0, eback(seg(t, OFF, OFF + 0.5)))
    snowp(c, GX, GY_ - 4, 0.8, 'sn', f, g, mood='sad' if on else ('joy' if t > 3.3 else 'happy'), look=(-1, 0.2), sq=sq, melt=1.0 if on else 0.0)
    if dk > 0: c.rectangle(-900, -900, 4000, 5000); rgb(c, DARK, 0.34 * dk); c.fill()
    if t < 1.9: lh, rh, eyes, mouth, look = (-112, -150), (112, -150), 'wide', 'o', (1, 0.1)
    elif on: lh, rh, eyes, mouth, look = (-98, 40), lerp2((98, 40), (300, 20), ease(seg(t, 1.9, 2.6))), 'wide', 'flat', (1, 0.8)
    else: lh, rh, eyes, mouth, look = lerp2((-98, 40), (-70, -150), ease(seg(t, 3.3, 3.6))), lerp2((300, 20), (98, 40), ease(seg(t, OFF, OFF + 0.5))), 'open', 'smile', (1, 0.1)
    reach = ease(seg(t, 1.9, 2.6)) * (1 - ease(seg(t, OFF, OFF + 0.5)))
    otto_full(c, ox + 40 * reach, 1400, S, 'of', f, eyes=eyes, mouth=mouth, look=look, lh=lh, rh=rh, bob=math.sin(g * 3) * 2, tilt=0.12 * reach)
    if 0.3 < t < 1.2: txt(c, "!", ox + 118, 1400 - 392 * S - 20, 110, GOLD, SERIF)
    if 0 <= t - OFF < 0.4:
        q = (t - OFF) / 0.4; rays(c, 756, 1349, 40 + 60 * q, 60 + 110 * q, 8, hx('BFE4FF'), 1 - q, f, 'off', lw=6)
    if not on:
        flakes(c, g, 14, 0.85 * ease(seg(t, OFF, OFF + 0.5)), 5, 560, 940, 560, 1380)
    c.restore()
    cap2(c, t, 0.3, ["A snowman!"], y=240, size=90, gold=True, t1=1.9)
    cap2(c, t, 2.0, ["And the heater is on."], y=240, size=84, t1=3.0)
    cap2(c, t, 3.1, ["Click. Heater off."], y=240, size=86)


def scC(c, t, f, g):
    fare_scene(c, t, f, g, snowp, flake, "Home before sunrise, please.", "Fare: one snowflake.", ps=0.8, seat3=True, size1=76)


def pic9(c):
    c.rectangle(-200, -150, 400, 300); rgb(c, hx('27326A')); c.fill()
    c.new_path(); c.arc(-110, -70, 30, 0, 2 * math.pi); rgb(c, hx('FFF3C4')); c.fill()
    c.save(); c.translate(30, 160); c.scale(1, 0.62); c.new_path(); c.arc(0, 0, 240, math.pi, 2 * math.pi); c.restore(); rgb(c, WHITE); c.fill()
    for (x, s) in ((10, 1.0), (70, 0.7)):
        c.new_path(); c.arc(x, 0 - 6 * s, 24 * s, 0, 2 * math.pi); rgb(c, hx('DDE6FA')); c.fill(); c.new_path(); c.arc(x, -38 * s - 6 * s, 16 * s, 0, 2 * math.pi); c.fill()
    for (x, y) in ((120, -100), (-30, -110), (150, -40)):
        c.new_path(); c.arc(x, y, 5, 0, 2 * math.pi); rgb(c, WHITE); c.fill()


def scD(c, t, f, g):
    road_scene(c, t, f, g, snowp, pic9, "the hill where the snow stays.", ps=0.4, size2=70, pdy=4)


def scE(c, t, f, g):
    ext_begin(c, f, g)
    dawn = seg(t, 0.0, 4.4)
    gl = cairo.RadialGradient(960, GY5, 30, 960, GY5, 760)
    gl.add_color_stop_rgba(0, 1, 0.62, 0.35, 0.55 * dawn); gl.add_color_stop_rgba(0.5, 1, 0.5, 0.45, 0.22 * dawn); gl.add_color_stop_rgba(1, 1, 0.5, 0.45, 0)
    c.set_source(gl); c.rectangle(100, 400, 1000, 1000); c.fill()
    sun = ease(seg(t, 3.0, 4.4))
    c.new_path(); c.arc(930, GY5 + 70 - 90 * sun, 70, 0, 2 * math.pi); rgb(c, hx('FFD98A')); c.fill()
    c.rectangle(-300, GY5 - 6, 1700, 800); rgb(c, hx('E6EDFB')); c.fill()
    bus_ext(c, f, g, -440, 1010, 0.8, door=1.0, otto=None)
    c.save(); c.translate(720, GY5 + 14); c.scale(1, 0.5); c.new_path(); c.arc(0, 0, 330, math.pi, 2 * math.pi); c.restore(); fs(c, SNOWW, 8)
    top = GY5 - 150
    ARR = 1.7
    joy = t > ARR + 0.3
    snowp(c, 820, top + 26, 0.72, 'pa', f, g, mood='joy' if joy else 'happy', look=(-1, 0.2), rot=0.03 * math.sin(g * 4))
    snowp(c, 900 + 0, top + 78, 0.42, 'ki', f, g, mood='joy' if joy else 'o', look=(-1, 0), rot=0.06 * math.sin(g * 7))
    hp = seg(t, 0.2, ARR); x = lerp(352, 690, ease(hp)); y = lerp(1396, top + 12, ease(hp)) - 46 * abs(math.sin(hp * math.pi * 4))
    snowp(c, x, y, 0.66, 'sn', f, g, mood='joy' if joy else 'happy', look=(1, 0), rot=0.07 * math.sin(g * 12) * (1 if hp < 1 else 0.4))
    for i in range(3):
        hq = seg(t, 2.1 + i * 0.3, 3.3 + i * 0.3)
        if 0 < hq < 1: heart(c, 720 + i * 60, top - 240 - 80 * hq, 0.6 + 0.12 * i, CORAL, 1 - ein(hq))
    flakes(c, g, 30, 0.85, 7, 120, 960, 300, 1500)
    otto_home(c, f, g, t, wave_t=3.0, eyes='closed' if t > 3.6 else 'open', look=(1, -0.3))
    ext_end(c, g, 0.0)
    cap2(c, t, 0.2, ["Home before the sun."], y=250, size=86, t1=1.95)
    cap2(c, t, 2.05, ["Just in time."], y=250, size=92, gold=True)


def scF(c, t, f, g): pin_scene(c, t, f, g, 9)


def scG(c, t, f, g):
    TUG = 2.9
    lk = ease(seg(t, TUG, TUG + 0.35)); lift = 0.04 * lk * (1 + 0.15 * math.sin(g * 22))
    road_base(c, t, f, g, None, otto=('wide', 'o') if t > 0.9 else ('open', 'smile'), look=(-0.2, -1) if t > 0.9 else (-1, -0.3), lift=lift)
    dp = eout(seg(t, 0.4, 1.1))
    ax, ay = 118, 1058 - 30 * lk
    if dp > 0:
        tx_, ty_ = 330 + 16 * math.sin(g * 3), -30
        ex, ey = lerp(tx_, ax, dp), lerp(ty_, ay, dp)
        sag = 60 * (1 - lk) * math.sin(g * 2.4)
        for (lw, col) in ((9, INK), (4, CREAMT)):
            c.new_path(); c.move_to(tx_, ty_); c.curve_to(tx_ - 40 + sag, 300, ex + 60 - sag, ey - 300, ex, ey); rgb(c, col); c.set_line_width(lw); c.set_line_cap(RND); c.stroke()
        if dp >= 1:
            for sg in (-1, 1):
                c.new_path(); c.move_to(ex, ey); c.line_to(ex + sg * 26, ey - 16); c.line_to(ex + sg * 26, ey + 16); c.close_path(); fs(c, CORAL, 5)
    if lk > 0 and t - TUG < 0.5: txt(c, "!", 250, 1010, 110, GOLD, SERIF)
    band(c, ease(seg(t, 0.0, 0.9)), 560)
    cap2(c, t, 1.25, ["What is on the other end?"], y=250, size=80, gold=True)
    cap2(c, t, 2.0, ["Kite, balloon or star?"], y=362, size=74)


SCENES = [(0.0, 3.6, scA), (3.6, 8.0, scB), (8.0, 12.4, scC), (12.4, 16.8, scD), (16.8, 21.2, scE), (21.2, 25.6, scF), (25.6, 30.0, scG)]
draw = make_draw(SCENES)


# November 26 retention edit. Values: output seconds, source start, source end.
from edit import edited_draw
EDIT = [(2, 0, 3.6), (3.8, 3.6, 8), (4, 8, 12.4), (3.2, 12.4, 16.8), (5, 16.8, 21.2), (3, 21.2, 25.6), (4, 25.6, 30)]
DURATION = sum(shot[0] for shot in EDIT)
draw = edited_draw(SCENES, EDIT)
