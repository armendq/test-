from ep2 import *

OWL = hx('8A6A4A'); OWLD = hx('5E452E'); OWLL = hx('EBDcBE'.upper()) if False else hx('EBDCBE'); BARK = hx('5A4030'); BARKD = hx('3F2C20'); LEAF = hx('2F5A3C')


def owl(c, x, y, s, key, f, face=1, eyes='big', look=(0, 0), scarf=CORAL, bandage=True, sil=False, shiver=0.0, wing_up=0.0):
    """x, y = feet"""
    c.save(); c.translate(x + shiver, y); c.scale(s * face, s)
    if sil:
        rgb(c, hx('05070F'))
        c.new_path(); c.arc(0, -84, 74, 0, 2 * math.pi); c.fill()
        c.new_path(); c.arc(0, -176, 80, 0, 2 * math.pi); c.fill()
        for sg in (-1, 1):
            c.new_path(); c.move_to(sg * 30, -236); c.line_to(sg * 62, -290); c.line_to(sg * 74, -214); c.close_path(); c.fill()
            c.new_path(); c.arc(sg * 30, -180, 20, 0, 2 * math.pi); rgb(c, hx('FFE14D')); c.fill()
            c.new_path(); c.arc(sg * 30 + look[0] * 5, -180, 8, 0, 2 * math.pi); rgb(c, hx('05070F')); c.fill()
        c.restore(); return
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * 26, -4, 14, 0, 2 * math.pi); fs(c, ORANGE, 5)
    wcirc(c, 0, -84, 72, (key, 'b'), f, ry=84); fs(c, OWL, 8)
    c.save(); c.translate(0, -70); c.scale(1, 1.35); c.new_path(); c.arc(0, 0, 44, 0, 2 * math.pi); c.restore(); rgb(c, OWLL); c.fill()
    for k in range(3):
        for j in range(-1, 2):
            wline(c, [(j * 22 - 7, -96 + k * 26), (j * 22, -88 + k * 26), (j * 22 + 7, -96 + k * 26)], (key, 'v', k, j), f, lw=4, col=OWLD, amp=0.3)
    for sg in (-1, 1):
        c.save(); c.translate(sg * 70, -96); c.rotate(sg * (0.2 - (wing_up if sg == 1 else 0))); c.scale(0.5, 1.2)
        c.new_path(); c.arc(0, 0, 52, 0, 2 * math.pi); c.restore(); fs(c, OWLD, 7)
    if bandage:
        c.save(); c.translate(-70, -96); c.rotate(-0.2)
        rrect(c, -32, -18, 64, 36, 8); fs(c, WHITE, 5)
        c.rectangle(-4, -12, 8, 24); rgb(c, CORAL); c.fill(); c.rectangle(-12, -4, 24, 8); c.fill(); c.restore()
    if scarf:
        rrect(c, -56, -138, 112, 30, 14); fs(c, scarf, 6); rrect(c, 26, -128, 26, 60, 10); fs(c, scarf, 6)
    for sg in (-1, 1):
        c.new_path(); c.move_to(sg * 26, -238); c.line_to(sg * 60, -292); c.line_to(sg * 74, -216); c.close_path(); fs(c, OWL, 7)
    wcirc(c, 0, -178, 82, (key, 'h'), f, ry=76); fs(c, OWL, 8)
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * 32, -180, 36, 0, 2 * math.pi); rgb(c, OWLL); c.fill()
        if eyes == 'closed':
            c.new_path(); c.arc(sg * 32, -176, 16, 1.15 * math.pi, 1.85 * math.pi); rgb(c, INK); c.set_line_width(7); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        else:
            c.new_path(); c.arc(sg * 32, -180, 24, 0, 2 * math.pi); rgb(c, hx('FFD23D')); c.fill_preserve(); rgb(c, INK); c.set_line_width(5); c.stroke()
            c.new_path(); c.arc(sg * 32 + look[0] * 7, -180 + look[1] * 7, 12, 0, 2 * math.pi); rgb(c, INK); c.fill()
            c.new_path(); c.arc(sg * 32 + look[0] * 7 - 4, -185 + look[1] * 7, 4, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
    c.new_path(); c.move_to(-10, -160); c.line_to(10, -160); c.line_to(0, -140); c.close_path(); fs(c, ORANGE, 4)
    c.restore()


def feather(c, x, y, s, rot, f, key='fe'):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.save(); c.scale(0.34, 1.0); c.new_path(); c.arc(0, -50, 52, 0, 2 * math.pi); c.restore(); fs(c, OWLL, 5)
    wline(c, [(0, 10), (0, -100)], (key, 'q'), f, lw=5, col=OWLD, amp=0.3)
    c.restore()


def tree_card(c, x, y, k, f, rot=0.0):
    c.save(); c.translate(x, y); c.scale(k, k); c.rotate(rot)
    rrect(c, -142, -192, 300, 400, 16); rgb(c, INK, 0.3); c.fill()
    rrect(c, -150, -200, 300, 400, 16); fs(c, PAPER, 8)
    c.rectangle(-130, -180, 260, 360); rgb(c, hx('27326A')); c.fill()
    c.rectangle(-22, -120, 44, 300); rgb(c, BARK); c.fill()
    for k2, (yy, sg) in enumerate(((120, 1), (60, -1), (0, 1), (-60, -1))):
        wline(c, [(sg * 20, yy), (sg * 86, yy - 24)], ('tcb', k2), f, lw=14, col=BARK, amp=0.5)
    wcirc(c, 0, -130, 70, 'tcc', f, ry=48); rgb(c, hx('3F7650')); c.fill()
    c.new_path(); c.arc(0, -126, 20, 0, 2 * math.pi); rgb(c, hx('FFD98A')); c.fill()
    wline(c, [(96, 150), (96, -110)], 'tca', f, lw=9, col=CORAL, amp=0.5)
    wline(c, [(76, -84), (96, -116), (116, -84)], 'tcb2', f, lw=9, col=CORAL, amp=0.5)
    c.new_path(); c.arc(0, -200, 12, 0, 2 * math.pi); fs(c, TEAL, 5)
    c.restore()


def souvenirs(c, f):
    kid_drawing(c, 196, 560, 0.52, f, rot=-0.07)
    c.save(); c.translate(330, 742); c.rotate(0.12)
    rrect(c, -44, -60, 88, 120, 10); fs(c, WHITE, 6)
    for k in range(3):
        c.rectangle(-28, -36 + k * 26, 56, 9); rgb(c, CORAL if k == 0 else hx('B9C0D6')); c.fill()
    c.new_path(); c.arc(0, -60, 9, 0, 2 * math.pi); fs(c, TEAL, 4)
    c.restore()


# ------------------------------------------------------------------ scene A 0-3.4: something on the roof
def scA(c, t, f, g):
    sh = 0
    if 2.2 <= t < 2.6: sh = (1 - (t - 2.2) / 0.4) * 14 * math.sin((t - 2.2) * 80)
    zz = 1 + 0.05 * ease(seg(t, 0.0, 3.4))
    c.save(); c.translate(sh, 0); c.translate(700, 720); c.scale(zz, zz); c.translate(-700, -720)
    brake = ease(seg(t, 2.2, 2.4)) * (1 - ease(seg(t, 2.5, 2.9)))
    def head():
        otto_head(c, 150 + math.sin(g * 44) * 1.6 + 26 * brake, 935, 98, 'oh', f, eyes='wide', mouth='o', look=(0.3, -1.0) if t < 2.2 else (1, 0), tilt=0.12 * brake)
    driver(c, f, g, head, moving=1.0 if t < 2.3 else 0.0)
    souvenirs(c, f)
    for i in range(3):
        dx = 820 - i * 250
        c.new_path(); c.arc(dx, 318, 86, 0, math.pi); c.close_path(); fs(c, CEIL, 8)
        c.new_path(); c.arc(dx, 322, 54, 0.15 * math.pi, 0.85 * math.pi); rgb(c, INK, 0.35); c.set_line_width(6); c.stroke()
    pk = 1 - ease(seg(t, 1.3, 1.6))
    if pk > 0:
        c.save(); c.rectangle(752, 474, 400, 540); c.clip()
        c.save(); c.translate(930, 474 + 150 * pk - 150)
        c.new_path(); c.arc(0, 0, 150, 0, math.pi); c.close_path(); rgb(c, hx('05070F')); c.fill()
        blink = 0.6 < t < 0.72
        for sg in (-1, 1):
            c.save(); c.translate(sg * 58, 62); c.scale(1, 0.12 if blink else 1); c.new_path(); c.arc(0, 0, 30, 0, 2 * math.pi); c.restore()
            rgb(c, hx('FFE14D')); c.fill()
            c.save(); c.translate(sg * 58 - 8, 66); c.scale(1, 0.12 if blink else 1); c.new_path(); c.arc(0, 0, 13, 0, 2 * math.pi); c.restore()
            rgb(c, INK); c.fill()
        c.restore(); c.restore()
    c.restore()
    cap2(c, t, -1, ["Something is on the roof."], y=250, size=84, gold=True, t1=2.1)
    cap2(c, t, 2.15, ["Otto stops the bus."], y=250, size=84)


# ------------------------------------------------------------------ scene B 3.4-9.4: up the ladder
def ladder(c, f, x0, y0, x1, y1, key='ld'):
    for off in (-22, 22):
        wline(c, [(x0 + off, y0), (x1 + off, y1)], (key, off), f, lw=11, col=hx('C9A06A'), amp=0.5)
    n = 8
    for k in range(1, n):
        u = k / n; xx, yy = lerp(x0, x1, u), lerp(y0, y1, u)
        wline(c, [(xx - 22, yy), (xx + 22, yy)], (key, 'r', k), f, lw=9, col=hx('C9A06A'), amp=0.4)


def scB(c, t, f, g):
    c.rectangle(0, 0, W, H); rgb(c, NAVY); c.fill()
    c.save(); c.translate(540, 1240); c.scale(1.12, 1.12); c.translate(-520, -1180)
    country(c, f, g, 1380)
    road(c, f, g, 1392, 0)
    bus_ext(c, f, g, 90, 960, 0.8, door=1.0, otto=None)
    reflect(c, g, 120, 760, 1388, n=4, depth=50)
    ladder(c, f, 900, 1396, 812, 950)
    S = 0.5
    shown = t >= 2.9
    onhat = t >= 4.8
    if t < 1.0: ox, oy = lerp(1030, 906, ease(seg(t, 0.1, 1.0))), 1396
    elif t < 2.6:
        u = ease(seg(t, 1.0, 2.6)); ox, oy = lerp(906, 842, u), lerp(1396, 1130, u)
    elif t < 4.9: ox, oy = 842, 1130
    else:
        u = ease(seg(t, 4.9, 5.9)); ox, oy = lerp(842, 906, u), lerp(1130, 1396, u)
    climbing = (1.0 < t < 2.6) or (4.9 < t < 5.9)
    bob = abs(math.sin(g * 9)) * 6 if (t < 1.0 or climbing) else 0
    ow = (520, 962)
    if t < 4.2: op = ow
    elif t < 4.8:
        u = seg(t, 4.2, 4.8); hp = (ox, oy - 222); op = (lerp(ow[0], hp[0], u), lerp(ow[1], hp[1], u) - 150 * math.sin(u * math.pi))
    else: op = (ox, oy - 222 + bob * S)
    if shown and not onhat:
        gl = cairo.RadialGradient(op[0], op[1] - 80, 10, op[0], op[1] - 80, 240)
        gl.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.35); gl.add_color_stop_rgba(1, 1, 0.9, 0.6, 0)
        c.set_source(gl); c.rectangle(op[0] - 260, op[1] - 340, 520, 520); c.fill()
    if not onhat:
        owl(c, op[0], op[1], 0.5, 'owl', f, face=1, eyes='big', look=(1, 0.2), sil=not shown, shiver=math.sin(g * 40) * (2.5 if shown and t < 4.2 else 0))
    rh = (-110, -40) if 2.3 < t < 4.4 else ((98, 40) if not climbing else (98, -60 + 40 * math.sin(g * 9)))
    lh = (-98, 40) if not climbing else (-98, -60 - 40 * math.sin(g * 9))
    otto_full(c, ox, oy, S, 'of', f, eyes='wide' if 2.5 < t < 3.1 else 'open', mouth='o' if 2.5 < t < 3.1 else ('smile' if shown else 'flat'), look=(-1, -0.4), lh=lh, rh=rh, bob=bob)
    if onhat:
        owl(c, op[0], op[1], 0.42, 'owl', f, face=-1, eyes='big', look=(-1, 0.2))
    if 2.3 < t < 4.4:
        hand = (ox + rh[0] * S, oy + (rh[1] - 175) * S)
        torch(c, hand[0] - 14, hand[1], math.pi + 0.5, f)
        bx, by = hand[0] - 40, hand[1] - 22
        aim = math.atan2(ow[1] - 90 - by, ow[0] - bx); sp = 0.3; L = 700
        c.new_path(); c.move_to(bx, by); c.line_to(bx + L * math.cos(aim - sp), by + L * math.sin(aim - sp)); c.line_to(bx + L * math.cos(aim + sp), by + L * math.sin(aim + sp))
        c.close_path(); rgb(c, hx('FFE9A8'), 0.16 * ease(seg(t, 2.6, 2.9))); c.fill()
    rain(c, g, 0.25)
    c.restore()
    if 2.9 <= t < 3.02:
        c.rectangle(0, 0, W, H); rgb(c, WHITE, 0.3 * (1 - (t - 2.9) / 0.12)); c.fill()
    cap2(c, t, 0.2, ["Otto climbs up."], y=250, size=84, t1=2.85)
    cap2(c, t, 2.95, ["An owl. With a hurt wing."], y=250, size=80, gold=True)


# ------------------------------------------------------------------ scene C 9.4-14.6: fare and stop
def scC(c, t, f, g):
    S = 0.9; ox = 500
    c.save(); rear_cam(c)
    rear(c, f, g)
    for wx in (210, 500):
        rrect(c, wx, 610, 230, 320, 26); fs(c, hx('121A40'), 9)
        for k in range(6):
            yy = 620 + ((k * 0.17 + g * 0.5) % 1) * 290
            c.new_path(); c.move_to(wx + 25 + k * 36, yy); c.line_to(wx + 21 + k * 36, yy + 24); rgb(c, hx('BFD4FF'), 0.5); c.set_line_width(3); c.stroke()
    bench(c, f)
    give = ease(seg(t, 0.5, 1.0)); show = t > 2.6
    owl(c, 752, 1224, 0.62, 'owl', f, face=-1, eyes='big', look=(1, -0.3), wing_up=0.9 * give * (1 - ease(seg(t, 1.5, 1.9))))
    if t < 1.5: rh = lerp2((98, 40), (150, 0), ease(seg(t, 1.0, 1.5)))
    elif t < 2.2: rh = lerp2((150, 0), (40, -330), ease(seg(t, 1.5, 2.1)))
    else: rh = lerp2((40, -330), (98, 40), ease(seg(t, 2.2, 2.5)))
    gulp = 3.3 < t < 4.3
    sal = ease(seg(t, 4.4, 4.7))
    otto_full(c, ox, 1400, S, 'of', f, eyes='wide' if gulp else 'open', mouth='o' if gulp else 'smile', look=(1, 0.2) if not gulp else (0.6, -1.0),
              lh=lerp2((-98, 40), (-70, -150), sal), rh=rh)
    hand = (ox + rh[0] * S, 1400 + (rh[1] - 175) * S)
    if 0.5 < t < 1.2: feather(c, 752 - 0.62 * 78, 1224 - 0.62 * 150 - 30 * give, 0.7, -0.5, f)
    elif 1.2 <= t < 2.1: feather(c, lerp(704, hand[0], ease(seg(t, 1.2, 1.5))) if t < 1.5 else hand[0], lerp(1100, hand[1], ease(seg(t, 1.2, 1.5))) if t < 1.5 else hand[1], 0.7, -0.3, f)
    if t >= 2.1: feather(c, ox + 52, 1400 - 392 * S, 0.62, 0.5, f, key='capf')
    c.restore()
    kd = eback(seg(t, 2.65, 3.0))
    if kd > 0.01: tree_card(c, 560, 600, kd * 1.0, f, rot=-0.04 + 0.02 * math.sin(g * 2))
    cap2(c, t, 0.2, ["Fare: one feather."], y=215, size=84, gold=True, t1=2.5)
    cap2(c, t, 2.6, ["Stop requested: the very top."], y=215, size=80)


# ------------------------------------------------------------------ scene D 14.6-21: the climb
TOP = -2500


def tree(c, f, g, y0, y1):
    c.rectangle(430, y1 - 400, 220, y0 - y1 + 800); rgb(c, BARK); c.fill()
    wline(c, [(430, y0 + 300), (430, y1 - 400)], 'tl', f, lw=9, amp=0.6); wline(c, [(650, y0 + 300), (650, y1 - 400)], 'tr', f, lw=9, amp=0.6)
    k0 = int(math.floor(y1 / 320.0)) - 2; k1 = int(math.ceil(y0 / 320.0)) + 2
    for k in range(k0, k1):
        yy = k * 320 + 80
        if yy > 1300 or yy < TOP - 200: continue
        sg = 1 if k % 2 == 0 else -1
        x0 = 650 if sg == 1 else 430
        wline(c, [(x0, yy), (x0 + sg * 240, yy - 60), (x0 + sg * 420, yy - 40)], ('br', k), f, lw=34, col=INK, amp=0.8)
        wline(c, [(x0, yy), (x0 + sg * 240, yy - 60), (x0 + sg * 420, yy - 40)], ('br2', k), f, lw=22, col=BARK, amp=0.5)
        for j in range(3):
            wcirc(c, x0 + sg * (250 + j * 90), yy - 100 - (j % 2) * 40, 76, ('lf', k, j), f, ry=56); fs(c, LEAF, 7)
        for j in range(4):
            c.new_path(); c.arc(480 + ((k * 53 + j * 47) % 130), yy + 60 + j * 60, 16, 0.2, 2.2); rgb(c, BARKD); c.set_line_width(6); c.stroke()


def climb_y(t):
    if t < 1.9: return lerp(1320, 880, ease(seg(t, 0.2, 1.9)))
    if t < 3.7: return lerp(-200, -700, seg(t, 1.9, 3.7))
    return lerp(-1900, TOP + 330, eout(seg(t, 3.7, 6.1)))


def scD(c, t, f, g):
    oy = climb_y(t)
    cam = 1150 - oy
    bg(c, NAVY, hx('2A3470'))
    for (x, y, r, p) in STARS:
        yy = (y * 2.4 + cam * 0.12) % 1920
        c.new_path(); c.arc(x, yy, r, 0, 2 * math.pi); rgb(c, WHITE, 0.5); c.fill()
    my = 500 + cam * 0.05
    wcirc(c, 860, my, 90, 'moon', f, amp=1.5); rgb(c, hx('FFF3C4')); c.fill()
    c.new_path(); c.arc(894, my - 26, 80, 0, 2 * math.pi); rgb(c, hx('1A2250')); c.fill()
    c.save(); c.translate(540, 1150); c.scale(1.3, 1.3); c.translate(-540, -1150); c.translate(0, cam)
    if oy > 300:
        c.rectangle(-200, 1380, W + 400, 900); rgb(c, hx('1E3F2A')); c.fill()
        bus_ext(c, f, g, -160, 1090, 0.6, door=1.0, otto=None)
    tree(c, f, g, oy + 900, oy - 1300)
    tired = seg(t, 3.7, 6.1)
    rate = lerp(11, 5, tired)
    a = math.sin(g * rate)
    otto_full(c, 540, oy, 0.5, 'of', f, eyes='open' if tired < 0.3 else 'sleepy', mouth='smile' if t < 1.9 else ('flat' if tired < 0.3 else 'o'), look=(0, -1),
              lh=(-98, -120 - 70 * a), rh=(98, -120 + 70 * a), bob=abs(a) * 6)
    feather(c, 540 + 26, oy - 196, 0.34, 0.5, f, key='capf')
    owl(c, 540, oy - 222, 0.42, 'owl', f, face=1, eyes='big' if int(g * 2) % 5 else 'closed', look=(0, -1))
    if tired > 0.2:
        for k in range(3):
            ph = (g * 1.3 + k / 3) % 1
            c.new_path(); c.arc(470 - k * 14, oy - 200 + ph * 80, 6 * (1 - ph) + 3, 0, 2 * math.pi); rgb(c, hx('BFE4FF'), 0.9 * (1 - ph)); c.fill()
    c.restore()
    for tj in (1.9, 3.7):
        if 0 <= t - tj < 0.12:
            c.rectangle(0, 0, W, H); rgb(c, WHITE, 0.3 * (1 - (t - tj) / 0.12)); c.fill()
    cap2(c, t, 0.2, ["Branch 1."], y=250, size=88, t1=1.85)
    cap2(c, t, 1.95, ["Branch 12."], y=250, size=88, t1=3.65)
    cap2(c, t, 3.75, ["Branch 40."], y=250, size=96, gold=True)


# ------------------------------------------------------------------ scene E 21-26: the top
def scE(c, t, f, g):
    c.set_source(grad(0, 0, 0, H, [(0, hx('1A2250')), (0.6, hx('4A4488')), (1, hx('C98AA0'))])); c.rectangle(0, 0, W, H); c.fill()
    for (x, y, r, p) in STARS[:26]:
        c.new_path(); c.arc(x, y * 1.2, r, 0, 2 * math.pi); rgb(c, WHITE, 0.45); c.fill()
    wcirc(c, 210, 520, 120, 'moon', f, amp=2); rgb(c, hx('FFF3C4')); c.fill()
    c.rectangle(330, -100, 420, H + 200); rgb(c, BARK); c.fill()
    wline(c, [(330, -100), (330, H + 100)], 'tl', f, lw=10, amp=0.6); wline(c, [(750, -100), (750, H + 100)], 'tr', f, lw=10, amp=0.6)
    for j in range(8):
        c.new_path(); c.arc(380 + (j * 97) % 320, 300 + j * 190, 22, 0.2, 2.2); rgb(c, BARKD); c.set_line_width(7); c.stroke()
    wcirc(c, 540, 330, 330, 'crown', f, ry=170); fs(c, LEAF, 9)
    wcirc(c, 320, 420, 180, 'crown2', f, ry=120); fs(c, LEAF, 9); wcirc(c, 780, 430, 190, 'crown3', f, ry=120); fs(c, LEAF, 9)
    # the hollow
    gl = cairo.RadialGradient(540, 900, 20, 540, 900, 420)
    gl.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.55); gl.add_color_stop_rgba(1, 1, 0.85, 0.5, 0)
    c.set_source(gl); c.rectangle(100, 480, 880, 840); c.fill()
    wcirc(c, 540, 900, 180, 'hol', f, ry=215); fs(c, hx('FFD98A'), 10)
    c.save(); wcirc(c, 540, 900, 174, 'hol', f, ry=209); c.clip()
    hug = t > 1.25
    owl(c, 450, 1100, 0.6, 'dad', f, face=1, eyes='closed' if hug else 'big', look=(1, 0.3), scarf=TEAL, bandage=False)
    owl(c, 640, 1100, 0.6, 'mum', f, face=-1, eyes='closed' if hug else 'big', look=(1, 0.3), scarf=PINK, bandage=False)
    for k, bx in enumerate((500, 590)):
        owl(c, bx, 1118 + 4 * math.sin(g * 6 + k), 0.26, ('sib', k), f, face=1 if k == 0 else -1, eyes='big', look=(0, -0.5), scarf=None, bandage=False)
    c.restore()
    wcirc(c, 540, 900, 180, 'hol', f, ry=215); rgb(c, INK); c.set_line_width(10); c.stroke()
    # branch with Otto
    wline(c, [(750, 1380), (940, 1340), (1100, 1350)], 'ob', f, lw=46, col=INK, amp=0.8); wline(c, [(750, 1380), (940, 1340), (1100, 1350)], 'ob2', f, lw=32, col=BARK, amp=0.5)
    S = 0.56; ox, oy = 900, 1332
    rest = t > 1.4
    otto_full(c, ox, oy, S, 'of', f, eyes='sleepy' if not rest else ('closed' if t > 3.2 else 'open'), mouth='o' if not rest else 'smile', look=(-1, -0.3),
              lh=lerp2((-98, 40), (-70, -150), ease(seg(t, 3.6, 3.9))), rh=(98, 40), bob=math.sin(g * (7 if not rest else 3)) * 3, tilt=0.06 * math.sin(g * 5) * (0 if rest else 1))
    feather(c, ox + 29, oy - 392 * S + 174 * S, 0.38, 0.5, f, key='capf')
    if t < 0.5: owl(c, ox, oy - 248, 0.42, 'owl', f, face=-1, eyes='big', look=(-1, 0))
    elif t < 1.25:
        u = seg(t, 0.5, 1.25)
        owl(c, lerp(ox, 545, u), lerp(oy - 248, 1108, u) - 230 * math.sin(u * math.pi), 0.42, 'owl', f, face=-1, eyes='big', look=(-1, 0), wing_up=0.9 * math.sin(u * math.pi))
    else:
        owl(c, 545, 1108 - 8 * abs(math.sin(g * 7)), 0.42, 'owl', f, face=1, eyes='closed', look=(0, 0))
        for i in range(3):
            q = seg(t, 1.4 + i * 0.3, 2.8 + i * 0.3)
            if 0 < q < 1: heart(c, 480 + i * 70, 720 - 150 * q, 0.8 + 0.2 * i, CORAL, 1 - ein(q))
    cap2(c, t, 2.4, ["Every passenger gets home."], y=250, size=78, gold=True)


# ------------------------------------------------------------------ scene F 26-30: the bus leaves
def scF(c, t, f, g):
    c.rectangle(0, 0, W, H); rgb(c, NAVY); c.fill()
    c.save(); c.translate(540, 1240); c.scale(1.12, 1.12); c.translate(-520, -1180)
    country(c, f, g, 1380)
    road(c, f, g, 1392, 0)
    c.rectangle(930, 300, 300, 1100); rgb(c, BARK); c.fill(); wline(c, [(930, 300), (930, 1392)], 'tb', f, lw=9, amp=0.6)
    roll = ein(seg(t, 0.9, 4.0))
    bx = lerp(150, -520, roll)
    by = 960 + (math.sin(g * 13) * 3 if t > 0.5 else 0)
    bus_ext(c, f, g, bx, by, 0.8, door=0.0, otto=None, rot=-roll * 12)
    c.save(); c.rectangle(bx + 0.8 * 40, by + 0.8 * 64, 0.8 * 122, 0.8 * 142); c.clip()
    hx0, hy0 = bx + 0.8 * 102, by + 0.8 * 168
    c.new_path(); c.arc(hx0, hy0, 44, 0, 2 * math.pi); rgb(c, hx('05070F')); c.fill()
    c.new_path(); c.arc(hx0, hy0 - 26, 42, math.pi, 2 * math.pi); c.close_path(); rgb(c, UNID); c.fill()
    c.rectangle(hx0 - 44, hy0 - 32, 88, 9); rgb(c, GOLD); c.fill()
    for sg in (-1, 1):
        c.new_path(); c.arc(hx0 + sg * 16, hy0 + 2, 8, 0, 2 * math.pi); rgb(c, hx('FFE14D')); c.fill()
    c.restore()
    for k in range(4):
        ph = (g * 1.1 + k / 4) % 1
        c.new_path(); c.arc(bx + 720 + 90 * ph, by + 300 - 70 * ph, 16 + 26 * ph, 0, 2 * math.pi); rgb(c, hx('C9CFE6'), 0.5 * (1 - ph) * (1 if t > 0.5 else 0)); c.fill()
    for i, tb in enumerate((0.7, 1.15)):
        k = eback(seg(t, tb, tb + 0.2)) * (1 - ein(seg(t, tb + 0.5, tb + 0.7)))
        if k > 0.01:
            c.save(); c.translate(bx + 150 + i * 150, by - 110 - i * 50); c.scale(k, k); c.rotate(-0.1 + 0.2 * i)
            txt(c, "BEEP!", 0, 0, 70, GOLD, SERIF); c.restore()
    S = 0.55
    arrive = ease(seg(t, 0.2, 0.9))
    ox = lerp(1040, 820, arrive) if t < 1.6 else lerp(820, 560, seg(t, 1.6, 4.0))
    run = t > 1.6
    a = math.sin(g * 16)
    otto_full(c, ox, 1396, S, 'of', f, eyes='wide', mouth='o', look=(-1, -0.2), lh=(-110, -150 + (30 * a if run else 0)), rh=(60, -160 - (30 * a if run else 0)) if run else (98, 40),
              bob=abs(a) * 10 if run else 0, tilt=-0.1 if run else 0)
    feather(c, ox + 28, 1396 - 392 * S + 174 * S, 0.36, 0.5, f, key='capf')
    if 1.0 < t < 2.2: txt(c, "!", ox + 70, 1396 - 250, 100, GOLD, SERIF)
    rain(c, g, 0.22)
    c.restore()
    cap2(c, t, 2.2, ["Who is driving the bus?"], y=250, size=88, gold=True)
    cap2(c, t, 2.9, ["Hedgehog, ghost or mice? You pick."], y=362, size=68)


SCENES = [(0.0, 3.4, scA), (3.4, 9.4, scB), (9.4, 14.6, scC), (14.6, 21.0, scD), (21.0, 26.0, scE), (26.0, 30.0, scF)]


def draw(c, g, f):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= g < b or (i == len(SCENES) - 1 and g >= b):
            c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, g - a, f, g); c.restore()
            fa = 1 - seg(g - a, 0, 0.18)
            if i > 0 and fa > 0:
                c.rectangle(0, 0, W, H); rgb(c, NAVY, fa); c.fill()
            return
