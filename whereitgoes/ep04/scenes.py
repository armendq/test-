from base2 import *

SKY1 = hx('9FDCF5'); SKY2 = hx('FFE9C9'); RIV1 = hx('6CC3D6'); RIV2 = hx('3C8FAE'); IRON = hx('3A3F4F')
TOWER = hx('7483A3'); TOWERD = hx('56627F'); BRG = hx('4F9A8E'); SHK = hx('C9D3DF')
LCOLS = [GOLD, TEAL, PINK, STEEL, BLUE, GREEN, ORANGE, PURPLE, hx('E8E3D8'), hx('FF8FA3'), hx('FFD98A')]
RT, RB = 1130, 1470          # top and bottom rail of the bridge railing


# ------------------------------------------------------------------ the hero and its friends
def lock(c, x, y, s, key, f, face='smile', eyes='dot', rot=0.0, look=(0, 0), col=CORAL, hang=False, cut=False, sq=1.0):
    """x, y = centre of the body. hang=True: x, y = the point the shackle hangs from"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    if hang: c.translate(0, 141)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    parts = [(math.pi, 2 * math.pi, True, True)] if not cut else [(math.pi, 1.56 * math.pi, True, False), (1.78 * math.pi, 2 * math.pi, False, True)]
    for lw, cl in ((38, INK), (20, SHK)):
        for (a0, a1, ll, lr) in parts:
            c.new_path()
            if ll: c.move_to(-56, -70); c.line_to(-56, -95)
            c.arc(0, -95, 56, a0, a1)
            if lr: c.line_to(56, -70)
            rgb(c, cl); c.set_line_width(lw); c.stroke()
    rrect(c, -100, -85, 200, 170, 36); fs(c, col, 11)
    c.new_path(); c.arc(-50, -36, 30, math.radians(185), math.radians(262)); rgb(c, WHITE, 0.8); c.set_line_width(9); c.stroke()
    facef(c, 0, -6, 84, face, look, eyes)
    heart(c, 68, 56, 0.34, GOLD)
    c.restore()


def mini(c, x, y, s, col, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-10, -8); c.line_to(-10, -17); c.arc(0, -17, 10, math.pi, 2 * math.pi); c.line_to(10, -8)
    rgb(c, INK); c.set_line_width(8); c.stroke_preserve(); rgb(c, SHK); c.set_line_width(3.5); c.stroke()
    rrect(c, -18, -10, 36, 30, 7); rgb(c, col); c.fill_preserve(); rgb(c, INK); c.set_line_width(4); c.stroke()
    c.new_path(); c.arc(0, 5, 3.6, 0, 2 * math.pi); rgb(c, INK, 0.5); c.fill()
    c.restore()


_walls = {}


def wall_items(seed, w, h, cell=(44, 50)):
    k = (seed, int(w), int(h))
    if k not in _walls:
        r = random.Random(seed); out = []
        for j in range(int(h / cell[1])):
            for i in range(int(w / cell[0]) + 1):
                out.append(((i + (0.5 if j % 2 else 0.0)) * cell[0] + r.uniform(-9, 9), 30 + j * cell[1] + r.uniform(-8, 8),
                            r.uniform(0.9, 1.25), r.choice(LCOLS), r.uniform(-0.3, 0.3), r.random()))
        r.shuffle(out); _walls[k] = out
    return _walls[k]


def lockwall(c, x0, y0, w, h, seed, g=0.0, hole=None, dens=1.0):
    c.save(); c.rectangle(x0, y0, w, h); c.clip()
    rgb(c, INK, 0.3); c.set_line_width(3); c.new_path()
    for k in range(-int(h / 40) - 1, int(w / 40) + 2):
        c.move_to(x0 + k * 40, y0); c.line_to(x0 + k * 40 + h, y0 + h)
        c.move_to(x0 + k * 40 + h, y0); c.line_to(x0 + k * 40, y0 + h)
    c.stroke()
    for (x, y, s, col, rot, ph) in wall_items(seed, w, h):
        if ph > dens: continue
        if hole and (x0 + x - hole[0]) ** 2 + (y0 + y - hole[1]) ** 2 < hole[2] ** 2: continue
        mini(c, x0 + x, y0 + y, s, col, rot + 0.05 * math.sin(g * 3 + ph * 6.28))
    c.restore()


def keyobj(c, x, y, s, rot, f=0, face=None, eyes='dot', look=(0, 0), col=GOLD):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND)
    R = 36 if face else 24
    for lw, cl in ((22, INK), (11, col)):
        c.new_path(); c.move_to(R - 4, 0); c.line_to(R + 66, 0); c.move_to(R + 44, 0); c.line_to(R + 44, 20); c.move_to(R + 62, 0); c.line_to(R + 62, 15)
        rgb(c, cl); c.set_line_width(lw); c.stroke()
    c.new_path(); c.arc(0, 0, R, 0, 2 * math.pi); fs(c, col, 7)
    if face: facef(c, 0, 0, R * 0.92, face, look, eyes)
    else:
        c.new_path(); c.arc(-5, 0, 8, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.restore()


# ------------------------------------------------------------------ Paris
def eiffel(c, x, yb, h):
    def hw(u): return h * (0.014 + 0.185 * u ** 2.3)
    n = 16; wb = hw(1.0)
    c.new_path(); c.move_to(x, yb - h * 1.08); c.line_to(x, yb - h); rgb(c, TOWERD); c.set_line_width(4); c.stroke()
    c.new_path(); c.move_to(x - hw(0), yb - h)
    for i in range(1, n + 1):
        u = i / n; c.line_to(x - hw(u), yb - h * (1 - u))
    c.line_to(x - wb * 0.52, yb)
    c.curve_to(x - wb * 0.46, yb - h * 0.21, x + wb * 0.46, yb - h * 0.21, x + wb * 0.52, yb)
    c.line_to(x + wb, yb)
    for i in range(n - 1, -1, -1):
        u = i / n; c.line_to(x + hw(u), yb - h * (1 - u))
    c.close_path(); rgb(c, TOWER); c.fill_preserve(); rgb(c, INK, 0.6); c.set_line_width(4); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    for u, ext, th in ((0.80, 1.12, 0.034), (0.60, 1.3, 0.028), (0.10, 1.9, 0.022)):
        w_ = hw(u) * ext; c.rectangle(x - w_, yb - h * (1 - u), 2 * w_, h * th); rgb(c, TOWERD); c.fill()
    rgb(c, TOWERD, 0.55); c.set_line_width(2.5); c.new_path()
    for (u0, u1) in ((0.2, 0.4), (0.4, 0.6), (0.63, 0.8)):
        c.move_to(x - hw(u0), yb - h * (1 - u0)); c.line_to(x + hw(u1), yb - h * (1 - u1))
        c.move_to(x + hw(u0), yb - h * (1 - u0)); c.line_to(x - hw(u1), yb - h * (1 - u1))
    c.stroke()


def paris_bg(c, f, g, tx=800, base=930, th=290):
    bg(c, SKY1, SKY2)
    wcirc(c, 170, max(base - 300, 640), 60, 'sun', f, amp=3); rgb(c, hx('FFE28A')); c.fill()
    for i, (cx, cy, s) in enumerate(((330, max(base - 350, 610), 1.0), (1000, base - 210, 0.8))):
        x = (cx + g * 14 * (1 + i * 0.5)) % 1500 - 200
        for dx, r in ((-52, 32), (0, 46), (54, 30)):
            c.new_path(); c.arc(x + dx * s, cy, r * s, 0, 2 * math.pi); rgb(c, WHITE, 0.9); c.fill()
    r = random.Random(5); x = -60
    while x < W + 60:
        w = r.choice((90, 120, 150)); h = r.choice((58, 70, 82))
        c.rectangle(x, base - h, w - 4, h); rgb(c, hx('F1E3C8')); c.fill()
        c.rectangle(x - 2, base - h - 16, w, 18); rgb(c, hx('8E9BB3')); c.fill()
        for k in range(int((w - 16) / 26)):
            for row in range(2):
                c.rectangle(x + 12 + k * 26, base - h + 12 + row * 26, 10, 15); rgb(c, hx('B9C7D6')); c.fill()
        x += w
    eiffel(c, tx, base, th)
    for k in range(10):
        c.new_path(); c.arc(k * 124 + 30, base - 4, 24 + (k % 3) * 4, math.pi, 2 * math.pi); rgb(c, hx('7CC48F')); c.fill()
    c.rectangle(0, base, W, 30); rgb(c, STONED); c.fill()
    c.rectangle(0, base, W, 5); rgb(c, INK, 0.55); c.fill()
    c.rectangle(0, base + 30, W, H - base - 30); c.set_source(grad(0, base + 30, 0, base + 520, [(0, RIV1), (1, RIV2)])); c.fill()
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    for k in range(16):
        x = (k * 173 + g * 30 * (1 if k % 2 else -1)) % (W + 160) - 80; y = base + 58 + (k * 67) % 300
        c.new_path(); c.move_to(x, y); c.curve_to(x + 14, y - 7, x + 28, y + 7, x + 42, y); rgb(c, WHITE, 0.6); c.set_line_width(4); c.stroke()


def deck(c, f):
    c.rectangle(-900, RB + 8, W + 1800, 1500); c.set_source(grad(0, RB, 0, H, [(0, hx('D6A074')), (1, hx('A86F45'))])); c.fill()
    ys = (RB + 8, RB + 78, RB + 170, RB + 290, RB + 440)
    for i, y in enumerate(ys[1:]):
        wline(c, [(-900, y), (W + 900, y)], ('pl', i), f, lw=6, col=INK, amp=0.8, a=0.35)
    for i in range(14):
        x = -700 + i * 190 + (i % 3) * 40; j = i % 4
        wline(c, [(x, ys[j]), (x, ys[j + 1])], ('pj', i), f, lw=5, col=INK, amp=0.6, a=0.3)


def railing(c, f, g, panels, posts, hole=None, dens=1.0):
    for (x0, x1, seed) in panels:
        if seed is not None: lockwall(c, x0, RT, x1 - x0, RB - RT, seed, g, hole, dens)
        rrect(c, x0, RT - 16, x1 - x0, 30, 10); fs(c, IRON, 7)
        rrect(c, x0, RB - 12, x1 - x0, 30, 10); fs(c, IRON, 7)
    for px in posts:
        rrect(c, px - 18, RT - 40, 36, RB - RT + 70, 12); fs(c, IRON, 7)
        rrect(c, px - 26, RT - 54, 52, 22, 8); fs(c, IRON, 7)


def crackfx(c, x, y, q, f):
    """a crack opens on a rail at x, y. q = seconds since it opened"""
    if q < 0: return
    wline(c, [(x - 8, y - 16), (x + 5, y - 5), (x - 6, y + 4), (x + 8, y + 14)], ('crk', x), f, lw=6, col=CREAM, amp=0.8)
    if q < 1.2:
        for i, (vx, vy) in enumerate(((170, -380), (-120, -440), (70, -320))):
            c.new_path(); c.arc(x + vx * q, y - 10 + vy * q + 900 * q * q, 9, 0, 2 * math.pi); fs(c, STEEL, 4)
    if q < 0.35:
        for i in range(5):
            a = -math.pi * (0.15 + 0.7 * i / 4); r0 = 34 + 90 * q
            wline(c, [(x + math.cos(a) * r0, y + math.sin(a) * r0), (x + math.cos(a) * (r0 + 30), y + math.sin(a) * (r0 + 30))], ('ck', i), f, lw=7, col=WHITE,
                  amp=0.6, a=1 - q / 0.35)


def sweat(c, x, y, s, g, f, n=4, a0=-2.75, da=0.5):
    for i in range(n):
        ph = (g * 2.4 + i / n) % 1
        ang = a0 + i * da; rr = (150 + 95 * ph) * s
        wcirc(c, x + math.cos(ang) * rr * 0.72, y + math.sin(ang) * rr * 0.6, (15 - 9 * ph) * s, ('sw', i), f, amp=1); fs(c, hx('8FD9FA'), 4)


# ------------------------------------------------------------------ scene 1: you lock it, you throw the key
def key_pos(t):
    u = clamp((t + 0.35) / 2.15)
    return lerp(566, 668, u), lerp(1030, 1045, u) - 420 * 4 * u * (1 - u), u


def scene1(c, t, f, g):
    k = ease(seg(t, 0.6, 1.3)); z = lerp(1.9, 1.0, k); zb = lerp(1.12, 1.0, k)
    c.save(); c.translate(540, 930); c.scale(zb, zb); c.translate(-540, -930)
    paris_bg(c, f, g)
    c.restore()
    q = t - 2.35; crack = q >= 0
    sag = 12 * (1 - math.exp(-9 * q) * math.cos(22 * q)) if crack else 0
    fx, fy = lerp(587, 540, k), lerp(1122, 960, k)
    es = lerp(1.15, 0.95, k)
    hxw, hyw = 540, RT + 6
    bcy = hyw + 141 * es
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy + sag)
    deck(c, f)
    railing(c, f, g, [(-300, 1400, 3)], (-40, 360, 760, 1160), hole=(hxw, bcy - 10, 128 * es))
    gl = cairo.RadialGradient(hxw, bcy, 60 * es, hxw, bcy, 250 * es)
    gl.add_color_stop_rgba(0, 1, 1, 1, 0.6); gl.add_color_stop_rgba(1, 1, 1, 1, 0)
    c.set_source(gl); c.rectangle(hxw - 260, bcy - 260, 520, 520); c.fill()
    rrect(c, 380, RT - 16, 360, 30, 10); fs(c, IRON, 7)
    crackfx(c, 690, RT, q, f)
    kx, ky, ku = key_pos(t)
    sx = 540 + (hxw - fx) * z; sy = 960 + (bcy - fy) * z
    fear = (1 - seg(t, 1.2, 1.4)) + (1 - seg(q, 0.5, 0.9) if crack else 0)
    jx = 5 * math.sin(g * 41) * fear; jy = 4 * math.sin(g * 53 + 1) * fear
    if t < 1.85:
        d = math.hypot(kx - sx, ky - sy) + 1e-6; look = ((kx - sx) / d, (ky - sy) / d); face, eyes = 'o', 'big'
    elif not crack: look = (0.3, 0.8); face, eyes = 'flat', 'dot'
    else: look = (1, -0.5); face, eyes = 'o', 'big'
    if fear > 0.05: sweat(c, hxw + jx, bcy + jy, es * 1.5, g, f, n=5, a0=-2.9, da=0.42)
    lock(c, hxw + jx, hyw + jy, es, 'hero', f, face=face, eyes=eyes, rot=0.07 * math.sin(g * 30) * min(1, fear) + 0.05 * math.sin(g * 5), look=look, hang=True)
    thr = t < 1.1
    cdx = -90 * (1 - k)
    stick(c, 250 + cdx, 1420, 0.95, 'you', f, lh=(-62, -60), rh=(96 + 12 * math.sin(g * 9), -292) if thr else (64, -40), face='smile', eyes='closed',
          shirt=TEAL, bob=math.sin(g * 3) * 2)
    stick(c, 120 + cdx, 1420, 0.9, 'par', f, lh=(-50, -20), rh=(70, -63), face='smile', eyes='closed', shirt=PINK, bob=math.sin(g * 3 + 1) * 2)
    for i in range(2):
        hq = seg(t, 1.9 + i * 0.45, 3.3 + i * 0.45)
        if 0 < hq < 1: heart(c, 170 + i * 50, 1130 - 130 * hq, 0.9 + 0.25 * i, CORAL, 1 - ein(hq))
    c.restore()
    if t < 1.8:
        ks = lerp(1.7, 1.0, k)
        for i in range(3):
            kx2, ky2, _ = key_pos(t - 0.05 - 0.05 * i)
            wline(c, [(kx2 - 16 + i * 14, ky2 + 30), (kx2 - 22 + i * 14, ky2 + 64)], ('kl', i), f, lw=7, col=WHITE, amp=1.0, a=0.8 - 0.2 * i)
        keyobj(c, kx, ky, ks, g * 13, f)
    else:
        sq_ = seg(t, 1.8, 2.5)
        if sq_ < 1:
            for i in range(2):
                rr = 20 + 90 * sq_ + i * 34
                c.save(); c.translate(668, 1050); c.scale(1, 0.32); c.new_path(); c.arc(0, 0, rr, 0, 2 * math.pi); c.restore()
                rgb(c, WHITE, 0.9 * (1 - sq_)); c.set_line_width(6); c.stroke()
            for i in range(5):
                a = -math.pi * (0.2 + 0.6 * i / 4); d_ = 150 * sq_
                c.new_path(); c.arc(668 + math.cos(a) * d_, 1046 + math.sin(a) * d_ + 220 * sq_ * sq_, 8 * (1 - sq_) + 2, 0, 2 * math.pi)
                rgb(c, WHITE, 1 - sq_); c.fill()
    caption(c, t, -1, [[("WHERE DOES YOUR", CREAM)], [("PARIS LOVE LOCK GO?", GOLD)]], y=300, size=92, pop=False)


# ------------------------------------------------------------------ scene 2: one million locks, 45 tonnes
_conf = []


def confetti():
    if not _conf:
        r = random.Random(21)
        for _ in range(560): _conf.append((r.uniform(-40, W + 40), r.uniform(5, 55), r.uniform(9, 14), r.choice(LCOLS)))
    return _conf


def bridge_side(c, f, g, DY=960):
    for px in (-60, 300, 660, 1020):
        rrect(c, px - 36, DY + 30, 72, 300, 10); fs(c, STONE, 7)
        c.save(); c.translate(px, DY + 330); c.scale(1, 0.3); c.new_path(); c.arc(0, 0, 62 + 6 * math.sin(g * 3 + px), 0, 2 * math.pi); c.restore()
        rgb(c, WHITE, 0.6); c.set_line_width(5); c.stroke()
    for x0 in (-60, 300, 660, 1020):
        xc = x0 + 180
        for k in range(1, 8):
            x = x0 + k * 45; dx = (x - xc) / 150.0
            if abs(dx) < 1:
                c.new_path(); c.move_to(x, DY + 30); c.line_to(x, DY + 215 - 180 * math.sqrt(1 - dx * dx)); rgb(c, hx('3E7A70')); c.set_line_width(6); c.stroke()
        for lw, col in ((24, INK), (12, BRG)):
            c.new_path(); c.save(); c.translate(xc, DY + 215); c.scale(1, 1.2); c.arc(0, 0, 150, math.pi, 2 * math.pi); c.restore()
            rgb(c, col); c.set_line_width(lw); c.stroke()
    rrect(c, -40, DY, W + 80, 34, 8); fs(c, BRG, 7)
    c.rectangle(-40, DY - 60, W + 80, 60); rgb(c, hx('2F4F6B'), 0.4); c.fill()
    for (x, y, s, col) in confetti():
        c.rectangle(x, DY - 60 + y - s / 2, s, s * 0.9); rgb(c, col); c.fill()
    wline(c, [(-40, DY - 60), (W + 40, DY - 60)], 'brl', f, lw=7, amp=0.6)
    for k in range(9):
        a = math.sin(g * 5 + k * 1.9)
        if a > 0: sparkle(c, 60 + k * 118 + (k % 3) * 20, DY - 32 - (k % 2) * 12, 22 * a, WHITE, 0.95)


def boat(c, x, y, f, g):
    y += math.sin(g * 2.2) * 4
    for k in range(3):
        wline(c, [(x - 150 - k * 46, y + 22 + k * 5), (x - 124 - k * 46, y + 14 + k * 5)], ('wk', k), f, lw=6, col=WHITE, amp=1.2, a=0.8 - 0.2 * k)
    rrect(c, x - 70, y - 72, 130, 50, 10); fs(c, hx('BFE4F5'), 6)
    wpoly(c, [(x - 112, y - 26), (x + 124, y - 26), (x + 92, y + 22), (x - 92, y + 22)], 'bh', f); fs(c, WHITE, 7)
    c.rectangle(x - 96, y - 6, 196, 9); rgb(c, CORAL); c.fill()


def weight(c, x, y, s, f):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.arc(0, -6, 30, math.pi, 2 * math.pi); rgb(c, INK); c.set_line_width(16); c.stroke()
    wpoly(c, [(-84, 0), (84, 0), (118, 150), (-118, 150)], 'wt', f); fs(c, IRON, 9)
    txt(c, "45 T", 0, 106, 74, GOLD)
    c.restore()


def magnifier(c, f, g, cx, cy, r, shocked):
    wline(c, [(cx - r * 0.72, cy + r * 0.72), (cx - r * 1.35, cy + r * 1.35)], 'mgh', f, lw=40, col=INK, amp=0.6)
    wline(c, [(cx - r * 0.72, cy + r * 0.72), (cx - r * 1.35, cy + r * 1.35)], 'mgh2', f, lw=24, col=WOOD, amp=0.4)
    c.save(); c.new_path(); c.arc(cx, cy, r, 0, 2 * math.pi); c.clip()
    c.rectangle(cx - r, cy - r, 2 * r, 2 * r); c.set_source(grad(0, cy - r, 0, cy + r, [(0, RIV1), (1, RIV2)])); c.fill()
    c.save(); c.translate(cx, cy); c.scale(2.7, 2.7); c.translate(-200, -75)
    lockwall(c, 0, 0, 400, 150, 7, g, hole=(200, 82, 54))
    c.restore()
    sq = math.sin(g * 6)
    mini(c, cx - 176 + 9 * sq, cy + 26, 5.2, TEAL, -0.2 + 0.05 * sq); mini(c, cx + 176 - 9 * sq, cy + 34, 5.2, GOLD, 0.2 - 0.05 * sq)
    lock(c, cx + (4 * math.sin(g * 40) if shocked else 0), cy + 26, 1.08, 'hero', f, face='o' if shocked else 'flat', eyes='big',
         look=(0.5, -1) if shocked else (math.sin(g * 2.6), 0.2), sq=1 - 0.05 * abs(sq), rot=0.04 * sq)
    c.restore()
    c.new_path(); c.arc(cx, cy, r, 0, 2 * math.pi); rgb(c, INK); c.set_line_width(24); c.stroke()
    c.new_path(); c.arc(cx, cy, r, 0, 2 * math.pi); rgb(c, GOLD); c.set_line_width(11); c.stroke()
    c.new_path(); c.arc(cx, cy, r - 28, math.radians(200), math.radians(250)); rgb(c, WHITE, 0.75); c.set_line_width(10); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()


def scene2(c, t, f, g):
    paris_bg(c, f, g, tx=820, base=800, th=255)
    q = t - 2.64; landed = q >= 0
    sag = 16 * (1 - math.exp(-7 * q) * math.cos(20 * q)) if landed else 0
    c.save(); c.translate(0, sag)
    bridge_side(c, f, g, 960)
    pk = eback(seg(t, 2.1, 2.32))
    if pk > 0.01:
        wy = lerp(545, 750, ein(seg(t, 2.36, 2.64)))
        weight(c, 600, wy, pk, f)
        if landed and q < 0.4:
            for i in range(6):
                sg = -1 if i < 3 else 1; d_ = 130 + (i % 3) * 30 + 160 * q
                wcirc(c, 600 + sg * d_, 895 - (i % 3) * 14 - 40 * q, 20 * (1 - q / 0.4) + 4, ('pf', i), f, amp=2); rgb(c, WHITE, 0.9 * (1 - q / 0.4)); c.fill()
    c.restore()
    boat(c, lerp(600, 1010, seg(t, 0, 4.4)), 1440, f, g)
    mx, my = 340, 1395 + 5 * math.sin(g * 2)
    for i in range(7):
        u = i / 6
        c.new_path(); c.arc(lerp(mx + 40, 410, u), lerp(my - 232, 935 + sag, u), 6, 0, 2 * math.pi); rgb(c, INK, 0.85); c.fill()
    c.new_path(); c.arc(410, 930 + sag, 20, 0, 2 * math.pi); rgb(c, INK); c.set_line_width(7); c.stroke()
    magnifier(c, f, g, mx, my, 225, landed)
    n = int(round(lerp(0, 1000, ease(seg(t, 0.4, 1.75))))) * 1000
    caption(c, t, 0.25, [[("IT HANGS WITH", CREAM)], [(f"{n:,} LOCKS.", GOLD)]], y=300, size=90, t1=2.3)
    caption(c, t, 2.35, [[("TOGETHER:", CREAM)], [("45 TONNES.", GOLD)]], y=300, size=96)


# ------------------------------------------------------------------ scene 3: June 2014, the railing falls
def scene3(c, t, f, g):
    paris_bg(c, f, g)
    fall = ein(seg(t, 1.2, 1.78)); q = t - 1.78; down = q >= 0
    shake = 14 * math.exp(-8 * q) * math.sin(q * 60) if down and q < 0.6 else 0
    q2 = t - 3.55
    c.save(); c.translate(W / 2, H / 2 + shake); c.scale(1.2, 1.2); c.translate(-630, -1047)
    deck(c, f)
    hxw, hyw, es = 885, RT + 6, 0.95
    railing(c, f, g, [(-300, 360, 5), (760, 1500, 6)], (360, 760), hole=(hxw, hyw + 141 * es - 8, 138))
    rrect(c, 360, RB - 12, 400, 30, 10); fs(c, IRON, 7)
    crackfx(c, 818, RT, q2, f)
    # the passer-by
    px_ = lerp(120, 300, seg(t, 0.0, 1.1)); walking = t < 1.1; scared = 1.2 <= t < 3.0
    jump = 60 * math.sin(clamp(seg(t, 1.25, 1.7)) * math.pi)
    stick(c, px_, 1440 - jump, 0.9, 'pass', f, lh=(-110, -260) if scared else (-50, -20), rh=(110, -260) if scared else (56, -30),
          lf=(-45 + (18 * math.sin(g * 10) if walking else 0), 190), rf=(45 - (18 * math.sin(g * 10) if walking else 0), 190),
          face='o' if scared else 'smile', eyes='big' if scared else 'dot', shirt=BLUE, look=(1, 0.2), bob=abs(math.sin(g * 10)) * 6 if walking else 0)
    # the hero watches from the next section
    pre = seg(t, 0.35, 1.2)
    fear = pre if t < 3.0 else (1 if q2 >= 0 else 0.3)
    jx = 4 * math.sin(g * 41) * fear; jy = 3 * math.sin(g * 53 + 1) * fear
    if fear > 0.4: sweat(c, hxw, hyw + 141 * es, es, g, f, n=3, a0=-0.9, da=0.45)
    swing = 0.25 * math.exp(-3 * q2) * math.sin(q2 * 14) if q2 >= 0 else 0
    lock(c, hxw + jx, hyw + jy, es, 'hero', f, face='flat' if t < 1.2 else 'o', eyes='big', rot=swing + 0.04 * math.sin(g * 30) * fear,
         look=(-1, 0.1) if q2 < 0 else (-0.6, -1), hang=True)
    # the section that gives way
    wob = 0.035 * math.sin(g * 34) * pre * (1 - seg(t, 1.2, 1.3))
    sy = lerp(1.0, -0.58, fall)
    c.save(); c.translate(560, RB); c.rotate(wob); c.scale(1 + 0.14 * fall, sy if abs(sy) > 0.03 else 0.03); c.translate(-560, -RB)
    lockwall(c, 378, RT, 364, RB - RT, 9, g)
    rrect(c, 372, RT - 16, 376, 30, 10); fs(c, IRON, 7)
    rrect(c, 372, RT - 16, 14, RB - RT + 6, 6); fs(c, IRON, 5); rrect(c, 734, RT - 16, 14, RB - RT + 6, 6); fs(c, IRON, 5)
    c.restore()
    if 0.35 < t < 1.2:
        for i in range(4):
            a = math.sin(g * 20 + i * 2)
            wline(c, [(400 + i * 100, RT - 60 - 10 * a), (410 + i * 100, RT - 90 - 10 * a)], ('crk3', i), f, lw=7, col=WHITE, amp=1.0, a=0.9 * pre)
    if down and q < 0.7:
        for i in range(8):
            u = q / 0.7; xx = 330 + i * 66
            wcirc(c, xx + (i - 3.5) * 40 * u, RB + 200 - 80 * u - (i % 2) * 20, 34 * (1 - u) + 8, ('dust', i), f, amp=3); rgb(c, WHITE, 0.85 * (1 - u)); c.fill()
    c.restore()
    caption(c, t, 0.25, [[("JUNE 2014:", GOLD)], [("THE RAILING FALLS.", CREAM)]], y=300, size=90, t1=2.25)
    caption(c, t, 2.3, [[("2.4 METRES OF IT.", GOLD)], [("NOBODY IS HURT.", CREAM)]], y=300, size=90)


# ------------------------------------------------------------------ scene 4: 2015, Paris cuts them all off
def cutters(c, px, py, ang, op, f, s=1.0):
    """pivot at px, py. the jaws point along ang. op = how far open, 0 to 1"""
    c.save(); c.translate(px, py); c.rotate(ang); c.scale(s, s)
    for sg in (-1, 1):
        c.save(); c.rotate(sg * (0.07 + 0.2 * op))
        wline(c, [(0, 0), (-230, 0)], ('cth', sg), f, lw=26, col=INK, amp=0.5)
        wline(c, [(-6, 0), (-110, 0)], ('cts', sg), f, lw=13, col=STEEL, amp=0.3)
        wline(c, [(-110, 0), (-226, 0)], ('ctg', sg), f, lw=15, col=CORAL, amp=0.3)
        wpoly(c, [(0, sg * 2), (92, sg * 2), (76, sg * 30), (0, sg * 26)], ('ctj', sg), f, 1.0); fs(c, STEEL, 7)
        c.restore()
    c.new_path(); c.arc(0, 0, 15, 0, 2 * math.pi); fs(c, GOLD, 6)
    c.restore()


def clearpanel(c, x0, x1, g, f, shine=0.0):
    rrect(c, x0 + 22, RT + 16, x1 - x0 - 44, RB - RT - 30, 12); rgb(c, WHITE, 0.3); c.fill_preserve(); rgb(c, INK); c.set_line_width(7); c.stroke()
    c.save(); rrect(c, x0 + 22, RT + 16, x1 - x0 - 44, RB - RT - 30, 12); c.clip()
    for k in range(2):
        xx = x0 + 90 + k * 60 + shine * (x1 - x0)
        c.new_path(); c.move_to(xx, RT); c.line_to(xx + 34, RT); c.line_to(xx - 110, RB); c.line_to(xx - 144, RB); c.close_path(); rgb(c, WHITE, 0.5); c.fill()
    c.restore()


def barrow(c, x, y, f, front=True):
    """x, y = centre of the rim"""
    if not front:
        for i, (dx, dy, col) in enumerate(((-96, -8, TEAL), (92, -6, GOLD), (-44, -20, PINK), (50, -22, BLUE))):
            mini(c, x + dx, y + dy, 2.1, col, -0.3 + i * 0.2)
        return
    wline(c, [(x + 130, y + 16), (x + 250, y - 26)], 'bwh', f, lw=16, col=INK, amp=0.6)
    c.new_path(); c.arc(x - 40, y + 156, 38, 0, 2 * math.pi); fs(c, hx('3A3F4F'), 9)
    c.new_path(); c.arc(x - 40, y + 156, 11, 0, 2 * math.pi); rgb(c, STEEL); c.fill()
    wpoly(c, [(x - 150, y), (x + 150, y), (x + 108, y + 128), (x - 108, y + 128)], 'bwt', f); fs(c, GREEN, 9)
    wline(c, [(x - 150, y), (x + 150, y)], 'bwr', f, lw=14, col=INK, amp=0.5)


def scene4(c, t, f, g):
    paris_bg(c, f, g)
    c.save(); c.translate(470, 1300); c.scale(1.2, 1.2); c.translate(-470, -1300)
    deck(c, f)
    hxw, hyw, es = 500, RT + 6, 0.85
    railing(c, f, g, [(-300, 360, None), (360, 760, 11), (760, 1500, 12)], (-40, 360, 760, 1160), hole=(hxw, hyw + 141 * es - 8, 135), dens=0.26)
    lockwall(c, 778, RT, 364, RB - RT, 12, g)
    shine = seg(t, 2.5, 3.1)
    clearpanel(c, -40, 360, g, f, shine)
    snip = t >= 1.5; q = t - 1.5
    # the worker and the cutters
    wx = lerp(1260, 820, eout(seg(t, 0.0, 0.9)))
    walking = t < 0.9
    if t < 2.3:
        op = 1 - ease(seg(t, 1.3, 1.5)) * (1 - 0.6 * seg(t, 1.6, 1.9))
        pv = (wx - 202 + (26 * (1 - seg(t, 1.0, 1.3)) if t >= 0.9 else 26), 1176); ang = math.pi + 0.35
    else:
        u = ease(seg(t, 2.3, 2.8)); op = 0.2
        pv = lerp2((618, 1176), (wx - 112, 1150), u); ang = lerp(math.pi + 0.35, math.pi * 1.5, u)
    hands = []
    for sg in (-1, 1):
        a = ang + sg * (0.07 + 0.2 * op)
        hands.append(((pv[0] - 214 * math.cos(a) - wx) / 1.0, (pv[1] - 214 * math.sin(a) - 1420) / 1.0))
    hands.sort(key=lambda p: p[1])
    done = t >= 2.8
    stick(c, wx, 1420, 1.0, 'wrk', f, lh=hands[1] if not done else (-108, -50), rh=hands[0] if not done else (100 + 10 * math.sin(g * 9), -285),
          lf=(-45 + (18 * math.sin(g * 10) if walking else 0), 190), rf=(45 - (18 * math.sin(g * 10) if walking else 0), 190),
          face='flat' if t < 1.5 else 'smile', eyes='dot', shirt=ORANGE, look=(-1, -0.3), hat='cap', bob=abs(math.sin(g * 10)) * 6 if walking else math.sin(g * 3) * 2)
    # the hero
    bx, by0 = 500, 1440
    barrow(c, bx, by0, f, front=False)
    if not snip:
        fear = seg(t, 0.3, 0.9)
        if fear > 0.3: sweat(c, hxw, hyw + 141 * es, es, g, f, n=3, a0=-2.9, da=0.4)
        lock(c, hxw + 4 * math.sin(g * 41) * fear, hyw + 3 * math.sin(g * 53) * fear, es, 'hero', f, face='flat' if t < 1.0 else 'o', eyes='big',
             rot=0.05 * math.sin(g * 30) * fear, look=(1, -0.2), hang=True)
    else:
        u = ein(seg(t, 1.5, 2.0)); landed = t >= 2.0
        cy = lerp(hyw + 141 * es, 1378, u)
        sq = 1 - 0.16 * math.sin(clamp(seg(t, 2.0, 2.3)) * math.pi)
        lock(c, hxw, cy + (1 - sq) * 70, es, 'hero', f, face='o' if (not landed or 3.45 <= t < 4.0) else 'flat', eyes='big' if (t < 2.4 or 3.45 <= t < 4.0) else 'dot',
             rot=0.5 * math.sin(u * math.pi) + (0.06 * math.sin(g * 5) if landed else 0), look=(0, 1) if not landed else ((0.6, -0.4) if t < 3.0 else (-1, -0.1)), cut=True, sq=sq)
        if q < 0.4:
            for i in range(7):
                a = -math.pi * (0.05 + 0.9 * i / 6); r0 = 30 + 150 * q
                wline(c, [(552 + math.cos(a) * r0, 1176 + math.sin(a) * r0), (552 + math.cos(a) * (r0 + 34), 1176 + math.sin(a) * (r0 + 34))], ('spk', i), f, lw=8,
                      col=GOLD if i % 2 else WHITE, amp=0.6, a=1 - q / 0.4)
    barrow(c, bx, by0, f)
    cutters(c, pv[0], pv[1], ang, op, f)
    # a late lock bounces off the new panel
    if t > 3.0:
        u = seg(t, 3.0, 3.45)
        if u < 1: mx_, my_, mr = lerp(-80, 196, u), lerp(1040, 1250, u) - 90 * math.sin(u * math.pi), u * 3
        else:
            v = seg(t, 3.45, 4.2); mx_, my_, mr = 196 - 30 * math.sin(v * math.pi), lerp(1250, RB - 50, ein(v)), 3 + v * 2.2
        mini(c, mx_, my_, 3.0, PINK, mr)
        if 3.45 <= t < 3.75:
            w_ = (t - 3.45) / 0.3
            for i in range(5):
                a = -math.pi * (0.25 + 0.5 * i / 4) + math.pi * 0.5 * 0
                wline(c, [(196 + math.cos(a) * (40 + 60 * w_), 1230 + math.sin(a) * (40 + 60 * w_)), (196 + math.cos(a) * (64 + 70 * w_), 1230 + math.sin(a) * (64 + 70 * w_))],
                      ('tnk', i), f, lw=7, col=WHITE, amp=0.6, a=1 - w_)
    c.restore()
    caption(c, t, 0.25, [[("2015: PARIS CUTS", CREAM)], [("THEM ALL OFF.", GOLD)]], y=300, size=92, t1=2.35)
    caption(c, t, 2.4, [[("LOCK-PROOF PANELS", GOLD)], [("GO UP INSTEAD.", CREAM)]], y=300, size=90)


# ------------------------------------------------------------------ scene 5: 2017, the auction
def burst(c, x, y, r, k, f, label, rot=0.0):
    c.save(); c.translate(x, y); c.scale(k, k); c.rotate(rot)
    pts = []
    for i in range(24):
        a = math.pi * i / 12; rr = r if i % 2 == 0 else r * 0.74
        pts.append((math.cos(a) * rr, math.sin(a) * rr))
    wpoly(c, pts, 'burst', f, 1.5); fs(c, GOLD, 9)
    txt(c, label, 0, r * 0.16, r * 0.43, INK)
    c.restore()


def stand(c, f, g, x, y, face, eyes, look, es=0.72, rot=0.0):
    """wooden block with a bunch of locks on a rod. x = centre, y = top of the block"""
    rrect(c, x - 130, y, 260, 72, 12); fs(c, WOOD, 8)
    for lw, cl in ((24, INK), (12, STEEL)):
        c.new_path(); c.move_to(x - 100, y); c.line_to(x - 100, y - 188); c.arc(x - 60, y - 188, 40, math.pi, 1.5 * math.pi)
        c.line_to(x + 60, y - 228); c.arc(x + 60, y - 188, 40, 1.5 * math.pi, 2 * math.pi); c.line_to(x + 100, y)
        rgb(c, cl); c.set_line_width(lw); c.set_line_cap(cairo.LINE_CAP_BUTT); c.stroke()
    for i, (dx, dy, col) in enumerate(((-70, -176, TEAL), (70, -172, GOLD), (-58, -108, PINK), (60, -102, BLUE), (-72, -44, GREEN), (70, -40, PURPLE))):
        mini(c, x + dx, y + dy + 2 * math.sin(g * 4 + i), 1.75, col, 0.12 * math.sin(g * 3 + i * 1.3))
    lock(c, x, y - 222, es, 'hero', f, face=face, eyes=eyes, rot=rot + 0.05 * math.sin(g * 4), look=look, hang=True)


def paddle(c, x, y, k, col, f, key, wave=0.0):
    c.save(); c.translate(x, y + 260 * (1 - k)); c.rotate(wave)
    wline(c, [(0, 0), (0, 240)], (key, 's'), f, lw=20, col=INK, amp=0.5); wline(c, [(0, 0), (0, 240)], (key, 's2'), f, lw=9, col=WOOD, amp=0.3)
    c.new_path(); c.arc(0, -40, 58, 0, 2 * math.pi); fs(c, col, 8)
    heart(c, 0, -40, 0.62, WHITE)
    c.restore()


def scene5(c, t, f, g):
    bg(c, hx('F6E4C6'), hx('FFF3DD'))
    for i in range(4):
        rrect(c, 55 + i * 250, 650, 220, 470, 16); rgb(c, hx('EED6B0')); c.fill()
    c.save(); c.translate(480, 1650); c.scale(1.22, 1.22); c.translate(-480, -1650)
    c.rectangle(-200, 1190, W + 400, H - 1190); c.set_source(grad(0, 1190, 0, H, [(0, hx('B9794C')), (1, hx('8F5632'))])); c.fill()
    wline(c, [(-200, 1190), (W + 200, 1190)], 'wn', f, lw=7, amp=0.8)
    sold = t >= 2.85; q = t - 2.85
    # the auctioneer
    strike = ease(seg(t, 2.7, 2.85)) * (1 - 0.3 * math.sin(clamp(seg(t, 2.9, 3.3)) * math.pi))
    hand = lerp2((-120, -250), (-70, -150), strike)
    hd = stick(c, 815, 1250, 1.0, 'auc', f, lh=hand, rh=(70, -118), face='o' if 2.4 < t < 2.9 else 'smile', eyes='dot', shirt=IRON, look=(-1, 0.2),
               bob=math.sin(g * 3) * 2, legs=False)
    c.new_path(); c.move_to(hd[0] - 20, hd[1] + hd[2] + 16); c.line_to(hd[0], hd[1] + hd[2] + 30); c.line_to(hd[0] + 20, hd[1] + hd[2] + 16)
    c.line_to(hd[0] + 20, hd[1] + hd[2] + 44); c.line_to(hd[0], hd[1] + hd[2] + 30); c.line_to(hd[0] - 20, hd[1] + hd[2] + 44); c.close_path(); fs(c, CORAL, 5)
    gx, gy = 815 + hand[0], 1250 + hand[1]; ga = math.radians(lerp(-100, -186, strike))
    ex, ey = gx + 92 * math.cos(ga), gy + 92 * math.sin(ga)
    wline(c, [(gx, gy), (ex, ey)], 'gvh', f, lw=14, col=INK, amp=0.4)
    c.save(); c.translate(ex, ey); c.rotate(ga); rrect(c, -22, -40, 44, 80, 10); fs(c, WOODD, 7); c.restore()
    rrect(c, 670, 1140, 290, 520, 16); fs(c, WOODD, 9)
    rrect(c, 700, 1180, 230, 300, 12); rgb(c, hx('8F5632')); c.fill()
    rrect(c, 634, 1118, 110, 26, 8); fs(c, WOOD, 6)
    if 2.85 <= t < 3.15:
        for i in range(6):
            a = -math.pi * (0.1 + 0.8 * i / 5); r0 = 40 + 160 * q
            wline(c, [(670 + math.cos(a) * r0, 1112 + math.sin(a) * r0), (670 + math.cos(a) * (r0 + 30), 1112 + math.sin(a) * (r0 + 30))], ('gv', i), f, lw=8, col=INK,
                  amp=0.6, a=1 - q / 0.3)
    # the lot
    rrect(c, 230, 1210, 340, 460, 14); fs(c, WHITE, 8)
    rrect(c, 300, 1250, 200, 70, 12); fs(c, GOLD, 6); heart(c, 400, 1284, 0.6, CORAL)
    lk = (math.sin(g * 3), 0.4) if t < 1.05 else ((0.9, 0.9) if t < 2.85 else (0, 0))
    stand(c, f, g, 400, 1138, 'grin' if sold else ('o' if t > 1.05 else 'flat'), 'closed' if sold and q > 0.3 else 'big', lk,
          rot=0.1 * math.exp(-4 * q) * math.sin(q * 20) if sold else 0)
    # the room bids
    for i, (px_, t0, col) in enumerate(((690, 1.05, TEAL), (170, 1.4, CORAL), (880, 1.75, GOLD), (520, 2.1, PINK))):
        k = eback(seg(t, t0, t0 + 0.22))
        if sold and i != 1: k *= 1 - ease(seg(t, 2.95, 3.2))
        if k > 0.01: paddle(c, px_, 1420, k, col, f, ('pd', i), wave=0.14 * math.sin(g * (9 if (sold and i == 1) else 4) + i))
    for i, x in enumerate((110, 370, 630, 890)):
        c.new_path(); c.arc(x, 1640 + 5 * math.sin(g * 3 + i), 78, 0, 2 * math.pi); rgb(c, hx('2B2F3A')); c.fill()
        rrect(c, x - 120, 1700, 240, 300, 60); rgb(c, hx('2B2F3A')); c.fill()
    c.restore()
    if sold:
        burst(c, 640, 770, 122, eback(seg(t, 2.87, 3.12)), f, "SOLD!", rot=-0.12 + 0.05 * math.sin(g * 8))
    caption(c, t, 0.25, [[("2017: THE BEST ONES", CREAM)], [("GO TO AUCTION.", GOLD)]], y=300, size=88, t1=2.4)
    caption(c, t, 2.45, [[("150 BUNCHES GO", GOLD)], [("UNDER THE HAMMER.", CREAM)]], y=300, size=88)
    k = eout(seg(t, 3.25, 3.5))
    if k > 0:
        c.save(); c.translate(540, 575)
        rrect(c, -380, -38, 760, 74, 24); rgb(c, INK, 0.88 * k); c.fill()
        txt(c, "The rest were to be melted for scrap.", 0, 13, 40, CREAM, HAND, a=k)
        c.restore()


# ------------------------------------------------------------------ scene 6: the money
def shelter(c, f, x, y, col, lit, k=1.0):
    c.save(); c.translate(x, y); c.scale(k, k)
    wrect(c, -120, -250, 240, 250, ('sh', x), f); fs(c, col, 8)
    wpoly(c, [(-146, -250), (0, -362), (146, -250)], ('shr', x), f); fs(c, hx('D9705A'), 8)
    rrect(c, -36, -124, 72, 124, 10); fs(c, hx('2F9E8F'), 7)
    for sg in (-1, 1):
        rrect(c, sg * 76 - 26, -206, 52, 56, 8); fs(c, hx('FFE28A') if lit else hx('BFE4F5'), 6)
    heart(c, 0, -176, 0.62)
    c.restore()


HOUSES = ((200, hx('F7C9A8')), (540, hx('F3D7B0')), (880, hx('E9D9B8')))
GY = 1480


def scene6(c, t, f, g):
    bg(c, hx('BFE8F7'), hx('FFF1D6'))
    c.rectangle(0, GY, W, H - GY); c.set_source(grad(0, GY, 0, H, [(0, hx('A8D08D')), (1, hx('8FBF7A'))])); c.fill()
    wline(c, [(0, GY), (W, GY)], 'gr6', f, lw=7, amp=0.8)
    arr = [0, 0, 0]; last = [-9, -9, -9]; fly = []
    for i in range(9):
        t0 = 0.45 + i * 0.22; u = seg(t, t0, t0 + 0.75); hi = i % 3
        if u >= 1: arr[hi] += 1; last[hi] = max(last[hi], t0 + 0.75)
        elif u > 0: fly.append((i, u, hi))
    for hi, (x, col) in enumerate(HOUSES):
        b = 1.3 * (1 + 0.06 * math.sin(clamp((t - last[hi]) / 0.25) * math.pi))
        shelter(c, f, x, GY, col, arr[hi] > 0, b)
        if arr[hi] > 0:
            for j in range(2):
                hq = ((t - last[hi]) * 0.6 + j * 0.5) % 1.0
                if t > 2.5: heart(c, x - 100 + j * 200, 1040 - 130 * hq, 0.8, CORAL, math.sin(hq * math.pi))
    # people come out
    for i, (x, s, t0, sh) in enumerate(((368, 0.7, 2.9, TEAL), (430, 0.48, 3.0, GOLD), (712, 0.7, 3.15, PURPLE))):
        k = eback(seg(t, t0, t0 + 0.25))
        if k > 0.01:
            stick(c, x, GY - 190 * s * k, s * k, ('ppl', i), f, lh=(-60, -30), rh=(96 + 12 * math.sin(g * 9 + i), -290), face='grin', eyes='closed', shirt=sh,
                  bob=math.sin(g * 5 + i) * 3)
    # the hero on its stand
    rrect(c, 410, 902, 260, 62, 12); fs(c, WOOD, 8)
    lock(c, 540, 812 - 6 * abs(math.sin(g * 6)), 1.0, 'hero', f, face='grin', eyes='closed' if t > 2.6 else 'dot', look=(0, 1), rot=0.05 * math.sin(g * 6))
    for (i, u, hi) in fly:
        x = lerp(540, HOUSES[hi][0], u); y = lerp(760, 1080, u) - 150 * math.sin(u * math.pi)
        coin(c, x, y, 30, ('cn', i), f, face=None, flip=0.4 + 0.6 * abs(math.cos(u * 9 + i)))
    n = int(round(lerp(0, 250, ease(seg(t, 0.45, 2.0))))) * 1000
    caption(c, t, 0.25, [[("THE SALE RAISES", CREAM)], [(f"€{n:,}.", GOLD)]], y=300, size=92, t1=2.4)
    caption(c, t, 2.45, [[("IT GOES TO", CREAM)], [("3 REFUGEE CHARITIES.", GOLD)]], y=300, size=90)
    k = eout(seg(t, 0.7, 1.0))
    if k > 0:
        c.save(); c.translate(540, 556)
        rrect(c, -400, -34, 800, 112, 22); rgb(c, INK, 0.88 * k); c.fill()
        txt(c, "Sources: Guinness World Records, PBS NewsHour,", 0, 8, 28, CREAM, HAND, a=k)
        txt(c, "NPR, NBC News, The Connexion, Smithsonian Magazine.", 0, 54, 28, CREAM, HAND, a=k)
        c.restore()


# ------------------------------------------------------------------ scene 7: and the key?
def fish(c, x, y, s, f, g):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.translate(70, 0); c.rotate(math.sin(g * 9) * 0.25); wpoly(c, [(0, 0), (58, -44), (48, 0), (58, 44)], 'ft', f, 1.0); fs(c, ORANGE, 7); c.restore()
    wcirc(c, 0, 0, 86, 'fb', f, amp=2, ry=52); fs(c, ORANGE, 8)
    c.new_path(); c.arc(-44, -12, 16, 0, 2 * math.pi); rgb(c, WHITE); c.fill_preserve(); rgb(c, INK); c.set_line_width(5); c.stroke()
    c.new_path(); c.arc(-49, -9, 7, 0, 2 * math.pi); rgb(c, INK); c.fill()
    wline(c, [(-6, -30), (14, 0), (-6, 30)], 'fg', f, lw=6, col=INK, amp=0.5, a=0.35)
    c.restore()


def scene7(c, t, f, g):
    bg(c, hx('3A9DBB'), hx('12506B'))
    for i in range(4):
        x = 150 + i * 270 + 30 * math.sin(g * 0.6 + i)
        c.new_path(); c.move_to(x, 0); c.line_to(x + 100, 0); c.line_to(x - 80, 1500); c.line_to(x - 250, 1500); c.close_path(); rgb(c, WHITE, 0.07); c.fill()
    for i, x in enumerate((70, 150, 960, 1030)):
        pts = [(x + math.sin(g * 2 + j * 0.6 + i) * j * 6, 1470 - j * 44) for j in range(7)]
        wline(c, pts, ('wd', i), f, lw=18, col=hx('2F9E6A'), amp=1.0)
    c.new_path(); c.move_to(-20, 1470)
    for x in range(0, W + 80, 60): c.line_to(x, 1440 + 20 * math.sin(x / 140.0))
    c.line_to(W + 20, H + 20); c.line_to(-20, H + 20); c.close_path(); rgb(c, hx('CDB68C')); c.fill_preserve(); rgb(c, INK); c.set_line_width(7); c.stroke()
    for i, (x, y, r) in enumerate(((120, 1560, 26), (300, 1620, 18), (760, 1590, 30), (960, 1540, 20), (560, 1680, 24))):
        wcirc(c, x, y, r, ('pb', i), f, amp=2, ry=r * 0.7); fs(c, hx('B39B72'), 5)
    for i, (x, y, rot, col) in enumerate(((180, 1470, 0.5, STEEL), (860, 1486, -0.4, SHK), (700, 1530, 2.6, STEEL), (330, 1540, 3.4, hx('E0B45A')))):
        keyobj(c, x, y, 1.0, rot, f, col=col)
    for i in range(7):
        ph = (g * 0.22 + i * 0.37) % 1; x = 120 + (i * 149) % 860 + 14 * math.sin(g * 3 + i)
        c.new_path(); c.arc(x, 1450 - 900 * ph, 8 + (i % 3) * 5, 0, 2 * math.pi); rgb(c, WHITE, 0.5 * math.sin(ph * math.pi)); c.set_line_width(4); c.stroke()
    # the fish finds the key
    if t < 1.5: fxp, fyp = lerp(1300, 800, eout(seg(t, 0.1, 1.5))), 1280 + 14 * math.sin(g * 4)
    elif t < 2.2: fxp, fyp = 800 - 44 * math.sin(seg(t, 1.5, 1.8) * math.pi), 1284 + 16 * seg(t, 1.5, 1.7) + 8 * math.sin(g * 4)
    else: fxp, fyp = 800 + 70 * math.sin((t - 2.2) * 1.4), 1300 - 80 * (1 - math.cos((t - 2.2) * 1.4)) + 8 * math.sin(g * 4)
    nudged = t >= 1.65; qn = t - 1.65
    kr = -0.22 + (0.2 * math.exp(-3 * qn) * math.sin(qn * 16) if nudged else 0.02 * math.sin(g * 2))
    keyobj(c, 400, 1372 - (26 * math.sin(clamp(qn / 0.4) * math.pi) if nudged else 0), 3.0, kr, f, face='o' if 1.3 < t < 2.4 else ('smile' if t >= 2.9 else 'flat'),
           eyes='big' if 1.3 < t < 2.4 else ('closed' if t >= 2.9 else 'dot'), look=(1, -0.4))
    fish(c, fxp, fyp, 1.0, f, g)
    # it still thinks of the lock
    tk = eback(seg(t, 2.6, 2.9))
    if tk > 0.01:
        for i, (dx, dy, r) in enumerate(((462, 1222, 14), (520, 1140, 22))):
            k2 = eback(seg(t, 2.5 + i * 0.08, 2.7 + i * 0.08))
            c.new_path(); c.arc(dx, dy, r * k2, 0, 2 * math.pi); fs(c, WHITE, 6)
        c.save(); c.translate(640, 900 + 8 * math.sin(g * 2.5)); c.scale(tk, tk)
        for (dx, dy, r) in ((-120, 20, 90), (0, -30, 130), (120, 20, 92), (-50, 70, 96), (60, 74, 96)):
            c.new_path(); c.arc(dx, dy, r + 6, 0, 2 * math.pi); rgb(c, INK); c.fill()
        for (dx, dy, r) in ((-120, 20, 90), (0, -30, 130), (120, 20, 92), (-50, 70, 96), (60, 74, 96)):
            c.new_path(); c.arc(dx, dy, r, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
        lock(c, -30, 42, 0.74, 'hero', f, face='smile', eyes='closed' if int(g * 1.3) % 3 == 0 else 'dot', rot=0.05 * math.sin(g * 4))
        heart(c, 118, -22 - 8 * math.sin(g * 5), 0.9 + 0.1 * math.sin(g * 5), CORAL)
        c.restore()
    caption(c, t, 0.15, [[("AND THE KEY YOU", CREAM)], [("THREW IN THE SEINE?", GOLD)]], y=300, size=90, t1=2.05)
    caption(c, t, 2.1, [[("DID YOU EVER", CREAM)], [("LEAVE A LOVE LOCK?", GOLD)]], y=300, size=90)


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
