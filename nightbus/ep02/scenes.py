from base import *

FOX = hx('F28A3A'); FOXD = hx('3A2A22'); DARK = hx('070B1C'); HILL = hx('2F5A3C'); HILLD = hx('1E3F2A'); PAPER = hx('FFF7E6')


# ------------------------------------------------------------------ characters and props
def fox(c, x, y, s, key, f, face=1, eyes='open', mouth='smile', look=(0, 0), scarf=CORAL, wag=0.0, ear=0.0, apron=False, arms=None):
    """x, y = feet. face=1 looks right."""
    c.save(); c.translate(x, y); c.scale(s * face, s)
    c.save(); c.translate(-46, -46); c.rotate(-0.45 + wag)
    blob(c, [(10, 10), (-70, -20), (-160, -90), (-128, -182), (-36, -120)]); fs(c, FOX, 8)
    c.new_path(); c.arc(-128, -138, 34, 0, 2 * math.pi); fs(c, WHITE, 6)
    c.restore()
    wcirc(c, 0, -80, 62, (key, 'b'), f, ry=82); fs(c, FOX, 8)
    c.save(); c.translate(8, -62); c.scale(1, 1.5); c.new_path(); c.arc(0, 0, 34, 0, 2 * math.pi); c.restore(); rgb(c, FUR); c.fill()
    if apron:
        rrect(c, -34, -112, 84, 96, 18); fs(c, WHITE, 6)
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * 30, -8, 19, 0, 2 * math.pi); fs(c, FOXD, 6)
    if arms:
        for i, hd in enumerate(arms):
            sg = -1 if i == 0 else 1
            wline(c, [(sg * 44, -130), hd], (key, 'arm', i), f, lw=24, col=INK, amp=0.6)
            wline(c, [(sg * 44, -130), hd], (key, 'arm2', i), f, lw=14, col=FOX, amp=0.4)
            c.new_path(); c.arc(hd[0], hd[1], 13, 0, 2 * math.pi); fs(c, FOXD, 5)
    if scarf:
        rrect(c, -54, -172, 108, 32, 15); fs(c, scarf, 6)
        rrect(c, -58, -160, 26, 62, 10); fs(c, scarf, 6)
    hy = -236; R = 80
    for sg in (-1, 1):
        c.save(); c.translate(sg * 50, hy - 50); c.rotate(sg * (0.28 + ear))
        c.new_path(); c.move_to(-32, 16); c.line_to(0, -78); c.line_to(32, 16); c.close_path(); fs(c, FOX, 8)
        c.new_path(); c.move_to(-13, 6); c.line_to(0, -42); c.line_to(13, 6); c.close_path(); rgb(c, FOXD); c.fill()
        c.restore()
    wcirc(c, 0, hy, R, (key, 'h'), f, ry=R * 0.9); path = c.copy_path(); fs(c, FOX, 8)
    c.save(); c.new_path(); c.append_path(path); c.clip()
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * 38, hy + 58, 54, 0, 2 * math.pi); rgb(c, FUR); c.fill()
    c.restore()
    c.new_path(); c.append_path(path); rgb(c, INK); c.set_line_width(8); c.stroke()
    c.new_path(); c.arc(look[0] * 4, hy + 24, 11, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for sg in (-1, 1):
        ex, ey = sg * 32, hy - 8
        if eyes == 'closed':
            c.new_path(); c.arc(ex, ey + 8, 13, 1.15 * math.pi, 1.85 * math.pi); rgb(c, INK); c.set_line_width(7); c.stroke()
        elif eyes == 'big':
            c.new_path(); c.arc(ex, ey, 21, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
            c.new_path(); c.arc(ex + look[0] * 6, ey + look[1] * 6, 13, 0, 2 * math.pi); rgb(c, INK); c.fill()
            c.new_path(); c.arc(ex + look[0] * 6 - 4, ey + look[1] * 6 - 5, 4.5, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
        else:
            c.new_path(); c.arc(ex + look[0] * 4, ey + look[1] * 4, 10, 0, 2 * math.pi); rgb(c, INK); c.fill()
            c.new_path(); c.arc(ex + look[0] * 4 - 3, ey + look[1] * 4 - 4, 3.2, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
    rgb(c, INK); c.set_line_width(6)
    if mouth == 'smile':
        c.new_path(); c.arc(0, hy + 30, 15, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
    elif mouth == 'o':
        c.new_path(); c.arc(0, hy + 48, 8, 0, 2 * math.pi); c.fill()
    elif mouth == 'grin':
        c.new_path(); c.arc(0, hy + 36, 17, 0, math.pi); c.close_path(); rgb(c, CORAL); c.fill_preserve(); rgb(c, INK); c.stroke()
    c.restore()


def kid_drawing(c, x, y, k, f, rot=0.0, key='kd'):
    c.save(); c.translate(x, y); c.scale(k, k); c.rotate(rot)
    rrect(c, -192, -142, 400, 300, 16); rgb(c, INK, 0.3); c.fill()
    rrect(c, -200, -150, 400, 300, 16); fs(c, PAPER, 8)
    c.save(); rrect(c, -194, -144, 388, 288, 12); c.clip()
    c.save(); c.translate(0, 190); c.scale(1.5, 1.0); c.new_path(); c.arc(0, 0, 160, 0, 2 * math.pi); c.restore()
    rgb(c, hx('7DCB6A')); c.fill()
    wline(c, [(-10, 36), (20, -10), (-6, -44), (26, -80)], (key, 'tr'), f, lw=13, col=hx('8A5A33'), amp=2.5)
    wcirc(c, 34, -92, 40, (key, 'cr'), f, amp=5, ry=30); rgb(c, hx('3FA65A')); c.fill()
    sparkle(c, 130, -96, 32, hx('FFC83D'))
    for (fx, fs_) in ((-110, 1.0), (-60, 0.7)):
        c.new_path(); c.move_to(fx - 16 * fs_, 60); c.line_to(fx, 60 - 34 * fs_); c.line_to(fx + 16 * fs_, 60); c.close_path(); rgb(c, FOX); c.fill()
        c.new_path(); c.arc(fx, 60 - 40 * fs_, 13 * fs_, 0, 2 * math.pi); rgb(c, FOX); c.fill()
    c.restore()
    c.new_path(); c.arc(0, -150, 12, 0, 2 * math.pi); fs(c, CORAL, 5)
    c.restore()


def torch(c, x, y, ang, f):
    c.save(); c.translate(x, y); c.rotate(ang)
    rrect(c, -34, -15, 60, 30, 8); fs(c, hx('8FA3B8'), 6)
    c.new_path(); c.move_to(22, -18); c.line_to(52, -30); c.line_to(52, 30); c.line_to(22, 18); c.close_path(); fs(c, GOLD, 6)
    c.restore()


def badge(c, x, y, k, ok, f, key='bd'):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k)
    c.new_path(); c.arc(0, 0, 72, 0, 2 * math.pi); fs(c, GREEN if ok else hx('FF4D4D'), 9)
    if ok: wline(c, [(-32, 2), (-10, 26), (36, -24)], (key, 'ok'), f, lw=17, col=WHITE, amp=0.6)
    else:
        wline(c, [(-26, -26), (26, 26)], (key, 'x1'), f, lw=17, col=WHITE, amp=0.6)
        wline(c, [(26, -26), (-26, 26)], (key, 'x2'), f, lw=17, col=WHITE, amp=0.6)
    c.restore()


# ------------------------------------------------------------------ sets
def rear(c, f, g, moving=0.0, bars=False):
    c.rectangle(-900, -900, W + 2400, 1424); rgb(c, CEIL); c.fill()
    c.rectangle(-900, 524, W + 2400, 880); rgb(c, WALL); c.fill()
    wline(c, [(-900, 524), (W + 900, 524)], 'cl', f, lw=8, amp=0.6)
    for lx in (250, 620):
        gl = cairo.RadialGradient(lx + 90, 510, 10, lx + 90, 510, 400)
        gl.add_color_stop_rgba(0, 1, 0.93, 0.7, 0.26); gl.add_color_stop_rgba(1, 1, 0.93, 0.7, 0)
        c.set_source(gl); c.rectangle(lx - 320, 100, 820, 1000); c.fill()
        if bars:
            rrect(c, lx, 500, 180, 22, 11); rgb(c, hx('FFF2CC')); c.fill()
    for wx in (210, 500):
        rrect(c, wx, 610, 230, 320, 26); fs(c, hx('121A40'), 9)
        c.save(); rrect(c, wx + 5, 615, 220, 310, 22); c.clip()
        for k in range(6):
            xx = wx + ((k * 97 + g * 700) % 330) - 50
            c.rectangle(xx, 640 + k * 48, 70, 7); rgb(c, hx('FFD98A'), 0.7); c.fill()
        c.restore()
    wline(c, [(170, 566), (850, 566)], 'rail', f, lw=12, col=GOLD, amp=0.6)
    for sx in (300, 420, 600, 720):
        wline(c, [(sx, 566), (sx, 600)], ('strap', sx), f, lw=6, col=GOLD, amp=0.4)
    c.rectangle(-900, 1400, W + 2400, 1500); rgb(c, FLOOR); c.fill()
    c.rectangle(-900, 1476, W + 2400, 12); rgb(c, hx('6B76A6')); c.fill()
    c.rectangle(860, 524, 900, 880); rgb(c, hx('33416E')); c.fill()
    wline(c, [(860, 524), (860, 1400)], 'bw', f, lw=8, amp=0.6)
    wline(c, [(-900, 1400), (W + 900, 1400)], 'fl', f, lw=8, amp=0.6)
    sx = 250
    rrect(c, sx, 1010, 60, 250, 24); fs(c, SEATD, 8)
    rrect(c, sx - 10, 1220, 210, 90, 26); fs(c, SEAT, 8)
    wline(c, [(sx + 24, 1310), (sx + 24, 1400)], ('sl', sx), f, lw=12); wline(c, [(sx + 170, 1310), (sx + 170, 1400)], ('sr', sx), f, lw=12)


def bench(c, f):
    rrect(c, 800, 1000, 64, 262, 24); fs(c, SEATD, 8)
    rrect(c, 650, 1220, 214, 90, 26); fs(c, SEAT, 8)
    wline(c, [(676, 1310), (676, 1400)], 'bl', f, lw=12); wline(c, [(836, 1310), (836, 1400)], 'br', f, lw=12)


def rear_cam(c):
    c.translate(-250 * 1.3, 1440 - 1400 * 1.3); c.scale(1.3, 1.3)


CS = 0.6


def country(c, f, g, gy):
    bg(c, NAVY, hx('2A3470'))
    for (x, y, r, p) in STARS:
        a = 0.35 + 0.4 * math.sin(g * 2 + p * 6.28)
        c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); rgb(c, WHITE, max(0.1, a)); c.fill()
    gl = cairo.RadialGradient(190, 520, 40, 190, 520, 260)
    gl.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.34); gl.add_color_stop_rgba(1, 1, 0.95, 0.75, 0)
    c.set_source(gl); c.rectangle(-100, 240, 600, 560); c.fill()
    wcirc(c, 190, 520, 70, 'moon', f, amp=1.5); rgb(c, hx('FFF3C4')); c.fill()
    c.new_path(); c.arc(218, 498, 62, 0, 2 * math.pi); rgb(c, hx('1A2250')); c.fill()
    c.rectangle(-400, gy, W + 800, H); c.set_source(grad(0, gy, 0, gy + 700, [(0, hx('24402F')), (1, hx('12241C'))])); c.fill()


def hill(c, f, g, x, base, kind, s=1.0, door=0.0):
    c.save(); c.translate(x, base); c.scale(s, s)
    c.save(); c.scale(1.35, 1.0); c.new_path(); c.arc(0, 0, 250, math.pi, 2 * math.pi); c.close_path(); c.restore(); fs(c, HILL, 9)
    c.save(); c.scale(1.35, 1.0); c.new_path(); c.arc(-40, 0, 170, math.pi * 1.05, math.pi * 1.6); c.restore()
    rgb(c, hx('3F7650'), 0.7); c.set_line_width(10); c.stroke()
    if kind == 'mill':
        wpoly(c, [(-36, -238), (36, -238), (24, -400), (-24, -400)], 'ml', f); fs(c, hx('E9DFC8'), 7)
        c.save(); c.translate(0, -400); c.rotate(g * 2.2)
        for k in range(4):
            c.save(); c.rotate(k * math.pi / 2); rrect(c, -14, -150, 28, 150, 8); fs(c, hx('C9B48A'), 6); c.restore()
        c.new_path(); c.arc(0, 0, 16, 0, 2 * math.pi); fs(c, INK, 4); c.restore()
    elif kind == 'two':
        for (tx, th, r) in ((-80, 80, 62), (70, 120, 78)):
            wline(c, [(tx, -228), (tx, -228 - th)], ('tt', tx), f, lw=18, col=hx('6B4A2B'), amp=1.0)
            wcirc(c, tx, -228 - th - r * 0.7, r, ('tc', tx), f); fs(c, hx('3F7650'), 7)
    else:
        wline(c, [(0, -244), (34, -300), (-8, -352), (34, -404), (10, -440)], 'ht', f, lw=20, col=hx('6B4A2B'), amp=1.2)
        wcirc(c, 40, -470, 74, 'hc', f, ry=54); fs(c, hx('3F7650'), 7)
        wcirc(c, -34, -430, 44, 'hc2', f, ry=34); fs(c, hx('3F7650'), 7)
        tw_ = 0.75 + 0.25 * math.sin(g * 5)
        gl = cairo.RadialGradient(170, -560, 4, 170, -560, 120)
        gl.add_color_stop_rgba(0, 1, 0.9, 0.5, 0.5 * tw_); gl.add_color_stop_rgba(1, 1, 0.9, 0.5, 0)
        c.set_source(gl); c.rectangle(40, -690, 260, 260); c.fill()
        sparkle(c, 170, -560, 44 * tw_, hx('FFD23D'))
        gl = cairo.RadialGradient(-150, -70, 10, -150, -70, 170)
        gl.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.25 + 0.3 * door); gl.add_color_stop_rgba(1, 1, 0.85, 0.5, 0)
        c.set_source(gl); c.rectangle(-330, -250, 360, 260); c.fill()
        c.new_path(); c.arc(-150, -62, 60, math.pi, 2 * math.pi); c.line_to(-90, 0); c.line_to(-210, 0); c.close_path()
        fs(c, lerp2((0.42, 0.26), (1.0, 0.85), door) + (lerp(0.14, 0.5, door),), 7)
        c.new_path(); c.arc(-116, -40, 7, 0, 2 * math.pi); rgb(c, GOLD); c.fill()
    c.restore()


def road(c, f, g, y, sp):
    c.rectangle(-400, y, W + 800, 96); rgb(c, hx('2A3044')); c.fill()
    c.rectangle(-400, y, W + 800, 8); rgb(c, hx('4A5594')); c.fill()
    for k in range(9):
        xx = ((k * 170 + g * sp) % 1530) - 220
        rrect(c, xx, y + 42, 90, 12, 6); rgb(c, hx('E9DFC8'), 0.8); c.fill()


# ------------------------------------------------------------------ scene A 0-3.5: the eyes
def driver(c, f, g, head, moving=1.0):
    c.save(); c.translate(430, 1080); c.scale(1.75, 1.75); c.translate(-150, -960)
    bus_int_back(c, f, g, None, moving=moving, door=0.0, bars=False)
    wcirc(c, 150, 1150, 108, 'ob', f, amp=1.2, ry=140); fs(c, UNI, 9)
    for i in range(2):
        c.new_path(); c.arc(150, 1080 + i * 46, 7, 0, 2 * math.pi); rgb(c, GOLD); c.fill()
    head()
    bus_int_front(c, f, g)
    wline(c, [(215, 1085), (262, 1010)], 'oa', f, lw=40, col=INK, amp=0.8); wline(c, [(215, 1085), (262, 1010)], 'oa2', f, lw=28, col=UNI, amp=0.5)
    c.new_path(); c.arc(264, 1004, 22, 0, 2 * math.pi); fs(c, STRIPE, 6)
    c.restore()


def scA(c, t, f, g):
    zz = 1 + 0.06 * ease(seg(t, 0.0, 3.5))
    c.save(); c.translate(700, 720); c.scale(zz, zz); c.translate(-700, -720)
    turn = ease(seg(t, 1.9, 2.5))
    def head():
        otto_head(c, 150 + math.sin(g * 44) * 2.2, 935, 98, 'oh', f, eyes='wide', mouth='o', look=(lerp(0.9, 1.0, turn), lerp(-0.9, 0.2, turn)),
                  tilt=0.1 * turn)
        for k in range(3):
            ph = (g * 1.4 + k / 3) % 1
            c.new_path(); c.arc(60 + k * 14, 800 + ph * 90, 7 * (1 - ph) + 3, 0, 2 * math.pi); rgb(c, hx('BFE4FF'), 0.9 * (1 - ph)); c.fill()
    driver(c, f, g, head)
    wline(c, [(790, 318), (790, 494)], 'mir', f, lw=14, amp=0.4)
    rrect(c, 548, 482, 484, 286, 44); fs(c, hx('C9CFE6'), 10)
    rrect(c, 574, 508, 432, 234, 26); fs(c, hx('0A0F24'), 8)
    c.save(); rrect(c, 578, 512, 424, 226, 22); c.clip()
    for sx in (610, 760, 910):
        rrect(c, sx - 60, 624, 120, 200, 24); rgb(c, hx('1B2550')); c.fill()
    c.new_path(); c.move_to(600, 742); c.line_to(690, 508); c.line_to(730, 508); c.line_to(640, 742); c.close_path(); rgb(c, WHITE, 0.07); c.fill()
    blink = (0.9 < t < 1.02) or (2.6 < t < 2.72)
    e = 0.12 if blink else 1.0
    for sg in (-1, 1):
        c.save(); c.translate(790 + sg * 44, 620); c.scale(1, e); c.new_path(); c.arc(0, 0, 26, 0, 2 * math.pi); c.restore()
        rgb(c, hx('FFE14D')); c.fill()
        c.save(); c.translate(790 + sg * 44 - 8, 620); c.scale(0.3, e); c.new_path(); c.arc(0, 0, 22, 0, 2 * math.pi); c.restore()
        rgb(c, INK); c.fill()
    c.restore()
    c.restore()
    cap2(c, t, -1, ["Something is in the back seat."], y=250, size=80, gold=True, t1=2.05)
    cap2(c, t, 2.1, ["Otto has to look."], y=250, size=84)


# ------------------------------------------------------------------ scene B 3.5-9.5: torch and shadow
def shadow_beast(c, g, grow, sa):
    c.save(); c.translate(975, 1190); c.scale(grow, grow)
    tw_ = math.sin(g * 6) * 0.12
    rgb(c, INK, 0.86 * sa)
    c.new_path(); c.arc(0, -150, 150, 0, 2 * math.pi); c.fill()
    c.new_path(); c.arc(0, -400, 150, 0, 2 * math.pi); c.fill()
    for sg in (-1, 1):
        c.save(); c.translate(sg * 96, -500); c.rotate(sg * (0.3 + tw_))
        c.new_path(); c.move_to(-62, 40); c.line_to(0, -170); c.line_to(62, 40); c.close_path(); c.fill(); c.restore()
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * 58, -410, 21, 0, 2 * math.pi); rgb(c, hx('FFE14D'), sa); c.fill()
    c.restore()


def scB(c, t, f, g):
    S = 0.9
    lit = ease(seg(t, 3.5, 3.8))
    c.save(); rear_cam(c)
    rear(c, f, g, moving=1.0)
    bench(c, f)
    up = eback(seg(t, 3.0, 3.3))
    if up > 0.01:
        wave = (70 + 8 * math.sin(g * 10), -214) if t > 4.3 else (40, -70)
        fox(c, 752, 1224, CS * up, 'cub', f, face=-1, eyes='closed' if t < 4.0 else 'big', mouth='smile' if t > 4.0 else 'o', look=(1, -0.2),
            wag=math.sin(g * 9) * 0.25 if t > 4.2 else 0, ear=-0.15 if t < 4.0 else 0, arms=((-40, -70), wave))
    ox = lerp(330, 520, ease(seg(t, 0.2, 2.8)))
    scared = 1.0 < t < 3.5
    bob = abs(math.sin(g * 9)) * 7 if t < 2.8 else 0
    jit = math.sin(g * 46) * 2.4 if scared else 0
    rh = (104, -40)
    hand = (ox + jit + rh[0] * S, 1400 + (rh[1] - 175 + bob) * S)
    tgt = lerp2((975, 800), (760, 1090), ease(seg(t, 2.95, 3.3)))
    aim = math.atan2(tgt[1] - hand[1], tgt[0] - (hand[0] + 20))
    otto_full(c, ox + jit, 1400, S, 'of', f, eyes='wide' if scared else 'open', mouth='o' if scared else ('smile' if t > 3.9 else 'flat'),
              look=(1, -0.5) if t < 3.2 else (1, 0.2), lh=(-98, 40) if t < 4.4 else lerp2((-98, 40), (-70, -150), ease(seg(t, 4.4, 4.7))),
              rh=rh, bob=bob)
    torch(c, hand[0] + 20, hand[1], aim, f)
    bx, by = hand[0] + 20 + 52 * math.cos(aim), hand[1] + 52 * math.sin(aim)
    L = 1200; sp = 0.27
    p1 = (bx + L * math.cos(aim - sp), by + L * math.sin(aim - sp)); p2 = (bx + L * math.cos(aim + sp), by + L * math.sin(aim + sp))
    dk = 0.78 * (1 - lit)
    if dk > 0.01:
        c.set_fill_rule(cairo.FILL_RULE_EVEN_ODD)
        c.new_path(); c.rectangle(-900, -900, 4000, 5000); c.move_to(bx, by); c.line_to(*p1); c.line_to(*p2); c.close_path()
        rgb(c, DARK, dk); c.fill(); c.set_fill_rule(cairo.FILL_RULE_WINDING)
        c.new_path(); c.move_to(bx, by); c.line_to(*p1); c.line_to(*p2); c.close_path(); rgb(c, hx('FFE9A8'), 0.2 * (1 - lit)); c.fill()
    grow = lerp(0.7, 1.12, ease(seg(t, 0.8, 2.8))) * (1 - 0.8 * ease(seg(t, 3.0, 3.25)))
    sa = ease(seg(t, 0.8, 1.15)) * (1 - ease(seg(t, 3.05, 3.3)))
    if sa > 0.01:
        c.save(); c.new_path(); c.move_to(bx, by); c.line_to(*p1); c.line_to(*p2); c.close_path(); c.clip()
        c.rectangle(866, 528, 900, 868); c.clip()
        shadow_beast(c, g, grow, sa); c.restore()
    if t > 4.6:
        hq = seg(t, 4.6, 5.8)
        if hq < 1: heart(c, 690, 960 - 80 * hq, 0.8, CORAL, 1 - ein(hq))
    c.restore()
    if 3.5 <= t < 3.62:
        c.rectangle(0, 0, W, H); rgb(c, WHITE, 0.35 * (1 - (t - 3.5) / 0.12)); c.fill()
    cap2(c, t, 0.25, ["It looks big."], y=215, size=84, t1=3.0)
    cap2(c, t, 3.1, ["It is not."], y=215, size=88, gold=True)


# ------------------------------------------------------------------ scene C 9.5-15: acorn and drawing
def acorn(c, x, y, s, punched=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.scale(1, 1.25); c.new_path(); c.arc(0, 8, 22, 0, 2 * math.pi); c.restore(); fs(c, hx('C98A4B'), 5)
    c.new_path(); c.arc(0, -8, 25, math.pi, 2 * math.pi); c.close_path(); fs(c, hx('7A5230'), 5)
    c.rectangle(-3, -44, 6, 14); rgb(c, hx('7A5230')); c.fill()
    if punched:
        sparkle(c, 0, 14, 11, WHITE)
    c.restore()


def scC(c, t, f, g):
    S = 0.9; ox = 500
    c.save(); rear_cam(c)
    rear(c, f, g, moving=1.0)
    bench(c, f)
    give = ease(seg(t, 0.5, 1.0)); taken = t > 1.5; back = ease(seg(t, 2.3, 2.7))
    show = t > 3.0
    cub_arm = lerp2((40, -70), (96, -150), give) if not show else (70, -230)
    fox(c, 752, 1224, CS, 'cub', f, face=-1, eyes='big', mouth='smile', look=(1, -0.3), wag=math.sin(g * 8) * 0.2,
        arms=((-30, -80), cub_arm))
    cub_hand = (752 - CS * lerp(40, 96, give), 1224 - CS * lerp(70, 150, give))
    if t < 1.5:
        rh = lerp2((98, 40), (150, 10), ease(seg(t, 1.0, 1.5)))
    elif t < 2.3: rh = (112, -30)
    else: rh = lerp2((112, -30), (150, 10), back) if t < 2.9 else lerp2((150, 10), (98, 40), ease(seg(t, 2.9, 3.2)))
    sal = ease(seg(t, 4.5, 4.8))
    lh = lerp2((-98, 40), (-70, -150), sal)
    hand = (ox + rh[0] * S, 1400 + (rh[1] - 175) * S)
    think = 3.3 < t < 4.4
    otto_full(c, ox, 1400, S, 'of', f, eyes='open', mouth='flat' if think else 'smile', look=(1, 0.2) if not think else (0.6, -0.9), lh=lh, rh=rh,
              tilt=0.08 if think else 0)
    # the acorn travels cub -> Otto -> punched -> cub
    if 0.5 < t < 1.5: acorn(c, lerp(cub_hand[0] - 30, hand[0] + 20, ease(seg(t, 1.2, 1.5))), lerp(cub_hand[1] - 20, hand[1] - 10, ease(seg(t, 1.2, 1.5))), 1.0)
    elif 1.5 <= t < 2.9:
        px, py = hand[0] + 20, hand[1] - 10
        acorn(c, px, py, 1.0 + 0.25 * math.sin(seg(t, 1.8, 2.1) * math.pi), punched=t > 1.95)
        if 1.9 < t < 2.3:
            q = seg(t, 1.9, 2.3)
            for k in range(6):
                a = k * math.pi / 3
                wline(c, [(px + math.cos(a) * (30 + 30 * q), py + math.sin(a) * (30 + 30 * q)), (px + math.cos(a) * (46 + 40 * q), py + math.sin(a) * (46 + 40 * q))],
                      ('pk', k), f, lw=6, col=GOLD, amp=0.5, a=1 - q)
    elif t >= 2.9 and not show:
        acorn(c, 752 - CS * 96 - 14, 1224 - CS * 150 - 16, 0.9, punched=True)
    c.restore()
    kd = eback(seg(t, 3.05, 3.4))
    if kd > 0.01: kid_drawing(c, 560, 560, kd * 1.0, f, rot=-0.04 + 0.02 * math.sin(g * 2))
    cap2(c, t, 0.2, ["No ticket."], y=215, size=84, t1=1.45)
    cap2(c, t, 1.5, ["Fare: one acorn."], y=215, size=84, gold=True, t1=2.95)
    cap2(c, t, 3.0, ["Stop requested: this hill."], y=215, size=80)


# ------------------------------------------------------------------ scene D 15-21: which hill
def scD(c, t, f, g):
    c.rectangle(0, 0, W, H); rgb(c, NAVY); c.fill()
    c.save(); c.translate(0, 120)
    country(c, f, g, 1250)
    sp = 560
    stop = ease(seg(t, 4.3, 5.0))
    cx = [540 + (t - 0.9) * sp, 540 + (t - 2.7) * sp, lerp(540 + (t - 4.55) * sp, 540, stop) if t < 5.0 else 540]
    kinds = ['mill', 'two', 'home']
    for i in range(3):
        if -500 < cx[i] < W + 500: hill(c, f, g, cx[i], 1250, kinds[i], 1.0)
    road(c, f, g, 1300, sp * (1 - stop))
    by = 1040 + (math.sin(g * 11) * 3) * (1 - stop)
    bus_ext(c, f, g, 270, by, 0.62, door=0.0, rot=g * 14 * (1 - stop), otto=('open', 'smile'), look=(-1, -0.4))
    c.save(); c.rectangle(270 + 0.62 * 194, by + 0.62 * 64, 0.62 * 112, 0.62 * 142); c.clip()
    fox(c, 270 + 0.62 * 250, by + 0.62 * 290, 0.27, 'cubw', f, face=-1, eyes='big', mouth='o' if t < 4.3 else 'grin', look=(-1, -0.6), scarf=CORAL)
    c.restore()
    reflect(c, g, 290, 780, 1396, n=4, depth=60)
    rain(c, g, 0.22)
    c.restore()
    kid_drawing(c, 850, 600, 0.56, f, rot=0.06)
    for i, tc in enumerate((0.9, 2.7)):
        badge(c, 300, 860, eback(seg(t, tc - 0.15, tc + 0.1)) * (1 - ein(seg(t, tc + 0.55, tc + 0.75))), False, f, key=('bx', i))
    badge(c, 300, 860, eback(seg(t, 4.9, 5.15)), True, f)
    cap2(c, t, 0.15, ["This hill?"], y=250, size=88, t1=1.95)
    cap2(c, t, 2.0, ["This one?"], y=250, size=88, t1=3.8)
    cap2(c, t, 4.6, ["That one."], y=250, size=96, gold=True)


# ------------------------------------------------------------------ scene E 21-26: home
def scE(c, t, f, g):
    c.save(); c.translate(540, 1300); c.scale(1.22, 1.22); c.translate(-560, -1250)
    country(c, f, g, 1340)
    hd = ease(seg(t, 0.2, 0.6))
    hill(c, f, g, 800, 1340, 'home', 1.15, door=hd)
    bus_ext(c, f, g, -330, 930, 0.8, door=1.0, otto=None)
    reflect(c, g, -300, 330, 1326, n=3, depth=50)
    S = 0.5
    sal = ease(seg(t, 3.9, 4.2))
    catch = ease(seg(t, 3.25, 3.6))
    rh = lerp2((98, 40), (120, -60), catch)
    otto_full(c, 320, 1352, S, 'of', f, eyes='closed' if t > 4.3 else 'open', mouth='smile', look=(1, 0.3), lh=lerp2((-98, 40), (-70, -150), sal), rh=rh,
              bob=math.sin(g * 3) * 2)
    # mother with lantern
    mx = 640
    lx, ly = mx - 76, 1352 - 92
    gl = cairo.RadialGradient(lx, ly, 6, lx, ly, 190)
    gl.add_color_stop_rgba(0, 1, 0.88, 0.5, 0.5); gl.add_color_stop_rgba(1, 1, 0.88, 0.5, 0)
    c.set_source(gl); c.rectangle(lx - 200, ly - 200, 400, 400); c.fill()
    hug = 1.55 < t < 3.0
    fox(c, mx, 1352, 0.62, 'mum', f, face=-1, eyes='closed' if hug else 'open', mouth='smile', look=(1, 0.2), scarf=TEAL, apron=True,
        wag=math.sin(g * 4) * 0.12, arms=((-56, -70), (122, -164) if not hug else (122, -164)))
    rrect(c, lx - 16, ly - 6, 32, 44, 8); fs(c, hx('FFD23D'), 5)
    wline(c, [(lx - 14, ly - 6), (lx, ly - 26), (lx + 14, ly - 6)], 'lan', f, lw=5, amp=0.4)
    # the cub runs home, hugs, then sends the drawing back
    if t < 1.55:
        u = seg(t, 0.35, 1.55); cxp = lerp(150, 560, u); hop = abs(math.sin(u * math.pi * 4)) * 34
        fox(c, cxp, 1352 - hop, 0.42, 'cub', f, face=1, eyes='big', mouth='grin', look=(1, -0.2), wag=math.sin(g * 14) * 0.3, arms=((-50, -200), (50, -200)))
    else:
        turn = t > 3.0
        fox(c, 566, 1352, 0.42, 'cub', f, face=-1 if turn else 1, eyes='closed' if hug else 'big', mouth='grin', look=(1, -0.2),
            wag=math.sin(g * 12) * 0.3, arms=((-30, -90), (64, -120) if hug else ((70, -210 + 10 * math.sin(g * 10)) if turn else (40, -80))))
        for i in range(3):
            q = seg(t, 1.7 + i * 0.3, 3.0 + i * 0.3)
            if 0 < q < 1: heart(c, 570 + i * 44, 1150 - 120 * q, 0.5 + 0.12 * i, CORAL, 1 - ein(q))
    # the drawing flies to Otto
    if 3.0 <= t < 3.6:
        u = seg(t, 3.0, 3.6)
        kid_drawing(c, lerp(540, 392, u), lerp(1220, 1235, u) - 150 * math.sin(u * math.pi), 0.2, f, rot=u * 6.0)
    elif t >= 3.6:
        kid_drawing(c, 392, 1235, 0.22, f, rot=0.1)
    rain(c, g, 0.2)
    c.restore()
    cap2(c, t, 2.6, ["Every passenger gets home."], y=250, size=78, gold=True)


# ------------------------------------------------------------------ scene F 26-30: the roof
def scF(c, t, f, g):
    thumps = [1.3, 1.85, 2.4]
    sh = 0
    for tp in thumps:
        if 0 <= t - tp < 0.22: sh = (1 - (t - tp) / 0.22) * 10 * math.sin((t - tp) * 90)
    zz = 1 + 0.05 * ease(seg(t, 1.3, 4.0))
    c.save(); c.translate(0, sh); c.translate(700, 720); c.scale(zz, zz); c.translate(-700, -720)
    alarmed = t > 1.3
    def head():
        if alarmed: otto_head(c, 150 + math.sin(g * 44) * 1.6, 935, 98, 'oh', f, eyes='wide', mouth='o', look=(0.3, -1.0))
        else: otto_head(c, 150 + math.sin(g * 4) * 5, 935, 98, 'oh', f, eyes='closed', mouth='smile', tilt=math.sin(g * 4) * 0.06)
    driver(c, f, g, head)
    if not alarmed:
        for k in range(3):
            ph = (g * 0.6 + k / 3) % 1
            x, y = 600 + k * 50 + ph * 60, 1010 - ph * 170
            c.new_path(); c.arc(x, y, 15, 0, 2 * math.pi); rgb(c, CREAMT, math.sin(ph * math.pi)); c.fill()
            c.new_path(); c.move_to(x + 13, y); c.line_to(x + 13, y - 52); c.line_to(x + 36, y - 44)
            c.set_line_width(6); rgb(c, CREAMT, math.sin(ph * math.pi)); c.stroke()
    # souvenirs pinned by the driver's seat
    kid_drawing(c, 196, 560, 0.52, f, rot=-0.07)
    c.save(); c.translate(330, 742); c.rotate(0.12)
    rrect(c, -44, -60, 88, 120, 10); fs(c, WHITE, 6)
    for k in range(3):
        c.rectangle(-28, -36 + k * 26, 56, 9); rgb(c, CORAL if k == 0 else hx('B9C0D6')); c.fill()
    c.new_path(); c.arc(0, -60, 9, 0, 2 * math.pi); fs(c, TEAL, 4)
    c.restore()
    # dents in the ceiling, walking forward
    for i, tp in enumerate(thumps):
        if t >= tp:
            k = eback(seg(t, tp, tp + 0.14)); dx = 820 - i * 250
            c.save(); c.translate(dx, 318); c.scale(1, k)
            c.new_path(); c.arc(0, 0, 86, 0, math.pi); c.close_path(); fs(c, CEIL, 8)
            c.new_path(); c.arc(0, 4, 54, 0.15 * math.pi, 0.85 * math.pi); rgb(c, INK, 0.35); c.set_line_width(6); c.stroke(); c.restore()
            q = seg(t, tp, tp + 0.5)
            if q < 1:
                for sg in (-1, 1):
                    wline(c, [(dx + sg * 110, 350 + 30 * q), (dx + sg * (130 + 20 * q), 380 + 60 * q)], ('dd', i, sg), f, lw=7, col=WHITE, amp=1.0, a=0.8 * (1 - q))
    # something peeks in, upside down, at the window
    pk = eout(seg(t, 2.9, 3.3))
    if pk > 0:
        c.save(); c.rectangle(752, 474, 400, 540); c.clip()
        c.save(); c.translate(930, 474 + 150 * pk - 150)
        c.new_path(); c.arc(0, 0, 150, 0, math.pi); c.close_path(); rgb(c, hx('05070F')); c.fill()
        blink = 3.6 < t < 3.72
        for sg in (-1, 1):
            c.save(); c.translate(sg * 58, 62); c.scale(1, 0.12 if blink else 1); c.new_path(); c.arc(0, 0, 30, 0, 2 * math.pi); c.restore()
            rgb(c, hx('FFE14D')); c.fill()
            c.save(); c.translate(sg * 58 - 8, 66); c.scale(1, 0.12 if blink else 1); c.new_path(); c.arc(0, 0, 13, 0, 2 * math.pi); c.restore()
            rgb(c, INK); c.fill()
        c.restore(); c.restore()
    c.restore()
    cap2(c, t, 2.55, ["Who is on the roof?"], y=250, size=88, gold=True)
    cap2(c, t, 3.2, ["Owl, cat or ghost? You pick."], y=362, size=72)


SCENES = [(0.0, 3.5, scA), (3.5, 9.5, scB), (9.5, 15.0, scC), (15.0, 21.0, scD), (21.0, 26.0, scE), (26.0, 30.0, scF)]


def draw(c, g, f):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= g < b or (i == len(SCENES) - 1 and g >= b):
            c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, g - a, f, g); c.restore()
            fa = 1 - seg(g - a, 0, 0.18)
            if i > 0 and fa > 0:
                c.rectangle(0, 0, W, H); rgb(c, NAVY, fa); c.fill()
            return
