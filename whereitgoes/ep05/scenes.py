from base2 import *

PAPER = hx('FFF7E6'); BOX = hx('3F7FE8'); BOXD = hx('2C5FC0'); SNOW = hx('F6FBFF'); SNOWD = hx('CADCF2'); IRON = hx('3A3F4F')
CR_R = hx('E23B3F'); CR_G = hx('2E9E5B'); CR_B = hx('3F7FE8'); CR_O = hx('B8672A'); CYAN = hx('6FE7FF'); MINT = hx('8CFFB0')
XCOL = [hx('FF5A5A'), hx('FFD23D'), hx('5BE38A'), hx('5AA8FF'), hx('FF9FE0')]


# ------------------------------------------------------------------ lettering and small parts
def crayon(c, s, x, y, size, cols, anchor='l', wob=1.0, seed=7):
    """wobbly crayon letters. x, y = baseline start (or centre with anchor='c')"""
    c.select_font_face(HAND, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD); c.set_font_size(size)
    if anchor == 'c': x -= c.text_extents(s)[4] / 2
    r = random.Random(seed + len(s) * 131)
    c.set_line_join(cairo.LINE_JOIN_ROUND)
    for i, ch in enumerate(s):
        adv = c.text_extents(ch)[4]; dy = r.uniform(-2.5, 2.5) * wob * size / 40; da = r.uniform(-0.1, 0.1) * wob
        if ch != ' ':
            c.save(); c.translate(x + adv / 2, y + dy); c.rotate(da)
            rgb(c, cols[i % len(cols)]); c.new_path(); c.move_to(-adv / 2, 0); c.text_path(ch); c.fill_preserve()
            c.set_line_width(size * 0.05); c.stroke(); c.restore()
        x += adv
    c.new_path(); c.select_font_face(CAP)


def fit(c, s, x, y, size, maxw, col, font=CAP, a=1.0):
    w = tw(c, s, size, font)
    if w > maxw: size *= maxw / w
    txt(c, s, x, y, size, col, font, a=a)


def hero(c, x, y, s, key, f, face='smile', eyes='dot', rot=0.0, look=(0, 0), sq=1.0, flap=0.0, adopted=0.0):
    """the letter to Santa. x, y = centre of the envelope"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    if flap > 0.02:
        wpoly(c, [(-142, -90), (0, -90 - 150 * flap), (142, -90)], (key, 'flp'), f, 1.0); fs(c, hx('FFEBC8'), 9)
    rrect(c, -150, -100, 300, 200, 18); rgb(c, WHITE); c.fill()
    c.save(); rrect(c, -150, -100, 300, 200, 18); c.clip(); rgb(c, CR_R)
    for k in range(-2, 20):
        x0 = -150 + k * 30
        c.new_path(); c.move_to(x0, -100); c.line_to(x0 + 15, -100); c.line_to(x0 + 15 - 200, 100); c.line_to(x0 - 200, 100); c.close_path(); c.fill()
    c.restore()
    rrect(c, -136, -86, 272, 172, 9); rgb(c, PAPER); c.fill()
    rrect(c, -150, -100, 300, 200, 18); rgb(c, INK); c.set_line_width(10); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    if flap <= 0.02:
        wline(c, [(-134, -84), (0, -4), (134, -84)], (key, 'fl'), f, lw=5, col=INK, amp=0.6, a=0.14)
    rrect(c, 78, -78, 46, 54, 6); fs(c, CR_G, 5); sparkle(c, 101, -51, 15, WHITE)
    crayon(c, "SANTA", -126, -37, 46, [CR_R])
    crayon(c, "NORTH POLE", -126, 80, 21, [CR_G], seed=3)
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * 47, 36, 10, 0, 2 * math.pi); rgb(c, PINK, 0.55); c.fill()
    facef(c, 0, 14, 64, face, look, eyes)
    if adopted > 0.01:
        c.save(); c.translate(54, 70); c.rotate(-0.12); c.scale(adopted, adopted)
        rrect(c, -86, -25, 172, 50, 8); rgb(c, PAPER, 0.9); c.fill_preserve(); rgb(c, CR_R); c.set_line_width(6); c.stroke()
        txt(c, "ADOPTED", 0, 12, 31, CR_R)
        c.restore()
    c.restore()


def mlet(c, x, y, s, rot=0.0, col=PAPER, face=None, look=(0, 0)):
    """a small plain letter"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rrect(c, -50, -34, 100, 68, 8); rgb(c, col); c.fill_preserve(); rgb(c, INK); c.set_line_width(5); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    c.new_path(); c.move_to(-46, -30); c.line_to(0, 2); c.line_to(46, -30); rgb(c, INK, 0.28); c.set_line_width(3.5); c.stroke()
    c.rectangle(27, -27, 14, 16); rgb(c, CR_R); c.fill()
    if face:
        for sg in (-1, 1):
            c.new_path(); c.arc(sg * 13 + look[0] * 3, 8 + look[1] * 3, 4.6, 0, 2 * math.pi); rgb(c, INK); c.fill()
        c.set_line_cap(cairo.LINE_CAP_ROUND); rgb(c, INK); c.set_line_width(4)
        if face == 'smile':
            c.new_path(); c.arc(0, 15, 9, math.radians(25), math.radians(155)); c.stroke()
        else:
            c.new_path(); c.arc(0, 21, 4.5, 0, 2 * math.pi); c.fill()
    c.restore()


def xlights(c, x0, y0, x1, y1, g, n=9, sag=40, key=0, r=13):
    pts = []
    for i in range(n + 1):
        u = i / n; pts.append((lerp(x0, x1, u), lerp(y0, y1, u) + sag * 4 * u * (1 - u)))
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    rgb(c, INK, 0.8); c.set_line_width(4); c.stroke()
    for i, (x, y) in enumerate(pts[1:-1]):
        col = XCOL[(i + key) % len(XCOL)]; on = 0.55 + 0.45 * math.sin(g * 7 + i * 2.1 + key)
        gl = cairo.RadialGradient(x, y + 10, 2, x, y + 10, r * 3.2)
        gl.add_color_stop_rgba(0, col[0], col[1], col[2], 0.5 * on); gl.add_color_stop_rgba(1, col[0], col[1], col[2], 0)
        c.set_source(gl); c.rectangle(x - r * 3.2, y + 10 - r * 3.2, r * 6.4, r * 6.4); c.fill()
        c.save(); c.translate(x, y + 10); c.scale(0.8, 1.15); c.new_path(); c.arc(0, 0, r, 0, 2 * math.pi); c.restore()
        rgb(c, col); c.fill_preserve(); rgb(c, INK); c.set_line_width(3.5); c.stroke()


def snowfall(c, g, n=40, seed=4, a=0.95):
    r = random.Random(seed)
    for i in range(n):
        bx = r.uniform(0, W); by = r.uniform(0, H); sp = r.uniform(120, 260); sz = r.uniform(5, 12); ph = r.uniform(0, 6.28)
        y = (by + g * sp) % (H + 40) - 20; x = bx + 26 * math.sin(g * 1.3 + ph)
        c.new_path(); c.arc(x, y, sz, 0, 2 * math.pi); rgb(c, WHITE, a * (0.55 + 0.45 * sz / 12)); c.fill()


def sweat(c, x, y, s, g, f, n=4, a0=-2.75, da=0.5):
    for i in range(n):
        ph = (g * 2.4 + i / n) % 1
        ang = a0 + i * da; rr = (150 + 95 * ph) * s
        wcirc(c, x + math.cos(ang) * rr * 0.72, y + math.sin(ang) * rr * 0.6, (15 - 9 * ph) * s, ('sw', i), f, amp=1); fs(c, hx('8FD9FA'), 4)


def kid(c, x, y, s, key, f, lh, rh, lf=(-45, 190), rf=(45, 190), face='smile', eyes='dot', look=(0, 0), bob=0.0, coat=GREEN, legs=True):
    """a small child in a beanie and mittens. x, y = hip"""
    hd = stick(c, x, y, s, key, f, lh=lh, rh=rh, lf=lf, rf=rf, face=face, eyes=eyes, shirt=coat, look=look, bob=bob, legs=legs)
    for hnd in (lh, rh):
        c.new_path(); c.arc(x + hnd[0] * s, y + hnd[1] * s, 16 * s, 0, 2 * math.pi); fs(c, CORAL, 6 * s)
    px, py, hr = hd
    c.new_path(); c.arc(px, py - hr * 0.22, hr * 1.05, math.pi, 2 * math.pi); c.close_path(); fs(c, CORAL, 8 * s)
    rrect(c, px - hr * 1.12, py - hr * 0.4, hr * 2.24, hr * 0.36, hr * 0.16); fs(c, WHITE, 7 * s)
    c.new_path(); c.arc(px, py - hr * 1.34, hr * 0.3, 0, 2 * math.pi); fs(c, WHITE, 7 * s)
    return hd


def monitor(c, f, x, y, w, h, key='mon'):
    wline(c, [(x + w / 2, y + h), (x + w / 2, y + h + 60)], (key, 's'), f, lw=18, col=STEELD, amp=0.6)
    rrect(c, x, y, w, h, 28); fs(c, IRON, 10)
    rrect(c, x + 22, y + 22, w - 44, h - 44, 16); rgb(c, hx('0B1430')); c.fill()


def tickbadge(c, x, y, k, f, key='tk', r=54):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k); c.new_path(); c.arc(0, 0, r, 0, 2 * math.pi); fs(c, GREEN, 8)
    wline(c, [(-r * 0.44, r * 0.04), (-r * 0.13, r * 0.37), (r * 0.48, -r * 0.33)], key, f, lw=r * 0.24, col=WHITE, amp=0.5); c.restore()


def strip(c, y, lines, k, size=40, w=None):
    if k <= 0: return
    c.select_font_face(HAND); c.set_font_size(size)
    ww = (w or max(c.text_extents(s)[4] for s in lines) + 70); hh = len(lines) * size * 1.5 + 14
    c.save(); c.translate(540, y)
    rrect(c, -ww / 2, -hh / 2, ww, hh, 22); rgb(c, INK, 0.88 * k); c.fill()
    for i, s in enumerate(lines):
        txt(c, s, 0, -hh / 2 + size * 1.22 + i * size * 1.5, size, CREAM, HAND, a=k)
    c.restore()


# ------------------------------------------------------------------ scene 1: the drop, on a snowy evening
HOUSES1 = ((40, 300, 420, hx('7868A8')), (330, 260, 520, hx('8E6FA3')), (590, 330, 400, hx('6C78B4')), (900, 240, 480, hx('7868A8')))
KID = (392, 1380 - 137); SLOT = (700, 1040)


def wstreet(c, f, g):
    c.set_source(grad(0, 0, 0, 1380, [(0, hx('1D2760')), (0.55, hx('5B4E98')), (1.0, hx('F5A88C'))])); c.rectangle(0, 0, W, H); c.fill()
    r = random.Random(9)
    for i in range(26):
        x = r.uniform(0, W); y = r.uniform(520, 980); tw_ = 0.5 + 0.5 * math.sin(g * 3 + i)
        sparkle(c, x, y, 5 + 5 * tw_, WHITE, 0.35 + 0.5 * tw_)
    for i, (x, w, h, col) in enumerate(HOUSES1):
        wrect(c, x, 1380 - h, w, h, ('hs', i), f); fs(c, col, 8)
        for k in range(2):
            wx = x + 40 + k * (w - 150); wy = 1380 - h + 96
            gl = cairo.RadialGradient(wx + 35, wy + 45, 20, wx + 35, wy + 45, 130)
            gl.add_color_stop_rgba(0, 1, 0.9, 0.55, 0.45); gl.add_color_stop_rgba(1, 1, 0.9, 0.55, 0)
            c.set_source(gl); c.rectangle(wx - 100, wy - 90, 270, 270); c.fill()
            rrect(c, wx, wy, 70, 90, 10); fs(c, hx('FFE28A'), 6)
        wpoly(c, [(x - 16, 1380 - h), (x + w / 2, 1380 - h - 120), (x + w + 16, 1380 - h)], ('rf', i), f); fs(c, SNOW, 8)
        xlights(c, x - 4, 1380 - h + 10, x + w + 4, 1380 - h + 10, g, n=max(5, int(w / 46)), sag=22, key=i)
    c.rectangle(0, 1380, W, H - 1380); c.set_source(grad(0, 1380, 0, H, [(0, SNOW), (1, SNOWD)])); c.fill()
    for (x, rr) in ((130, 120), (960, 150), (560, 90)):
        c.save(); c.translate(x, 1384); c.scale(1, 0.3); c.new_path(); c.arc(0, 0, rr, math.pi, 2 * math.pi); c.restore(); rgb(c, SNOW); c.fill()
    wline(c, [(0, 1380), (W, 1380)], 'kerb', f, lw=7, amp=0.8, a=0.7)


def mailbox(c, f, x, y, key='mb', gape=None, gulp=0.0, cap=(0, 0, 0.0)):
    c.save(); c.translate(x, y); c.scale(1 + 0.06 * gulp, 1 - 0.06 * gulp); c.translate(-x, -y)
    wline(c, [(x - 60, y), (x - 60, y - 60)], (key, 'l1'), f, lw=20, col=BOXD, amp=0.6); wline(c, [(x + 60, y), (x + 60, y - 60)], (key, 'l2'), f, lw=20, col=BOXD, amp=0.6)
    c.new_path(); c.move_to(x - 120, y - 50); c.line_to(x - 120, y - 330); c.arc(x, y - 330, 120, math.pi, 2 * math.pi); c.line_to(x + 120, y - 50); c.close_path()
    fs(c, BOX, 10)
    if gape is not None:
        rrect(c, x - 90, y - 356 - gape / 2, 180, 34 + gape, 16); fs(c, hx('10172B'), 6)
    else:
        rrect(c, x - 84, y - 356, 168, 34, 12); fs(c, hx('10172B'), 6)
    rrect(c, x - 70, y - 270, 140, 74, 12); fs(c, WHITE, 6); txt(c, "MAIL", x, y - 214, 50, BOXD)
    c.restore()
    if cap is not None:
        c.save(); c.translate(x + cap[0], y - 330 + cap[1]); c.rotate(cap[2]); c.set_line_cap(cairo.LINE_CAP_ROUND)
        for lw, col in ((40, INK), (26, SNOW)):
            c.new_path(); c.arc(0, 0, 124, math.pi * 1.14, math.pi * 1.86); rgb(c, col); c.set_line_width(lw); c.stroke()
        c.restore()


def scene1(c, t, f, g):
    tip = 16 * (1 - seg(t, 2.25, 2.4))
    hip = (KID[0], KID[1] - tip)
    hand0 = (hip[0] + 150 * 0.72, hip[1] - 292 * 0.72)
    drop = ease(seg(t, 1.35, 2.2))
    px = lerp(hand0[0] + 40, SLOT[0], drop); py = lerp(hand0[1] - 112, SLOT[1], drop) - 150 * math.sin(drop * math.pi)
    k = ease(seg(t, 0.6, 1.3)); z = lerp(2.0, 1.42, k)
    fx, fy = lerp((px + SLOT[0]) / 2 + 10, 560, k), lerp((py + SLOT[1]) / 2 - 10, 1080, k)
    fear = 1 - seg(t, 1.2, 1.35)
    jx = 5 * math.sin(g * 41) * fear; jy = 4 * math.sin(g * 53 + 1) * fear
    es = lerp(0.84, 0.62, k)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)
    wstreet(c, f, g)
    gulp = math.sin(clamp(seg(t, 2.2, 2.55)) * math.pi)
    cu = seg(t, 2.75, 3.2)
    mailbox(c, f, 700, 1380, gape=(12 + 14 * abs(math.sin(g * 5))) if t < 1.35 else None, gulp=gulp, cap=None)
    startled = t >= 3.0
    jump = 26 * abs(math.sin((t - 2.4) * 9)) * (1 - seg(t, 2.75, 2.9)) if t >= 2.4 else 0
    push = math.sin(clamp(seg(t, 1.3, 1.7)) * math.pi)
    if t < 2.4: lh, rh, face, eyes, look = (-60, -20), (150 + 40 * push, -292 + 20 * push), 'smile', 'dot', (1, -0.6)
    elif not startled: lh, rh, face, eyes, look = (-96, -285), (96, -290), 'grin', 'closed', (1, -0.3)
    else: lh, rh, face, eyes, look = (-80, -150), (100, -160), 'o', 'big', (1, 0.5)
    kid(c, hip[0], hip[1] - jump, 0.72, 'kid', f, lh=lh, rh=rh, face=face, eyes=eyes, look=look, bob=math.sin(g * 3) * 2)
    if drop < 1:
        if fear > 0.05:
            sweat(c, px + jx, py + jy, es * 1.3, g, f, n=5, a0=-2.95, da=0.4)
            for i in range(3):          # it is being pulled toward the slot
                ph = (g * 3.0 + i / 3) % 1
                x0 = lerp(px + 110, SLOT[0] - 30, ph); y0 = lerp(py + 96, SLOT[1] - 30, ph) + (i - 1) * 16
                wline(c, [(x0, y0), (x0 + 26, y0 + 14)], ('pull', i), f, lw=7, col=WHITE, amp=0.8, a=0.9 * math.sin(ph * math.pi) * fear)
        hero(c, px + jx, py + jy, es * (1 - 0.35 * ein(seg(drop, 0.8, 1.0))), 'hero', f, face='o', eyes='big',
             rot=0.11 * math.sin(g * 30) * fear + 0.1 * math.sin(g * 7) * (1 - fear) + drop * 0.5, look=(1, 0.7))
    if drop > 0.85:
        rrect(c, 616, 1024, 168, 34, 12); rgb(c, hx('10172B')); c.fill()
    # the snow cap sits on top, then slides off
    if cu <= 0: mailbox_cap(c, 700, 1380, (0, 0, 0.0))
    elif cu < 1:                                   # it comes down as one lump
        lx_, ly_ = lerp(640, 505, cu), lerp(940, 1356, cu * cu)
        mailbox_cap(c, 700, 1380, (0, 0, 0.0)) if cu < 0.12 else None
        for i, (dx, dy, rr) in enumerate(((-30, 6, 30), (26, 10, 26), (0, -12, 36))):
            a_ = cu * 5 + i * 2.1
            wcirc(c, lx_ + dx * math.cos(a_) - dy * math.sin(a_), ly_ + dx * math.sin(a_) + dy * math.cos(a_), rr, ('lump', i), f, amp=2); fs(c, SNOW, 6)
    else:
        q = t - 3.2
        for i in range(6):
            sgn = -1 if i < 3 else 1; d_ = 30 + (i % 3) * 26 + 150 * q
            wcirc(c, 505 + sgn * d_, 1372 - (i % 3) * 12 - 60 * q, max(3, 22 * (1 - q / 0.4)), ('pf1', i), f, amp=2); rgb(c, WHITE, clamp(1 - q / 0.4)); c.fill()
        c.save(); c.translate(505, 1384); c.scale(1, 0.34); c.new_path(); c.arc(0, 0, 76, math.pi, 2 * math.pi); c.restore(); fs(c, SNOW, 6)
    if 2.2 < t < 2.6:
        for i in range(3):
            q = seg(t, 2.2 + i * 0.06, 2.6)
            c.new_path(); c.arc(700, 1010 - 90 * q - i * 26, 10 + 6 * i, 0, 2 * math.pi); rgb(c, WHITE, 0.8 * (1 - q)); c.set_line_width(5); c.stroke()
    c.restore()
    snowfall(c, g, n=38)
    caption(c, t, -1, [[("WHERE DOES YOUR KID'S", CREAM)], [("LETTER TO SANTA GO?", GOLD)]], y=300, size=92, pop=False)


def mailbox_cap(c, x, y, cap):
    c.save(); c.translate(x + cap[0], y - 330 + cap[1]); c.rotate(cap[2]); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for lw, col in ((40, INK), (26, SNOW)):
        c.new_path(); c.arc(0, 0, 124, math.pi * 1.14, math.pi * 1.86); rgb(c, col); c.set_line_width(lw); c.stroke()
    c.restore()


# ------------------------------------------------------------------ scene 2: Santa has a real address
def scene2(c, t, f, g):
    boh(c, f, g)
    stop = 0.9 <= t < 3.55; reading = 0.9 <= t < 2.35; found = t >= 2.35
    if t < 3.55: bx = lerp(-230, 540, eout(seg(t, 0.0, 0.9)))
    else: bx = lerp(540, 1360, ein(seg(t, 3.55, 4.3)))
    c.save(); c.translate(0, 60)
    belt(c, -80, W + 80, 1300, g, f, sp=0 if stop else 640)
    for k in range(3):
        mx = bx - 450 - k * 300
        if mx > -80: mlet(c, mx, 1300 - 36, 1.05, rot=0.04 * math.sin(g * 5 + k))
    hop = 46 * math.sin(clamp(seg(t, 2.4, 2.8)) * math.pi)
    if t < 0.9: face, eyes, look = 'o', 'big', (1, 0)
    elif reading: face, eyes, look = 'flat', 'big', (0.2 * math.sin(g * 6), -1)
    elif t < 3.55: face, eyes, look = 'grin', ('closed' if 2.9 < t < 3.3 else 'dot'), (0, -1)
    else: face, eyes, look = 'o', 'big', (1, 0)
    if reading: sweat(c, bx, 1300 - 100, 0.95, g, f, n=3, a0=-2.6, da=0.5)
    if t >= 3.55:
        for k in range(4):
            yy = 1150 - k * 36 + math.sin(g * 9 + k) * 5
            wline(c, [(bx - 360 - (k % 2) * 70, yy), (bx - 190, yy)], ('sl2', k), f, lw=8, col=WHITE, amp=1.0, a=0.85)
    hero(c, bx + (3 * math.sin(g * 40) if reading else 0), 1300 - 100 - hop, 1.0, 'hero', f, face=face, eyes=eyes, look=look,
         rot=0.03 * math.sin(g * 9) + (-0.1 if t >= 3.55 else 0))
    # the camera
    wline(c, [(540, 620), (540, 900)], 'cam1', f, lw=22, col=STEELD, amp=0.6)
    rrect(c, 430, 880, 220, 130, 26); fs(c, STEEL, 10)
    lx = clamp((bx - 540) / 500, -1, 1) * 22
    c.new_path(); c.arc(540 + lx, 965, 46, 0, 2 * math.pi); fs(c, hx('10172B'), 8)
    love = eback(seg(t, 3.1, 3.3))
    if love > 0.01: heart(c, 540 + lx, 962, 0.72 * love * (1 + 0.08 * math.sin(g * 14)), CORAL)
    else:
        c.new_path(); c.arc(540 + lx, 965, 20 * (0.55 + 0.25 * math.sin(g * 16) if reading else 1), 0, 2 * math.pi); rgb(c, CYAN); c.fill()
    if 0.5 < t < 3.55:
        for dx in (-70, 0, 70):
            c.new_path(); c.move_to(540 + lx, 1012); c.line_to(bx + dx * 1.3, 1196); rgb(c, CYAN, 0.28 if reading else 0.14); c.set_line_width(4); c.stroke()
    c.restore()
    # the monitor
    monitor(c, f, 240, 560, 600, 300)
    c.save(); rrect(c, 262, 582, 556, 256, 16); c.clip()
    if t < 0.9:
        for k in range(3):
            c.new_path(); c.arc(480 + k * 60, 710, 12 + 5 * math.sin(g * 8 - k), 0, 2 * math.pi); rgb(c, CYAN, 0.7); c.fill()
    elif not found:
        kk = eout(seg(t, 0.9, 1.1))
        c.save(); c.translate(540, 742); c.scale(kk, kk); crayon(c, "SANTA", 0, 0, 104, [CYAN], anchor='c', wob=1.4 + 0.5 * math.sin(g * 20)); c.restore()
        sx = 262 + 556 * (((t - 0.9) * 1.25) % 1.0)
        c.rectangle(sx - 5, 582, 10, 256); rgb(c, hx('B8F4FF'), 0.85); c.fill()
        q = seg(t, 1.15, 2.3)
        rrect(c, 330, 792, 420, 22, 11); rgb(c, WHITE, 0.2); c.fill()
        rrect(c, 330, 792, max(22, 420 * q), 22, 11); rgb(c, GOLD); c.fill()
    else:
        for i, (s_, yy, sz, col) in enumerate((("SANTA CLAUS", 652, 46, CYAN), ("123 ELF ROAD", 728, 64, MINT), ("NORTH POLE 88888", 800, 50, MINT))):
            kk = eback(seg(t, 2.35 + i * 0.08, 2.6 + i * 0.08))
            if kk > 0.01:
                c.save(); c.translate(540, yy - sz * 0.35); c.scale(kk, kk); fit(c, s_, 0, sz * 0.35, sz, 510, col); c.restore()
    for yy in range(590, 838, 12):
        c.rectangle(262, yy, 556, 2); rgb(c, WHITE, 0.05); c.fill()
    c.restore()
    qk = eback(seg(t, 1.2, 1.45)) * (1 - ein(seg(t, 2.2, 2.33)))
    if qk > 0.01:
        c.save(); c.translate(826, 580); c.scale(qk, qk); c.new_path(); c.arc(0, 0, 56, 0, 2 * math.pi); fs(c, hx('FF4D4D'), 8)
        txt(c, "?", 0, 30, 82, WHITE); c.restore()
    tickbadge(c, 826, 580, eback(seg(t, 2.5, 2.75)), f, 'tk2')
    caption(c, t, 0.25, [[("SANTA HAS A REAL", CREAM)], [("MAILING ADDRESS.", GOLD)]], y=300, size=92, t1=2.3)
    caption(c, t, 2.35, [[("123 ELF ROAD,", GOLD)], [("NORTH POLE 88888.", GOLD)]], y=300, size=92)


# ------------------------------------------------------------------ scene 3: before 1912, the Dead Letter Office
def stove(c, f, g, x, y, shut=False):
    """x = centre, y = the floor"""
    pts = [(x, y - 400), (x, y - 640), (W + 60, y - 640)]
    wline(c, pts, 'pipe', f, lw=60, col=INK, amp=0.5); wline(c, pts, 'pipe2', f, lw=44, col=hx('4A4F5E'), amp=0.3)
    for sg in (-1, 1): wline(c, [(x + sg * 76, y - 70), (x + sg * 104, y)], ('stl', sg), f, lw=20, col=INK, amp=0.5)
    wcirc(c, x, y - 235, 150, 'stb', f, amp=2, ry=182); fs(c, hx('3A3F4F'), 10)
    rrect(c, x - 112, y - 432, 224, 38, 12); fs(c, hx('4A4F5E'), 8)
    rrect(c, x - 134, y - 84, 268, 32, 10); fs(c, hx('4A4F5E'), 8)
    rrect(c, x - 80, y - 306, 160, 156, 22); fs(c, hx('15100E'), 8)
    if shut:
        rrect(c, x - 84, y - 310, 168, 164, 22); fs(c, hx('4A4F5E'), 9)
        c.new_path(); c.arc(x + 54, y - 228, 13, 0, 2 * math.pi); fs(c, hx('8A8F9E'), 5)
    else:
        rrect(c, x + 80, y - 310, 26, 164, 10); fs(c, hx('4A4F5E'), 8)


def flames(c, x, y, s, g, power=1.0):
    for i, (dx, hgt, w0, col) in enumerate(((-36, 84, 38, hx('FF6A2E')), (32, 100, 36, hx('FF8A3D')), (0, 124, 34, hx('FFC83D')), (0, 64, 22, hx('FFF0A8')))):
        hh = hgt * s * power * (0.8 + 0.25 * math.sin(g * 17 + i * 2)); w = w0 * s
        cx = x + dx * s + 5 * math.sin(g * 13 + i); tipx = cx + 10 * math.sin(g * 9 + i)
        c.new_path(); c.move_to(cx - w, y); c.curve_to(cx - w, y - hh * 0.5, cx - w * 0.2, y - hh * 0.6, tipx, y - hh)
        c.curve_to(cx + w * 0.2, y - hh * 0.6, cx + w, y - hh * 0.5, cx + w, y); c.close_path(); rgb(c, col); c.fill()


TOSS = (0.45, 0.95, 1.45, 1.95, 2.45)
SX, SFL = 815, 1460          # the stove


def scene3(c, t, f, g):
    slam = t >= 3.55; q = t - 3.55
    shake = 9 * math.exp(-9 * q) * math.sin(q * 70) if slam and q < 0.5 else 0
    bg(c, hx('EFE1C6'), hx('DCC7A2'))
    c.save(); c.translate(shake, 0)
    for i in range(8):
        c.rectangle(-20 + i * 150, 500, 74, 960); rgb(c, hx('E3D2B2'), 0.6); c.fill()
    c.rectangle(-40, SFL, W + 80, H - SFL); c.set_source(grad(0, SFL, 0, H, [(0, hx('A9825A')), (1, hx('8A6746'))])); c.fill()
    wline(c, [(-40, SFL), (W + 40, SFL)], 'f3', f, lw=7, amp=0.8)
    # pigeonholes full of letters
    rrect(c, 84, 606, 452, 356, 12); fs(c, WOODD, 9)
    rr = random.Random(31)
    for j in range(3):
        for i in range(4):
            x0, y0 = 98 + i * 108, 692 + j * 88
            rrect(c, x0, y0, 96, 78, 6); rgb(c, hx('5A3B25')); c.fill()
            for m in range(rr.choice((1, 2, 2, 3))):
                mlet(c, x0 + 30 + m * 20, y0 + 50 - (m % 2) * 6, 0.52, rot=rr.uniform(-0.5, 0.5), col=hx('F3E7CF'))
    rrect(c, 104, 618, 412, 62, 10); fs(c, hx('F3E2C3'), 6); txt(c, "DEAD LETTERS", 310, 666, 44, INK)
    stove(c, f, g, SX, SFL, shut=slam)
    # the clerk and the counter
    held = t >= 2.95
    ph = 0.0
    for T in TOSS:
        if T - 0.22 <= t < T + 0.25: ph = eout(seg(t, T - 0.22, T)) * (1 - ease(seg(t, T + 0.05, T + 0.25)))
    if held: rh = lerp2((40, -110), (110, -215), ease(seg(t, 2.95, 3.2)))
    else: rh = lerp2((40, -110), (165, -255), ph)
    hd = stick(c, 400, 1236, 1.0, 'clk', f, lh=(-70, -70), rh=rh, face='o' if slam else 'flat', eyes='big' if slam else 'dot', shirt=hx('7A8FA8'),
               look=(0.6, -1) if slam else (1, 0.1), hat='cap', bob=math.sin(g * 3) * 2, legs=False)
    wline(c, [(hd[0] - 4, hd[1] + hd[2] * 0.2), (hd[0] + 16, hd[1] + hd[2] * 0.3), (hd[0] + 36, hd[1] + hd[2] * 0.2)], 'mus', f, lw=10, col=INK, amp=0.5)
    if held: mlet(c, 400 + rh[0] + 34, 1236 + rh[1] - 30, 1.0, rot=0.15 + 0.05 * math.sin(g * 6), col=hx('F3E7CF'))
    rrect(c, 110, 1180, 540, 300, 14); fs(c, WOOD, 9)
    rrect(c, 92, 1160, 576, 34, 10); fs(c, WOODD, 8)
    left = sum(1 for T in TOSS if t < T - 0.2) + (0 if held else 1)
    for m in range(left):
        mlet(c, 190 + (m % 3) * 46, 1146 - (m // 3) * 22 - (m % 2) * 6, 0.9, rot=-0.3 + m * 0.17, col=hx('F3E7CF'))
    # letters fly into the stove
    arr = -9.0
    for i, T in enumerate(TOSS):
        u = seg(t, T, T + 0.5)
        if u >= 1: arr = max(arr, T + 0.5)
        elif u > 0:
            x = lerp(565, SX, u); y = lerp(985, SFL - 235, u) - 190 * math.sin(u * math.pi)
            mlet(c, x, y, 1.0 - 0.25 * u, rot=u * 7 + i, col=hx('F3E7CF'))
    # the wall calendar
    rrect(c, 580, 630, 170, 196, 12); fs(c, hx('F7EEDC'), 8)
    rrect(c, 580, 630, 170, 50, 12); fs(c, hx('9A7A55'), 8)
    for k in range(2):
        c.new_path(); c.arc(625 + k * 80, 630, 9, 0, 2 * math.pi); fs(c, hx('5A3B25'), 5)
    if not slam:
        for k in range(3):
            c.rectangle(606, 706 + k * 34, 118 - k * 26, 12); rgb(c, INK, 0.3); c.fill()
    # sepia pass
    c.set_operator(cairo.OPERATOR_HSL_COLOR); rgb(c, hx('B98A55')); c.paint(); c.set_operator(cairo.OPERATOR_OVER)
    vg = cairo.RadialGradient(540, 1000, 520, 540, 1000, 1150)
    vg.add_color_stop_rgba(0, 0.2, 0.12, 0.05, 0); vg.add_color_stop_rgba(1, 0.2, 0.12, 0.05, 0.5)
    c.set_source(vg); c.paint()
    rj = jr('scr', f, 3)
    for k in range(3):
        xx = rj.uniform(40, W - 40); c.rectangle(xx, 500, 2.5, 1420); rgb(c, WHITE, 0.16); c.fill()
    for k in range(5):
        c.new_path(); c.arc(rj.uniform(0, W), rj.uniform(520, H), rj.uniform(2, 5), 0, 2 * math.pi); rgb(c, hx('2A1A0C'), 0.45); c.fill()
    # the fire stays in colour
    oy = SFL - 150
    if not slam:
        flare = max(0.0, 1 - (t - arr) / 0.45) if arr > 0 else 0
        gl = cairo.RadialGradient(SX, oy - 70, 20, SX, oy - 70, 300 + 80 * flare)
        gl.add_color_stop_rgba(0, 1, 0.62, 0.2, 0.55 + 0.25 * flare); gl.add_color_stop_rgba(1, 1, 0.62, 0.2, 0)
        c.set_source(gl); c.rectangle(SX - 400, oy - 470, 800, 800); c.fill()
        c.save(); rrect(c, SX - 76, SFL - 302, 152, 148, 20); c.clip()
        flames(c, SX, oy, 1.0, g, 1.0 + 0.5 * flare); c.restore()
        if flare > 0:
            for i in range(7):
                a = -math.pi * (0.12 + 0.76 * i / 6); d_ = 60 + 190 * (1 - flare)
                c.new_path(); c.arc(SX + math.cos(a) * d_, oy - 80 + math.sin(a) * d_, 4 + 6 * flare, 0, 2 * math.pi); rgb(c, hx('FFC83D') if i % 2 else hx('FF7A2E'), flare); c.fill()
    else:
        for k in range(3):
            rrect(c, SX - 54, SFL - 286 + k * 34, 78, 12, 6); rgb(c, hx('FF8A3D'), 0.75 + 0.2 * math.sin(g * 15 + k)); c.fill()
        if q < 0.35:
            for i in range(7):
                a = math.pi * 2 * i / 7; r0 = 110 + 240 * q
                wline(c, [(SX + math.cos(a) * r0, SFL - 228 + math.sin(a) * r0), (SX + math.cos(a) * (r0 + 40), SFL - 228 + math.sin(a) * (r0 + 40))], ('slm', i), f,
                      lw=9, col=WHITE, amp=0.6, a=1 - q / 0.35)
        kk = eback(seg(t, 3.55, 3.8))
        c.save(); c.translate(656, 730); c.scale(kk, kk); c.rotate(-0.05 + 0.03 * math.sin(g * 8))
        rrect(c, -122, -134, 244, 268, 16); fs(c, CREAM, 9)
        rrect(c, -122, -134, 244, 66, 16); fs(c, CORAL, 9)
        fit(c, "1912", 0, 84, 96, 204, INK)
        c.restore()
        for k in range(4):
            a_ = math.sin(g * 6 + k * 1.7)
            if a_ > 0: sparkle(c, 528 + (k % 2) * 258, 606 + (k // 2) * 250, 28 * a_, GOLD, 0.95)
        pu = seg(t, 3.55, 4.3)                      # the torn page falls
        if pu < 1:
            c.save(); c.translate(665 - 90 * pu, 760 + 520 * pu * pu); c.rotate(-2.2 * pu); rrect(c, -80, -70, 160, 140, 8); rgb(c, hx('E9D9BB'), 1 - pu * 0.3); c.fill_preserve()
            rgb(c, INK, 0.6); c.set_line_width(5); c.stroke(); c.restore()
    c.restore()
    # the hero watches, in colour
    hx_, hy_ = 236, 1372
    fear = 1.0 if not slam else max(0.0, 1 - q / 0.5)
    gl = cairo.RadialGradient(hx_, hy_, 50, hx_, hy_, 240)
    gl.add_color_stop_rgba(0, 1, 1, 1, 0.75); gl.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(gl); c.rectangle(hx_ - 250, hy_ - 250, 500, 500); c.fill()
    if fear > 0.3: sweat(c, hx_, hy_, 0.85, g, f, n=4, a0=-2.7, da=0.48)
    flinch = 0.0
    for T in TOSS: flinch = max(flinch, math.sin(clamp(seg(t, T + 0.42, T + 0.72)) * math.pi))
    hero(c, hx_ + 4 * math.sin(g * 41) * fear, hy_ + 3 * math.sin(g * 53) * fear - 16 * flinch, 0.86, 'hero', f, face='o' if (not slam or q < 0.45) else 'flat', eyes='big',
         rot=-0.06 + 0.05 * math.sin(g * 30) * fear, look=(1, -0.4) if not slam else (0.75, -1), sq=1 - 0.05 * flinch)
    caption(c, t, 0.25, [[("BEFORE 1912: THE", CREAM)], [("DEAD LETTER OFFICE.", GOLD)]], y=300, size=90, t1=2.25)
    caption(c, t, 2.3, [[("MOST WERE", CREAM)], [("DESTROYED.", GOLD)]], y=300, size=96)


# ------------------------------------------------------------------ the mailroom and the child's letter
def mailroom(c, f, g, floor=1420):
    bg(c, hx('FFE0BC'), hx('FFF2DC'))
    for i in range(6):
        c.rectangle(40 + i * 190, 480, 96, floor - 480); rgb(c, hx('FFD3A6'), 0.55); c.fill()
    c.rectangle(0, floor, W, H - floor); c.set_source(grad(0, floor, 0, H, [(0, hx('C98B5E')), (1, hx('A86F45'))])); c.fill()
    wline(c, [(0, floor), (W, floor)], 'mfl', f, lw=7, amp=0.8)
    xlights(c, -20, 590, 550, 590, g, n=8, sag=40, key=1); xlights(c, 530, 590, W + 20, 590, g, n=8, sag=40, key=3)


def teddy(c, x, y, s, key, f, wave=0.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for (dx, dy) in ((-30, -64), (30, -64)):
        wcirc(c, dx, dy, 15, (key, 'e', dx), f, amp=2); rgb(c, CR_O); c.set_line_width(7); c.stroke()
    wcirc(c, 0, 40, 44, (key, 'b'), f, amp=3, ry=52); rgb(c, hx('F1C27D')); c.fill_preserve(); rgb(c, CR_O); c.set_line_width(7); c.stroke()
    wcirc(c, 0, -34, 38, (key, 'h'), f, amp=3); rgb(c, hx('F1C27D')); c.fill_preserve(); rgb(c, CR_O); c.set_line_width(7); c.stroke()
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * 13, -40, 4.5, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.new_path(); c.arc(0, -28, 11, math.radians(20), math.radians(160)); rgb(c, INK); c.set_line_width(4.5); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    wline(c, [(-40, 20), (-66, 44)], (key, 'al'), f, lw=8, col=CR_O, amp=1.5)
    a = -0.5 - 0.9 * wave
    wline(c, [(40, 20), (40 + 36 * math.cos(a), 20 + 36 * math.sin(a))], (key, 'ar'), f, lw=8, col=CR_O, amp=1.5)
    for sg in (-1, 1): wline(c, [(sg * 20, 88), (sg * 26, 108)], (key, 'lg', sg), f, lw=8, col=CR_O, amp=1.5)
    c.restore()


def page(c, x, y, s, key, f, rot=0.0, unfold=1.0, red=(0, 0, 0), wave=0.0, hrt=0.0):
    """the child's letter, 380 x 480. red = how far each black bar has been drawn"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * max(0.08, unfold))
    rrect(c, -180, -230, 380, 480, 14); rgb(c, INK, 0.22); c.fill()
    rrect(c, -190, -240, 380, 480, 14); fs(c, hx('FFFDF6'), 8)
    for yy in (-80, 80):
        c.new_path(); c.move_to(-186, yy); c.line_to(186, yy); rgb(c, INK, 0.1); c.set_line_width(3); c.stroke()
    crayon(c, "DEAR SANTA,", -162, -168, 50, [CR_R, CR_G], seed=5, wob=1.3)
    for k, wdt in enumerate((300, 250, 280)):
        pts = [(-158 + i * wdt / 11, -118 + k * 40 + 7 * math.sin(i * 2.1 + k * 1.3)) for i in range(12)]
        wline(c, pts, (key, 'wl', k), f, lw=7, col=CR_B, amp=1.4)
    teddy(c, -96, 104, 1.0, (key, 'td'), f, wave)
    crayon(c, "LOVE,", 14, 44, 32, [CR_G], seed=2)
    crayon(c, "SAM", 14, 98, 52, [CR_R], seed=8, wob=1.3)
    for k, wdt in enumerate((150, 120)):
        pts = [(18 + i * wdt / 7, 138 + k * 34 + 5 * math.sin(i * 2.3 + k)) for i in range(8)]
        wline(c, pts, (key, 'ad', k), f, lw=6, col=CR_B, amp=1.2)
    for (bx, by, bw, bh), rk in zip(((8, 54, 142, 54), (10, 122, 166, 28), (10, 156, 136, 28)), red):
        if rk > 0.01:
            rrect(c, bx, by, max(14, bw * rk), bh, 7); rgb(c, INK); c.fill()
    if hrt > 0.01:
        c.save(); c.translate(-22, 16); c.scale(hrt, hrt); heart(c, 0, 0, 0.62, CR_R); c.restore()
    c.restore()


def badge(c, x, y, r, k, f, top, big, rot=0.0):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k); c.rotate(rot)
    pts = []
    for i in range(24):
        a = math.pi * i / 12; rr = r if i % 2 == 0 else r * 0.76
        pts.append((math.cos(a) * rr, math.sin(a) * rr))
    wpoly(c, pts, 'bdg', f, 1.5); fs(c, GOLD, 9)
    txt(c, top, 0, -r * 0.2, r * 0.27, INK); txt(c, big, 0, r * 0.42, r * 0.62, INK)
    c.restore()


# ------------------------------------------------------------------ scene 4: 1912, postmasters may open it
def scene4(c, t, f, g):
    mailroom(c, f, g)
    DY = 1250; hx0 = lerp(-240, 320, eout(seg(t, 0.0, 0.6))); HT = DY - 14 - 200
    opened = t >= 1.3
    # the postal worker behind the desk
    reach = ease(seg(t, 0.65, 0.95)) * (1 - ease(seg(t, 1.35, 1.7)))
    wx = 704; WS = 1.08
    lh = lerp2((-70, -50), ((320 + 126 - wx) / WS, (HT + 8 - 1262) / WS), reach)
    happy = t >= 3.1
    hd = stick(c, wx, 1262, WS, 'wrk', f, lh=lh, rh=(70, -50) if not happy else (60, -150), face='grin' if happy else ('o' if 1.3 <= t < 1.9 else 'smile'),
               eyes='closed' if happy else 'dot', shirt=BLUE, look=(-1, -0.5) if t > 1.3 else (-1, 0.3), hat='cap', bob=math.sin(g * 3) * 2, legs=False)
    if reach > 0.05:      # the letter opener
        ox, oy = wx + lh[0] * WS, 1262 + lh[1] * WS
        wline(c, [(ox + 6, oy - 4), (ox - 62, oy + 12)], 'opn', f, lw=14, col=INK, amp=0.4); wline(c, [(ox + 2, oy - 3), (ox - 58, oy + 11)], 'opn2', f, lw=6, col=GOLD, amp=0.3)
    for i in range(2):
        hq = seg(t, 3.15 + i * 0.4, 4.4 + i * 0.4)
        if 0 < hq < 1: heart(c, hd[0] + 40 + i * 50, hd[1] - 90 - 120 * hq, 0.85 + 0.2 * i, CORAL, 1 - ein(hq))
    # the desk
    rrect(c, 60, DY, 960, 300, 16); fs(c, WOOD, 9)
    rrect(c, 40, DY - 14, 1000, 40, 12); fs(c, WOODD, 8)
    for k in range(3): mlet(c, 872 + k * 18, DY - 44 - k * 18, 1.1, rot=-0.2 + k * 0.22)
    # the hero
    pop = math.sin(clamp(seg(t, 1.3, 1.6)) * math.pi)
    if t < 1.0: face, eyes, look = 'smile', 'dot', (1, -0.3)
    elif t < 1.9: face, eyes, look = 'o', 'big', (0.6, -1)
    else: face, eyes, look = 'smile', ('closed' if int(g * 1.4) % 3 == 0 else 'dot'), (0.1, -1)
    hero(c, hx0, DY - 14 - 100 - 22 * pop, 1.0, 'hero', f, face=face, eyes=eyes, look=look, rot=0.03 * math.sin(g * 9) + 0.06 * pop,
         flap=eback(seg(t, 1.3, 1.5)) if opened else 0.0)
    zq = seg(t, 1.02, 1.3)
    if 0 < zq < 1:        # the cut runs along the top edge
        zx = lerp(hx0 + 140, hx0 - 140, zq)
        for k in range(4):
            a = -math.pi * (0.2 + 0.2 * k)
            wline(c, [(zx + math.cos(a) * 16, HT + math.sin(a) * 16), (zx + math.cos(a) * 50, HT + math.sin(a) * 50)], ('zp', k), f, lw=7, col=GOLD if k % 2 else WHITE, amp=0.8)
    if 1.3 <= t < 1.6:
        q = (t - 1.3) / 0.3
        for i in range(6):
            a = -math.pi * (0.1 + 0.8 * i / 5); r0 = 110 + 130 * q
            wline(c, [(hx0 + math.cos(a) * r0, HT - 10 + math.sin(a) * r0 * 0.7), (hx0 + math.cos(a) * (r0 + 34), HT - 10 + math.sin(a) * (r0 + 34) * 0.7)], ('pp', i), f,
                  lw=8, col=WHITE, amp=0.6, a=1 - q)
    # the letter rises and unfolds
    rise = ease(seg(t, 1.4, 2.15))
    if rise > 0.01:
        page(c, lerp(hx0, 332, rise), lerp(HT, 806, rise) + 4 * math.sin(g * 2.4), lerp(0.2, 0.86, rise), 'pg', f, rot=lerp(-0.4, -0.05, rise) + 0.015 * math.sin(g * 2),
             unfold=lerp(0.25, 1.0, ease(seg(t, 1.6, 2.2))), wave=0.5 + 0.5 * math.sin(g * 12) if t > 3.2 else 0.0, hrt=eback(seg(t, 3.3, 3.55)))
    badge(c, 816, 792, 130, eback(seg(t, 2.42, 2.7)), f, "YEAR", "114", rot=-0.1 + 0.05 * math.sin(g * 7))
    caption(c, t, 0.25, [[("1912: POSTMASTERS MAY", CREAM)], [("OPEN SANTA'S MAIL.", GOLD)]], y=300, size=88, t1=2.3)
    caption(c, t, 2.35, [[("THIS IS", CREAM), (" YEAR 114.", GOLD)]], y=320, size=100)


# ------------------------------------------------------------------ scene 5: details removed, adopted online
def cursor(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.move_to(0, 0); c.line_to(0, 62); c.line_to(16, 47); c.line_to(28, 74); c.line_to(40, 68); c.line_to(28, 42); c.line_to(48, 42); c.close_path()
    rgb(c, WHITE); c.fill_preserve(); rgb(c, INK); c.set_line_width(7); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke(); c.restore()


def scene5(c, t, f, g):
    bg(c, hx('CDEDE6'), hx('F2FAF3'))
    for i in range(5):
        c.rectangle(110 + i * 220, 480, 70, 760); rgb(c, hx('BFE5DC'), 0.6); c.fill()
    xlights(c, -20, 560, W + 20, 560, g, n=13, sag=30, key=2)
    adopted = t >= 3.4; qa = t - 3.4
    # the stranger arrives
    sx_ = lerp(1240, 906, eout(seg(t, 1.9, 2.5)))
    hd = stick(c, sx_, 1272, 0.95, 'str', f, lh=(-44, -52), rh=(64, -40) if not adopted else (84 + 10 * math.sin(g * 9), -280),
               face='grin' if adopted else ('o' if 2.5 <= t < 3.0 else 'smile'), eyes='closed' if adopted and qa > 0.25 else 'dot', shirt=PURPLE, look=(-1, -0.2),
               bob=math.sin(g * 3) * 2 + (10 * abs(math.sin(g * 9)) if adopted else 0), legs=False)
    c.new_path(); c.arc(hd[0], hd[1] - hd[2] * 0.3, hd[2] * 1.03, math.pi * 0.98, math.pi * 2.02); c.close_path(); fs(c, hx('5A3B25'), 6)
    for sg in (-1, 1):
        c.new_path(); c.arc(hd[0] + sg * hd[2] * 0.36 - 5, hd[1] - hd[2] * 0.06, hd[2] * 0.25, 0, 2 * math.pi); rgb(c, INK); c.set_line_width(5); c.stroke()
    # the desk and the laptop
    c.rectangle(0, 1195, W, 110); rgb(c, hx('E7C196')); c.fill()
    c.rectangle(0, 1300, W, H - 1300); c.set_source(grad(0, 1300, 0, H, [(0, hx('C98B5E')), (1, hx('A86F45'))])); c.fill()
    wline(c, [(0, 1195), (W, 1195)], 'd5a', f, lw=7, amp=0.8); wline(c, [(0, 1300), (W, 1300)], 'd5b', f, lw=7, amp=0.8)
    wpoly(c, [(226, 1140), (864, 1140), (930, 1222), (160, 1222)], 'lpb', f, 1.5); fs(c, STEEL, 9)
    rrect(c, 480, 1166, 130, 34, 8); rgb(c, STEELD, 0.7); c.fill()
    rrect(c, 250, 600, 590, 546, 28); fs(c, IRON, 10)
    rrect(c, 270, 620, 550, 506, 12); rgb(c, hx('F4F8FB')); c.fill()
    c.save(); rrect(c, 270, 620, 550, 506, 12); c.clip()
    c.rectangle(270, 620, 550, 50); rgb(c, hx('D3DEE9')); c.fill()
    for k, col in enumerate((CORAL, GOLD, GREEN)):
        c.new_path(); c.arc(296 + k * 26, 645, 8, 0, 2 * math.pi); rgb(c, col); c.fill()
    rrect(c, 390, 632, 330, 26, 13); rgb(c, WHITE); c.fill()
    mv = ease(seg(t, 2.05, 2.5))
    red = (ease(seg(t, 0.55, 0.9)), ease(seg(t, 0.95, 1.3)), ease(seg(t, 1.35, 1.7)))
    px_, py_, ps = lerp(545, 408, mv), lerp(899, 898, mv), lerp(0.9, 0.68, mv)
    page(c, px_, py_, ps, 'pg5', f, rot=-0.02, red=red, hrt=eback(seg(t, 3.5, 3.75)))
    for i, (r0, r1) in enumerate(((0.55, 0.9), (0.95, 1.3), (1.35, 1.7))):          # the marker tip
        if r0 <= t < r1 + 0.04:
            bx, by, bw, bh = ((8, 54, 142, 54), (10, 122, 166, 28), (10, 156, 136, 28))[i]
            mx, my = px_ + (bx + bw * red[i]) * ps, py_ + (by + bh / 2) * ps
            wline(c, [(mx, my), (mx + 70, my - 96)], 'mk', f, lw=30, col=INK, amp=0.4); wline(c, [(mx + 16, my - 22), (mx + 66, my - 90)], 'mk2', f, lw=16, col=GOLD, amp=0.3)
    if mv > 0.02:
        for k, wd in enumerate((210, 170)):
            rrect(c, 590 + 240 * (1 - mv), 752 + k * 30, wd, 14, 7); rgb(c, hx('B9C7D6')); c.fill()
        kb = eback(seg(t, 2.35, 2.6))
        if kb > 0.01:
            pulse = 1 + 0.05 * math.sin(g * 9) if not adopted else 1 + 0.12 * math.exp(-6 * qa) * math.cos(qa * 22)
            press = 1 - 0.1 * math.sin(clamp(seg(t, 3.32, 3.48)) * math.pi)
            c.save(); c.translate(690, 880); c.scale(kb * pulse, kb * pulse); heart(c, 0, 0, 1.5, CORAL if adopted else WHITE); c.restore()
            c.save(); c.translate(690, 1012); c.scale(kb * press, kb * press)
            rrect(c, -112, -34, 232, 84, 20); rgb(c, INK, 0.25); c.fill()
            rrect(c, -116, -42, 232, 84, 20); fs(c, GREEN if adopted else CORAL, 7)
            fit(c, "ADOPTED!" if adopted else "ADOPT", 0, 17, 50, 196, WHITE)
            c.restore()
    c.restore()
    rrect(c, 250, 600, 590, 546, 28); rgb(c, INK); c.set_line_width(10); c.stroke()
    # a mouse under the stranger's hand
    if sx_ < 1000:
        rrect(c, sx_ - 78, 1196, 62, 40, 18); fs(c, WHITE, 6)
    # the cursor
    if 2.55 <= t:
        cu = ease(seg(t, 2.6, 3.25))
        cx_, cy_ = lerp(806, 752, cu), lerp(1112, 1036, cu)
        cursor(c, cx_, cy_, 1.0 - 0.18 * math.sin(clamp(seg(t, 3.3, 3.48)) * math.pi))
    if adopted:
        for i in range(7):
            a = -math.pi * (0.08 + 0.84 * i / 6); d_ = 60 + 330 * eout(clamp(qa / 0.8))
            heart(c, 690 + math.cos(a) * d_, 1000 + math.sin(a) * d_ * 0.9, 0.6 + 0.25 * (i % 2), CORAL if i % 2 else PINK, clamp(1.2 - qa / 0.8))
    # the hero watches from the desk
    hop = 52 * abs(math.sin((t - 3.4) * 8)) * max(0.0, 1 - qa / 0.9) if adopted else 0
    if t < 1.9: face, eyes, look = ('o' if any(r0 <= t < r1 for r0, r1 in ((0.55, 0.9), (0.95, 1.3), (1.35, 1.7))) else 'flat'), 'big', (1, -0.7)
    elif not adopted: face, eyes, look = 'flat', 'big', (1, -0.4)
    else: face, eyes, look = 'grin', ('closed' if qa > 0.2 else 'dot'), (1, -0.5)
    hero(c, 162, 1180 - hop, 0.68, 'hero', f, face=face, eyes=eyes, look=look, rot=-0.05 + 0.04 * math.sin(g * 6))
    caption(c, t, 0.25, [[("NAMES AND ADDRESSES", CREAM)], [("ARE REMOVED.", GOLD)]], y=300, size=88, t1=2.25)
    caption(c, t, 2.3, [[("A KIND STRANGER", CREAM)], [("ADOPTS IT ONLINE.", GOLD)]], y=300, size=90)


# ------------------------------------------------------------------ scene 6: the gift arrives
def parcel(c, x, y, s, f, rot=0.0, key='pc'):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    wrect(c, -78, -60, 156, 120, key, f, 1.5); fs(c, hx('D9A066'), 8)
    c.rectangle(-14, -60, 28, 120); rgb(c, CORAL); c.fill(); c.rectangle(-78, -12, 156, 24); rgb(c, CORAL); c.fill()
    wrect(c, -78, -60, 156, 120, key, f, 1.5); rgb(c, INK); c.set_line_width(8); c.stroke()
    for sg in (-1, 1):
        wcirc(c, sg * 22, -74, 20, (key, 'bw', sg), f, amp=1.5, ry=14); fs(c, CORAL, 6)
    c.new_path(); c.arc(0, -70, 9, 0, 2 * math.pi); fs(c, hx('FF8A7C'), 5)
    c.save(); c.translate(46, 30); c.rotate(0.2); rrect(c, -22, -15, 44, 30, 5); fs(c, WHITE, 4); heart(c, 0, -1, 0.26, CR_R); c.restore()
    c.restore()


def pine(c, x, y, s, f, key='pn'):
    wline(c, [(x, y), (x, y - 60 * s)], (key, x, 't'), f, lw=20 * s, col=hx('8A5A33'), amp=0.6)
    for k in range(3):
        w = (120 - k * 28) * s; yb = y - (50 + k * 78) * s
        wpoly(c, [(x - w, yb), (x, yb - 130 * s), (x + w, yb)], (key, x, k), f, 1.5); fs(c, hx('3E9B6E'), 7)
        c.new_path(); c.move_to(x - w * 0.55, yb - 54 * s); c.line_to(x, yb - 130 * s); c.line_to(x + w * 0.55, yb - 54 * s)
        c.curve_to(x + w * 0.2, yb - 40 * s, x - w * 0.2, yb - 68 * s, x - w * 0.55, yb - 54 * s); rgb(c, SNOW); c.fill()


def scene6(c, t, f, g):
    GY = 1400
    zz = 1 + 0.35 * ease(seg(t, 2.35, 3.0))
    bg(c, hx('F3BE93'), hx('F3BE93'))
    c.save(); c.translate(600, 1150); c.scale(zz, zz); c.translate(-600, -1150)
    for yy in range(756, GY, 64):
        c.rectangle(-300, yy, W + 600, 4); rgb(c, INK, 0.08); c.fill()
    pine(c, 96, GY, 1.15, f); pine(c, 250, GY, 0.8, f)
    xlights(c, -220, 826, 440, 826, g, n=11, sag=30, key=4); xlights(c, 440, 826, W + 240, 826, g, n=11, sag=30, key=2)
    # the window, with a tree inside
    rrect(c, 830, 880, 190, 236, 14); fs(c, hx('FFE9A8'), 8)
    c.save(); rrect(c, 834, 884, 182, 228, 12); c.clip()
    wpoly(c, [(866, 1116), (925, 920), (984, 1116)], 'tr6', f, 1.0); rgb(c, hx('3E9B6E')); c.fill()
    for k in range(6):
        tw_ = 0.5 + 0.5 * math.sin(g * 6 + k * 1.9)
        c.new_path(); c.arc(900 + (k * 37) % 56, 990 + (k * 53) % 110, 7, 0, 2 * math.pi); rgb(c, XCOL[k % 5], 0.5 + 0.5 * tw_); c.fill()
    sparkle(c, 925, 926, 16 + 4 * math.sin(g * 5), GOLD)
    c.restore()
    wline(c, [(925, 880), (925, 1116)], 'wm6', f, lw=7, amp=0.6)
    rrect(c, 814, 1106, 222, 28, 14); fs(c, SNOW, 6)
    c.rectangle(-200, GY, W + 400, H - GY); c.set_source(grad(0, GY, 0, H, [(0, SNOW), (1, SNOWD)])); c.fill()
    wline(c, [(-200, GY), (W + 200, GY)], 'g6', f, lw=7, amp=0.8, a=0.7)
    # the door and the child
    op = ease(seg(t, 1.3, 1.8))
    rrect(c, 500, 880, 250, 520, 16); fs(c, hx('3A2A22'), 9)
    got = t >= 2.7
    jump = 64 * abs(math.sin((t - 3.05) * 6.5)) * max(0.0, 1 - (t - 3.05) / 1.25) if t >= 3.05 else 0
    khip = (636, GY - 137 - jump)
    give = ease(seg(t, 1.9, 2.3)); u = ease(seg(t, 2.3, 2.7))
    cx = lerp(-160, 372, ease(seg(t, 0.2, 1.4))); walking = t < 1.4
    crh = lerp2((84, -84), (176, -150), give) if t < 2.9 else (96 + 12 * math.sin(g * 9), -290)
    hand = (cx + lerp2((84, -84), (176, -150), give)[0] * 0.95, 1215 + lerp2((84, -84), (176, -150), give)[1] * 0.95)
    if op > 0.05:
        if not got: lh, rh, face, eyes = (-90, -150) if t > 1.9 else (-60, -20), (60, -30), ('o' if t > 1.85 else 'smile'), ('big' if t > 1.85 else 'dot')
        else: lh, rh, face, eyes = (-78, -62), (78, -62), 'grin', ('closed' if t > 2.95 else 'dot')
        kid(c, khip[0], khip[1], 0.72, 'kid6', f, lh=lh, rh=rh, face=face, eyes=eyes, look=(-1, 0.2), bob=math.sin(g * 3) * 2)
    c.save(); c.translate(500, 880); c.scale(1 - 0.84 * op, 1)
    rrect(c, 0, 0, 250, 520, 16); fs(c, hx('2F9E8F'), 9)
    c.new_path(); c.arc(206, 280, 14, 0, 2 * math.pi); fs(c, GOLD, 5)
    c.new_path(); c.arc(125, 170, 58, 0, 2 * math.pi); rgb(c, hx('2E7D4F')); c.set_line_width(26); c.stroke()
    c.new_path(); c.arc(125, 170, 58, 0, 2 * math.pi); rgb(c, INK, 0.5); c.set_line_width(3); c.stroke()
    for k in range(6):
        a = k * math.pi / 3 + 0.4; c.new_path(); c.arc(125 + 58 * math.cos(a), 170 + 58 * math.sin(a), 7, 0, 2 * math.pi); rgb(c, CR_R); c.fill()
    for sg in (-1, 1):
        wpoly(c, [(125, 226), (125 + sg * 34, 208), (125 + sg * 34, 246)], ('bow', sg), f, 1.0); fs(c, CR_R, 5)
    c.restore()
    # the carrier
    stick(c, cx, 1215, 0.95, 'car', f, lh=(-50, -20), rh=crh, lf=(-45 + (18 * math.sin(g * 10) if walking else 0), 190), rf=(45 - (18 * math.sin(g * 10) if walking else 0), 190),
          face='smile' if t < 2.9 else 'grin', eyes='dot', shirt=BLUE, look=(1, 0), hat='cap', bob=abs(math.sin(g * 10)) * 6 if walking else 0)
    rrect(c, cx - 96, 1215 - 120, 78, 96, 14); fs(c, hx('8A5A33'), 7)
    wline(c, [(cx - 60, 1215 - 120), (cx + 14, 1215 - 250)], 'strap6', f, lw=9, col=hx('8A5A33'), amp=0.6)
    if walking:
        for k in range(3):
            q = (g * 2.2 + k / 3) % 1
            c.new_path(); c.arc(cx - 50 - 60 * q, 1392 - 26 * math.sin(q * math.pi), 9 * (1 - q) + 3, 0, 2 * math.pi); rgb(c, WHITE, 0.9 * (1 - q)); c.fill()
    # the parcel
    if t < 2.3: pxy = (hand[0] + 44, hand[1] - 44); ps = 0.8
    else: pxy = lerp2((hand[0] + 44, hand[1] - 44), (khip[0] - 4, khip[1] - 44), u); ps = lerp(0.8, 0.7, u)
    parcel(c, pxy[0], pxy[1], ps, f, rot=0.06 * math.sin(g * 6) if not got else 0.05 * math.sin(g * 9))
    if got:
        for hnd in ((-78, -62), (78, -62)):
            c.new_path(); c.arc(khip[0] + hnd[0] * 0.72 + (6 if hnd[0] < 0 else -6), khip[1] + hnd[1] * 0.72 + 6, 16 * 0.72, 0, 2 * math.pi); fs(c, CORAL, 4.5)
        for i in range(3):
            hq = seg(t, 2.8 + i * 0.3, 4.2 + i * 0.3)
            if 0 < hq < 1: heart(c, 560 + i * 76, 1050 - 130 * hq, 0.8 + 0.15 * i, CORAL, 1 - ein(hq))
    c.restore()
    # the hero watches from the mailroom
    bk = eback(seg(t, 0.5, 0.8))
    if bk > 0.01:
        c.save(); c.translate(882, 1352); c.scale(bk, bk)
        c.new_path(); c.arc(0, 0, 106, 0, 2 * math.pi); fs(c, hx('FFE9C9'), 9)
        hero(c, 0, 4 - (20 * abs(math.sin((t - 2.75) * 8)) * max(0.0, 1 - (t - 2.75) / 1.0) if got else 0), 0.53, 'hero', f, face='grin' if got else 'smile',
             eyes='closed' if t > 3.0 else 'dot', look=(-1, -0.4), rot=0.04 * math.sin(g * 5))
        c.restore()
    snowfall(c, g, n=26, seed=6, a=0.9)
    caption(c, t, 0.25, [[("THE STRANGER", CREAM)], [("SHIPS THE GIFT.", GOLD)]], y=300, size=92)
    strip(c, 562, ["Sources: USPS news releases 2026, USPS Operation Santa,", "USPS Postal Facts, Smithsonian Magazine."], eout(seg(t, 0.7, 1.0)), size=27, w=800)
    strip(c, 668, ["Not every letter gets adopted."], eout(seg(t, 2.9, 3.2)), size=38)


# ------------------------------------------------------------------ scene 7: adopted, and the deadline
def stamper(c, x, y, s, f):
    c.save(); c.translate(x, y); c.scale(s, s)
    wcirc(c, 0, -150, 52, 'sth', f, amp=2); fs(c, WOODD, 9)
    wline(c, [(0, -104), (0, -40)], 'stn', f, lw=44, col=INK, amp=0.4); wline(c, [(0, -104), (0, -40)], 'stn2', f, lw=28, col=WOOD, amp=0.3)
    rrect(c, -104, -44, 208, 44, 12); fs(c, CR_R, 9)
    c.restore()


def scene7(c, t, f, g):
    mailroom(c, f, g, floor=1560)
    SY = 1330
    # the shelf
    for xx in (150, 930): wline(c, [(xx, SY + 24), (xx, 1560)], ('sh7', xx), f, lw=22, col=WOODD, amp=0.6)
    rrect(c, 40, SY, 1000, 36, 12); fs(c, WOOD, 9)
    stamped = t >= 1.25; q = t - 1.25
    HX, HY, HS = 500, SY - 158, 1.5
    # the letters that still wait
    for i, (mx, ms) in enumerate(((128, 1.25), (240, 1.05), (786, 1.05), (892, 1.2))):
        hopm = 18 * abs(math.sin(g * 5 + i * 1.3)) if stamped else 4 * abs(math.sin(g * 3 + i))
        mlet(c, mx, SY - 34 * ms - hopm, ms, rot=0.08 * math.sin(g * 4 + i), face='o' if (stamped and q < 0.8) else 'smile',
             look=(1 if mx < 500 else -1, -0.6))
    # the calendar
    ck = eback(seg(t, 0.4, 0.65))
    if ck > 0.01:
        c.save(); c.translate(852, 800); c.scale(ck, ck); c.rotate(0.05 + 0.02 * math.sin(g * 5))
        rrect(c, -104, -124, 208, 248, 16); fs(c, CREAM, 9)
        rrect(c, -104, -124, 208, 74, 16); fs(c, CORAL, 9); txt(c, "DEC", 0, -68, 56, WHITE)
        txt(c, "5", 0, 96, 150, INK)
        rk = seg(t, 0.85, 1.15)
        if rk > 0:
            c.new_path(); c.save(); c.translate(0, 44); c.scale(1.0, 0.92); c.arc(0, 0, 84, -1.4, -1.4 + 2 * math.pi * rk * 1.04); c.restore()
            rgb(c, CR_R); c.set_line_width(9); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        c.restore()
    # the hero
    sq = 1 - 0.14 * math.sin(clamp(seg(t, 1.25, 1.5)) * math.pi)
    hop = 30 * abs(math.sin((t - 1.55) * 7)) * max(0.0, 1 - (t - 1.55) / 0.9) if t >= 1.55 else 0
    if t < 0.9: face, eyes, look = 'smile', 'dot', (1, -0.6)
    elif not stamped: face, eyes, look = 'o', 'big', (0.3, -1)
    elif t < 2.35: face, eyes, look = 'grin', ('closed' if q > 0.3 else 'big'), (0, 0)
    else: face, eyes, look = 'smile', ('closed' if int(g * 1.6) % 4 == 0 else 'dot'), (0, 0.2)
    hero(c, HX, HY + (1 - sq) * 150 - hop, HS, 'hero', f, face=face, eyes=eyes, look=look, rot=0.04 * math.sin(g * 4) + (0.05 * math.sin(g * 2.2) if t > 2.35 else 0), sq=sq,
         adopted=eback(seg(t, 1.25, 1.42)) if stamped else 0.0)
    # the stamp comes down
    tx, ty_ = HX + 54 * HS, HY + 70 * HS - 34
    if t < 2.0:
        if t < 0.95: sp = lerp2((tx + 60, 560), (tx + 30, 760), eout(seg(t, 0.6, 0.95))); sk = eback(seg(t, 0.6, 0.85))
        elif t < 1.25: sp = lerp2((tx + 30, 760), (tx, ty_), ein(seg(t, 1.08, 1.25))); sk = 1.0
        else: sp = lerp2((tx, ty_), (tx + 150, 700), eout(seg(t, 1.36, 1.8))); sk = 1 - ein(seg(t, 1.7, 2.0))
        if sk > 0.01: stamper(c, sp[0], sp[1], 1.0 * sk, f)
    if stamped and q < 0.35:
        for i in range(8):
            a = math.pi * 2 * i / 8; r0 = 150 + 240 * q
            wline(c, [(tx + math.cos(a) * r0, ty_ + 30 + math.sin(a) * r0 * 0.6), (tx + math.cos(a) * (r0 + 40), ty_ + 30 + math.sin(a) * (r0 + 40) * 0.6)], ('st7', i), f,
                  lw=9, col=WHITE if i % 2 else GOLD, amp=0.6, a=1 - q / 0.35)
    if stamped:
        for i in range(4):
            hq = seg(t, 1.4 + i * 0.32, 2.9 + i * 0.32)
            if 0 < hq < 1: heart(c, 330 + i * 118, 1010 - 190 * hq, 0.9 + 0.2 * (i % 2), CORAL if i % 2 else PINK, 1 - ein(hq))
        rr = random.Random(12)
        for i in range(34):
            x0 = rr.uniform(60, 1020); sp_ = rr.uniform(260, 520); ph = rr.uniform(0, 6.28); col = XCOL[i % 5]; dl = rr.uniform(0, 0.5)
            yy = 640 + (q - dl) * sp_
            if q > dl and yy < SY - 10:
                c.save(); c.translate(x0 + 24 * math.sin(q * 5 + ph), yy); c.rotate(q * 6 + ph); c.rectangle(-9, -5, 18, 10); rgb(c, col); c.fill(); c.restore()
    if t > 2.6:
        for k in range(2):
            qq = (g * 0.7 + k * 0.5) % 1
            txt(c, "?", 236 + k * 44, 1010 - 90 * qq, 84, GOLDD, CAP, a=math.sin(qq * math.pi))
    caption(c, t, 0.15, [[("THIS YEAR'S DEADLINE:", CREAM)], [("DECEMBER 5.", GOLD)]], y=300, size=90, t1=2.3)
    caption(c, t, 2.35, [[("WHAT DID YOU", CREAM)], [("ASK SANTA FOR?", GOLD)]], y=300, size=94)


SCENES = [(0.0, 3.6, scene1), (3.6, 8.0, scene2), (8.0, 12.4, scene3), (12.4, 16.8, scene4), (16.8, 21.2, scene5),
          (21.2, 25.6, scene6), (25.6, 30.0, scene7)]
TR = 0.22


def draw(c, g, f):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= g < b or (i == len(SCENES) - 1 and g >= b):
            loc = g - a
            if i >= 1 and loc < TR:
                o = eout(loc / TR)
                pa, pb, pfn = SCENES[i - 1]
                c.save(); c.translate(0, -H * o); c.rectangle(0, 0, W, H); c.clip(); pfn(c, pb - pa - 0.001, f, pb - 0.001); c.restore()
                c.save(); c.translate(0, H * (1 - o)); c.rectangle(0, 0, W, H); c.clip(); fn(c, loc, f, g); c.restore()
            else:
                c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, loc, f, g); c.restore()
            return
