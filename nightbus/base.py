from lib import *
import cairocffi as cairo

NAVY = hx('0B1026'); BUSY = hx('F2A93B'); BUSD = hx('D98A1F'); WARM = hx('FFE7A8'); CREAMT = hx('FFF1D6')
UNI = hx('3A5BA8'); UNID = hx('24345E'); FUR = hx('F4F1EA'); STRIPE = hx('2B2B33'); SHELL = hx('E08A4F'); SHELLD = hx('B8612E')
SLUG = hx('B7E3A8'); SEAT = hx('2FA39A'); SEATD = hx('1F7F78'); WALL = hx('3A4A7A'); CEIL = hx('2B3760'); FLOOR = hx('56608C')
SERIF = "Crimson Text"; SANS = "DM Sans"

_rs = random.Random(11)
STARS = [(_rs.uniform(0, W), _rs.uniform(0, 760), _rs.uniform(1.5, 4), _rs.random()) for _ in range(46)]
RAIN = [(_rs.random(), _rs.random(), _rs.uniform(0.7, 1.3)) for _ in range(70)]
BLD = [(x, _rs.uniform(260, 520), _rs.uniform(130, 200), [(_rs.random(), _rs.random()) for _ in range(6)]) for x in range(-40, 1100, 170)]


def cap2(c, t, t0, lines, y=250, size=74, t1=None, gold=False):
    if t < t0 or (t1 is not None and t > t1): return
    a = ease(seg(t, t0, t0 + 0.3))
    if t1 is not None: a *= 1 - ease(seg(t, t1 - 0.25, t1))
    c.select_font_face(SERIF, cairo.FONT_SLANT_NORMAL, cairo.FONT_WEIGHT_BOLD)
    for i, s in enumerate(lines):
        c.set_font_size(size); w = c.text_extents(s)[4]
        sz = size * min(1.0, (W - 150) / w); c.set_font_size(sz); w = c.text_extents(s)[4]
        yy = y + i * (size * 1.3) + (1 - a) * 18
        rrect(c, W / 2 - w / 2 - 32, yy - sz * 0.84, w + 64, sz * 1.2, 22); rgb(c, NAVY, 0.78 * a); c.fill()
        rgb(c, GOLD if gold else CREAMT, a); c.move_to(W / 2 - w / 2, yy); c.show_text(s); c.new_path()


def night(c, f, g, gy=1340, moon=True):
    bg(c, NAVY, hx('2A3470'))
    for (x, y, r, p) in STARS:
        a = 0.35 + 0.4 * math.sin(g * 2 + p * 6.28)
        c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); rgb(c, WHITE, max(0.1, a)); c.fill()
    if moon:
        gl = cairo.RadialGradient(850, 330, 40, 850, 330, 280)
        gl.add_color_stop_rgba(0, 1, 0.95, 0.75, 0.38); gl.add_color_stop_rgba(1, 1, 0.95, 0.75, 0)
        c.set_source(gl); c.rectangle(0, 0, W, 760); c.fill()
        wcirc(c, 850, 330, 80, 'moon', f, amp=1.5); rgb(c, hx('FFF3C4')); c.fill()
    for i, (x, h, w, wins) in enumerate(BLD):
        c.rectangle(x, gy - h, w, h); rgb(c, hx('1B2452')); c.fill()
        for (u, v) in wins:
            if (u + v + i * 0.37) % 1 < 0.55:
                c.rectangle(x + 14 + u * (w - 50), gy - h + 20 + v * (h - 90), 22, 30); rgb(c, hx('FFD98A'), 0.75); c.fill()
    c.rectangle(0, gy, W, H - gy); c.set_source(grad(0, gy, 0, H, [(0, hx('1C2347')), (1, hx('0D1230'))])); c.fill()
    c.rectangle(0, gy, W, 12); rgb(c, hx('3B4680')); c.fill()


def rain(c, g, a=0.42):
    c.set_line_width(3); c.set_line_cap(cairo.LINE_CAP_ROUND)
    for (u, v, sp) in RAIN:
        y = ((v + g * 0.9 * sp) % 1) * H; x = (u * W * 1.3 - y * 0.18) % W
        rgb(c, hx('BFD4FF'), a); c.new_path(); c.move_to(x, y); c.line_to(x - 7, y + 38); c.stroke()


def otto_head(c, x, y, R, key, f, eyes='open', mouth='smile', look=(0, 0), cap=True, tilt=0.0):
    c.save(); c.translate(x, y); c.rotate(tilt)
    for sg in (-1, 1):
        c.new_path(); c.arc(sg * R * 0.8, -R * 0.6, R * 0.27, 0, 2 * math.pi); fs(c, STRIPE, R * 0.07)
    wcirc(c, 0, 0, R * 1.06, (key, 'h'), f, amp=R * 0.012, ry=R * 0.92)
    path = c.copy_path(); fs(c, FUR, R * 0.08)
    c.save(); c.new_path(); c.append_path(path); c.clip()
    for sg in (-1, 1):
        c.save(); c.translate(sg * R * 0.47, -R * 0.12); c.rotate(sg * 0.2); c.scale(1, 2.7)
        c.new_path(); c.arc(0, 0, R * 0.3, 0, 2 * math.pi); c.restore(); rgb(c, STRIPE); c.fill()
    c.restore()
    c.new_path(); c.append_path(path); rgb(c, INK); c.set_line_width(R * 0.08); c.stroke()
    for sg in (-1, 1):
        ex, ey = sg * R * 0.45, -R * 0.08
        if eyes == 'closed':
            c.new_path(); c.arc(ex, ey - R * 0.04, R * 0.14, 0.15 * math.pi, 0.85 * math.pi)
            rgb(c, WHITE); c.set_line_width(R * 0.07); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
        else:
            r = R * (0.23 if eyes == 'wide' else 0.17)
            c.new_path(); c.arc(ex, ey, r, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
            c.new_path(); c.arc(ex + look[0] * r * 0.4, ey + look[1] * r * 0.4, r * (0.4 if eyes == 'wide' else 0.56), 0, 2 * math.pi)
            rgb(c, INK); c.fill()
            if eyes == 'sleepy':
                c.new_path(); c.arc(ex, ey, r * 1.08, math.pi, 2 * math.pi); c.close_path(); rgb(c, STRIPE); c.fill()
    c.save(); c.translate(0, R * 0.44); c.scale(1, 0.78); c.new_path(); c.arc(0, 0, R * 0.42, 0, 2 * math.pi); c.restore()
    rgb(c, WHITE); c.fill()
    c.save(); c.translate(0, R * 0.27); c.scale(1, 0.7); c.new_path(); c.arc(0, 0, R * 0.16, 0, 2 * math.pi); c.restore()
    rgb(c, INK); c.fill()
    rgb(c, INK); c.set_line_width(R * 0.06); c.set_line_cap(cairo.LINE_CAP_ROUND)
    my = R * 0.56
    if mouth == 'smile':
        c.new_path(); c.arc(0, my - R * 0.12, R * 0.2, 0.15 * math.pi, 0.85 * math.pi); c.stroke()
    elif mouth == 'flat':
        c.new_path(); c.move_to(-R * 0.15, my); c.line_to(R * 0.15, my); c.stroke()
    elif mouth == 'o':
        c.new_path(); c.arc(0, my + R * 0.02, R * 0.1, 0, 2 * math.pi); c.fill()
    if cap:
        c.new_path(); c.arc(0, -R * 0.56, R * 0.8, math.pi, 2 * math.pi); c.close_path(); fs(c, UNID, R * 0.07)
        c.rectangle(-R * 0.8, -R * 0.68, R * 1.6, R * 0.14); rgb(c, GOLD); c.fill()
        wline(c, [(-R * 0.98, -R * 0.53), (R * 0.98, -R * 0.53)], (key, 'brim'), f, lw=R * 0.13, col=INK, amp=0.6)
    c.restore()


def otto_full(c, x, y, s, key, f, eyes='open', mouth='smile', look=(0, 0), lh=(-98, 40), rh=(98, 40), bob=0.0, tilt=0.0):
    P = lambda p: (x + p[0] * s, y + p[1] * s)
    for sg in (-1, 1):
        wline(c, [P((sg * 38, -95)), P((sg * 42, -12))], (key, 'leg', sg), f, lw=40 * s, col=INK, amp=0.8)
        wline(c, [P((sg * 38, -95)), P((sg * 42, -14))], (key, 'leg2', sg), f, lw=28 * s, col=STRIPE, amp=0.5)
    bx, by = P((0, -175 + bob))
    wcirc(c, bx, by, 94 * s, (key, 'body'), f, amp=1.2, ry=114 * s); fs(c, UNI, 9 * s)
    for i in range(3):
        c.new_path(); c.arc(bx, by - 52 * s + i * 46 * s, 7 * s, 0, 2 * math.pi); rgb(c, GOLD); c.fill()
    for i, hd in enumerate((lh, rh)):
        sg = -1 if i == 0 else 1
        sh = (sg * 80, -232 + bob); hp = (hd[0], hd[1] - 175 + bob)
        wline(c, [P(sh), P(hp)], (key, 'arm', i), f, lw=42 * s, col=INK, amp=0.8)
        wline(c, [P(sh), P(hp)], (key, 'arm2', i), f, lw=30 * s, col=UNI, amp=0.5)
        hx_, hy_ = P(hp); c.new_path(); c.arc(hx_, hy_, 21 * s, 0, 2 * math.pi); fs(c, STRIPE, 6 * s)
    hx0, hy0 = P((0, -348 + bob))
    otto_head(c, hx0, hy0, 100 * s, (key, 'head'), f, eyes=eyes, mouth=mouth, look=look, tilt=tilt)


def snail(c, x, y, s, key, f, face=1, hat=True, ticket=False, hat_lift=0.0, happy=True, squash=1.0, look=(0, 0)):
    c.save(); c.translate(x, y); c.scale(face * s, s * squash)
    rrect(c, -80, -34, 172, 34, 17); fs(c, SLUG, 6)
    wline(c, [(70, -20), (84, -70)], (key, 'nk1'), f, lw=42, col=INK, amp=0.5)
    wline(c, [(70, -18), (84, -70)], (key, 'nk2'), f, lw=30, col=SLUG, amp=0.3)
    c.new_path(); c.arc(86, -84, 31, 0, 2 * math.pi); fs(c, SLUG, 6)
    if hat:
        c.save(); c.translate(86, -112 - hat_lift)
        c.new_path(); c.arc(0, 0, 24, math.pi, 2 * math.pi); c.close_path(); fs(c, STRIPE, 5)
        wline(c, [(-32, 0), (32, 0)], (key, 'hb'), f, lw=9, amp=0.4); c.restore()
    for i, ax in enumerate((70, 104)):
        tipx, tipy = ax + (i * 2 - 1) * 10, -158
        wline(c, [(ax, -104), (tipx, tipy)], (key, 'an', i), f, lw=6, amp=0.6)
        c.new_path(); c.arc(tipx, tipy, 12, 0, 2 * math.pi); fs(c, WHITE, 4)
        c.new_path(); c.arc(tipx + 2 + look[0] * 4, tipy + look[1] * 4, 5.5, 0, 2 * math.pi); rgb(c, INK); c.fill()
    rgb(c, INK); c.set_line_width(5); c.set_line_cap(cairo.LINE_CAP_ROUND); c.new_path()
    if happy: c.arc(96, -84, 12, 0.1 * math.pi, 0.8 * math.pi)
    else: c.move_to(90, -74); c.line_to(106, -74)
    c.stroke()
    c.new_path(); c.arc(-8, -80, 64, 0, 2 * math.pi); fs(c, SHELL, 7)
    c.new_path(); c.arc(-8, -80, 42, 0.3, 5.4); rgb(c, SHELLD); c.set_line_width(8); c.stroke()
    c.new_path(); c.arc(-4, -78, 21, 2.2, 7.0); c.stroke()
    if ticket:
        wline(c, [(112, -150), (134, -150)], (key, 'tk'), f, lw=6, amp=0.4)
        c.save(); c.translate(150, -158); c.rotate(0.22); c.rectangle(-24, -34, 48, 68); fs(c, CREAMT, 5)
        c.rectangle(-13, -18, 26, 7); rgb(c, CORAL); c.fill(); c.rectangle(-13, 0, 26, 5); rgb(c, INK, 0.5); c.fill(); c.restore()
    c.restore()


def bus_ext(c, f, g, x, y, s=1.0, door=1.0, stop=False, rot=0.0, otto=('open', 'smile'), key='bus', look=(0, 0), passenger=False):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.move_to(10, 330); c.line_to(-460, 480); c.line_to(-460, 300); c.close_path(); rgb(c, hx('FFE9A8'), 0.15); c.fill()
    rrect(c, 0, 0, 880, 420, 54); rgb(c, BUSY); c.fill()
    c.save(); rrect(c, 0, 0, 880, 420, 54); c.clip(); c.rectangle(0, 305, 880, 120); rgb(c, BUSD); c.fill(); c.restore()
    rrect(c, 0, 0, 880, 420, 54); rgb(c, INK); c.set_line_width(10); c.stroke()
    rrect(c, 300, -54, 280, 60, 16); fs(c, INK, 8); txt(c, "N1  NIGHT", 440, -12, 34, GOLD, SANS)
    for wx in (190, 340, 720):
        rrect(c, wx, 60, 120, 150, 18); fs(c, WARM, 8)
    rrect(c, 36, 60, 130, 150, 18); fs(c, WARM, 8)
    if otto:
        c.save(); rrect(c, 40, 64, 122, 142, 14); c.clip()
        otto_head(c, 102, 158, 50, (key, 'oh'), f, eyes=otto[0], mouth=otto[1], look=look); c.restore()
    if passenger:
        c.save(); rrect(c, 194, 64, 112, 142, 14); c.clip()
        snail(c, 256, 214, 0.56, (key, 'ps'), f, face=-1, look=(-1, -0.2)); c.restore()
    rrect(c, 490, 50, 200, 330, 14); fs(c, hx('FFF2CC') if door > 0.02 else BUSD, 8)
    w = 100 * (1 - door)
    if w > 2:
        for sx in (490, 690 - w):
            c.rectangle(sx, 50, w, 330); fs(c, hx('C97F1B'), 6)
    if stop:
        rrect(c, 352, 76, 96, 46, 10); rgb(c, hx('FF4D4D')); c.fill(); txt(c, "STOP", 400, 111, 30, WHITE, SANS)
    for wx in (170, 700):
        c.new_path(); c.arc(wx, 420, 64, 0, 2 * math.pi); fs(c, hx('20233A'), 10)
        c.new_path(); c.arc(wx, 420, 24, 0, 2 * math.pi); fs(c, hx('9AA3C7'), 6)
        c.save(); c.translate(wx, 420); c.rotate(rot); c.new_path(); c.move_to(-22, 0); c.line_to(22, 0)
        rgb(c, INK); c.set_line_width(6); c.stroke(); c.restore()
    c.new_path(); c.arc(16, 330, 20, 0, 2 * math.pi); fs(c, hx('FFF3C4'), 6)
    c.restore()


def stop_sign(c, f, x, gy, key='st'):
    wline(c, [(x, gy), (x, gy - 330)], (key, 'p'), f, lw=12, col=hx('9AA3C7'), amp=0.6)
    rrect(c, x - 62, gy - 420, 124, 96, 16); fs(c, GOLD, 8); txt(c, "N1", x, gy - 356, 52, INK, SANS)


def house(c, f, g, x, y, door=0.0, key='hs'):
    gl = cairo.RadialGradient(x, y - 90, 20, x, y - 90, 260)
    gl.add_color_stop_rgba(0, 1, 0.9, 0.6, 0.22 + 0.25 * door); gl.add_color_stop_rgba(1, 1, 0.9, 0.6, 0)
    c.set_source(gl); c.rectangle(x - 280, y - 380, 560, 420); c.fill()
    rrect(c, x - 70, y - 150, 140, 150, 30); fs(c, hx('FFF1D6'), 8)
    c.new_path(); c.arc(x, y - 150, 150, math.pi, 2 * math.pi); c.close_path(); fs(c, hx('E2504A'), 9)
    for (dx, dy, r) in [(-70, -205, 22), (30, -235, 28), (95, -185, 16), (-20, -180, 14)]:
        c.new_path(); c.arc(x + dx, y + dy, r, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
    c.new_path(); c.arc(x + 38, y - 100, 20, 0, 2 * math.pi); fs(c, hx('FFD98A'), 6)
    c.new_path(); c.move_to(x - 48, y); c.line_to(x - 48, y - 56); c.arc(x - 20, y - 56, 28, math.pi, 2 * math.pi); c.line_to(x + 8, y); c.close_path()
    fs(c, lerp2((0.55, 0.32), (1.0, 0.86), door) + (lerp(0.2, 0.5, door),), 6)


# ------------------------------------------------------------------ interior
DX = 620


def reflect(c, g, x0, x1, gy, n=6, depth=260):
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n + math.sin(g * 1.3 + k) * 6
        gl = cairo.LinearGradient(0, gy, 0, gy + depth)
        gl.add_color_stop_rgba(0, 1, 0.86, 0.5, 0.22); gl.add_color_stop_rgba(1, 1, 0.86, 0.5, 0)
        c.set_source(gl); c.rectangle(x - 26, gy + 6, 52, depth); c.fill()
    for k in range(4):
        ph = (g * 0.6 + k * 0.27) % 1
        c.save(); c.translate(x0 + (x1 - x0) * ((k * 0.31 + 0.1) % 1), gy + 90 + k * 55); c.scale(1, 0.3)
        c.new_path(); c.arc(0, 0, 10 + 50 * ph, 0, 2 * math.pi); c.restore()
        rgb(c, hx('BFD4FF'), 0.4 * (1 - ph)); c.set_line_width(3); c.stroke()


def bus_int_back(c, f, g, clock="23:58", moving=0.0, door=1.0, bars=True):
    c.rectangle(-900, -900, W + 2400, 1424); rgb(c, CEIL); c.fill()
    c.rectangle(-900, 524, W + 2400, 880); rgb(c, WALL); c.fill()
    wline(c, [(-900, 524), (W + 900, 524)], 'cl', f, lw=8, amp=0.6)
    for lx in (60, 660):
        gl = cairo.RadialGradient(lx + 90, 510, 10, lx + 90, 510, 400)
        gl.add_color_stop_rgba(0, 1, 0.93, 0.7, 0.26); gl.add_color_stop_rgba(1, 1, 0.93, 0.7, 0)
        c.set_source(gl); c.rectangle(lx - 320, 100, 820, 1000); c.fill()
        if bars:
            rrect(c, lx, 500, 180, 22, 11); rgb(c, hx('FFF2CC')); c.fill()
    wx = 330
    rrect(c, wx, 610, 230, 320, 26); fs(c, hx('121A40'), 9)
    c.save(); rrect(c, wx + 5, 615, 220, 310, 22); c.clip()
    for k in range(6):
        if moving > 0:
            xx = wx + ((k * 97 - g * 700 * moving) % 330) - 50
            c.rectangle(xx, 640 + k * 48, 70, 7); rgb(c, hx('FFD98A'), 0.7); c.fill()
        else:
            yy = 620 + ((k * 0.17 + g * 0.5) % 1) * 300
            c.new_path(); c.move_to(wx + 25 + k * 36, yy); c.line_to(wx + 21 + k * 36, yy + 24)
            rgb(c, hx('BFD4FF'), 0.5); c.set_line_width(3); c.stroke()
    c.restore()
    wline(c, [(290, 566), (600, 566)], 'rail', f, lw=12, col=GOLD, amp=0.6)
    for sx in (380, 500):
        wline(c, [(sx, 566), (sx, 600)], ('strap', sx), f, lw=6, col=GOLD, amp=0.4)
    if clock:
        rrect(c, 342, 416, 220, 72, 14); fs(c, INK, 6); txt(c, clock, 452, 471, 54, hx('FFB13D'), SANS)
    c.rectangle(-900, 1400, W + 2400, 1500); rgb(c, FLOOR); c.fill()
    c.rectangle(-900, 1476, W + 2400, 12); rgb(c, hx('6B76A6')); c.fill()
    sx = 370
    rrect(c, sx, 1010, 200, 250, 30); fs(c, SEATD, 8)
    rrect(c, sx - 10, 1220, 220, 90, 26); fs(c, SEAT, 8)
    wline(c, [(sx + 24, 1310), (sx + 24, 1400)], ('sl', sx), f, lw=12)
    wline(c, [(sx + 176, 1310), (sx + 176, 1400)], ('sr', sx), f, lw=12)
    c.save(); c.rectangle(DX, 580, 900, 820); c.clip()
    c.rectangle(DX, 580, 900, 820); c.set_source(grad(0, 580, 0, 1400, [(0, hx('0A0F24')), (1, hx('222D63'))])); c.fill()
    if door > 0.02:
        wline(c, [(DX + 262, 1400), (DX + 262, 900)], 'dp', f, lw=10, col=hx('9AA3C7'), amp=0.5)
        rrect(c, DX + 208, 806, 108, 84, 14); fs(c, GOLD, 7); txt(c, "N1", DX + 262, 864, 46, INK, SANS)
        for k in range(11):
            yy = 590 + ((k * 0.13 + g * 0.9) % 1) * 800
            c.new_path(); c.move_to(DX + 26 + (k * 53) % 340, yy); c.line_to(DX + 20 + (k * 53) % 340, yy + 34)
            rgb(c, hx('BFD4FF'), 0.45); c.set_line_width(3); c.stroke()
    if door < 0.98:
        px = DX + 500 * door
        rrect(c, px, 584, 560, 840, 16); fs(c, BUSD, 9)
        rrect(c, px + 44, 650, 210, 330, 18); fs(c, hx('121A40'), 8)
    c.restore()
    wline(c, [(DX, 1400), (DX, 580), (DX + 900, 580)], 'df', f, lw=10, amp=0.5)
    c.rectangle(DX, 1396, 900, 22); rgb(c, GOLD); c.fill()
    wline(c, [(-900, 1400), (DX, 1400)], 'fl', f, lw=8, amp=0.6)


def bus_int_front(c, f, g):
    rrect(c, -900, 1160, 1200, 250, 30); fs(c, hx('2A335F'), 9)
    wcirc(c, 262, 1100, 104, 'wheel', f, amp=1.0, ry=118); rgb(c, INK); c.set_line_width(24); c.stroke()
    c.new_path(); c.arc(262, 1100, 26, 0, 2 * math.pi); rgb(c, INK); c.fill()


def otto_seat(c, f, g, state, lt):
    wcirc(c, 150, 1150, 108, 'ob', f, amp=1.2, ry=140); fs(c, UNI, 9)
    for i in range(2):
        c.new_path(); c.arc(150, 1080 + i * 46, 7, 0, 2 * math.pi); rgb(c, GOLD); c.fill()
    if state == 0:
        wv = math.sin(g * 9) * 18
        wline(c, [(225, 1090), (318 + wv, 905)], 'oa', f, lw=40, col=INK, amp=0.8); wline(c, [(225, 1090), (318 + wv, 905)], 'oa2', f, lw=28, col=UNI, amp=0.5)
        c.new_path(); c.arc(318 + wv, 898, 22, 0, 2 * math.pi); fs(c, STRIPE, 6)
        otto_head(c, 150, 935, 98, 'oh', f, eyes='open', mouth='smile', look=(1, 0.2))
    elif state == 1:
        wline(c, [(225, 1090), (300, 1010)], 'oa', f, lw=40, col=INK, amp=0.8); wline(c, [(225, 1090), (300, 1010)], 'oa2', f, lw=28, col=UNI, amp=0.5)
        c.new_path(); c.arc(304, 1004, 22, 0, 2 * math.pi); fs(c, STRIPE, 6)
        c.new_path(); c.arc(286, 1030, 17, 0, 2 * math.pi); fs(c, GOLD, 5)
        otto_head(c, 150, 935, 98, 'oh', f, eyes='sleepy', mouth='flat', look=(0.9, 0.9), tilt=0.06)
    elif state in (2, 3):
        br = math.sin(g * 2.2) * 6
        otto_head(c, 186, 975 + br, 98, 'oh', f, eyes='closed', mouth='o', tilt=0.42)
        for k in range(3):
            ph = (g * 0.45 + k / 3) % 1
            txt(c, "z", 320 + ph * 110 + k * 8, 880 - ph * 190, 44 + ph * 44, CREAMT, SERIF, a=math.sin(ph * math.pi))
        if state == 3:
            rgb(c, WHITE, 0.6); c.set_line_width(3)
            for (x0, y0, x1, y1) in [(250, 880, 420, 524), (250, 880, 110, 524), (250, 880, 300, 1000), (210, 700, 330, 700), (180, 620, 370, 620)]:
                c.new_path(); c.move_to(x0, y0); c.line_to(x1, y1); c.stroke()
            sy = 700 + math.sin(g * 2) * 14
            c.new_path(); c.move_to(390, 524); c.line_to(390, sy); c.stroke()
            c.new_path(); c.arc(390, sy + 12, 13, 0, 2 * math.pi); rgb(c, INK); c.fill()
    else:
        otto_head(c, 150, 925 - 30 * math.sin(seg(lt, 0, 0.3) * math.pi), 98, 'oh', f, eyes='wide', mouth='o', look=(1, 0.3))


def int_cam(c):
    c.translate(-33.6, -128); c.scale(1.12, 1.12)


# ------------------------------------------------------------------ scenes
def scA(c, t, f, g):
    sx, sy = 676, 1412
    k = ease(seg(t, 1.0, 2.7)); z = lerp(2.5, 1.18, k); fx, fy = lerp(sx + 6, 540, k), lerp(sy - 150, 1100, k)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)
    night(c, f, g, 1340)
    stop_sign(c, f, 890, 1352)
    bus_ext(c, f, g, 100, 856, 1.0, door=1.0, otto=('open', 'smile'), look=(1, 0.6))
    reflect(c, g, 130, 950, 1340)
    c.new_path(); c.move_to(590, 1340); c.line_to(790, 1340); c.line_to(900, 1500); c.line_to(500, 1500); c.close_path()
    rgb(c, hx('FFE7A8'), 0.2); c.fill()
    snail(c, sx, sy, 0.8, 'sn', f, face=-1, ticket=True, squash=1 + 0.03 * math.sin(g * 6), look=(-1, -0.5))
    rain(c, g)
    c.restore()
    cap2(c, t, -1, ["The last bus of the night"], y=250, size=80, t1=2.35)
    cap2(c, t, 2.45, ["waits for one passenger."], y=250, size=80, gold=True)


BEATS = [(0.0, "23:58", None), (1.6, "00:19", "21 minutes later"), (3.3, "01:03", "One hour later"), (5.0, "02:47", "Almost three hours later")]
SNP = [805, 778, 735, 648]


def scB(c, t, f, g):
    i = max(k for k, b in enumerate(BEATS) if t >= b[0])
    tb, clk, lab = BEATS[i]; lt = t - tb
    c.save(); int_cam(c)
    bus_int_back(c, f, g, clk, door=1.0)
    otto_seat(c, f, g, i, lt)
    bus_int_front(c, f, g)
    snail(c, SNP[i] - min(lt, 1.7) * 6, 1400, 0.85, 'sn', f, face=-1, ticket=True, squash=1 + 0.04 * math.sin(g * 5),
          look=(-1, -0.4))
    if i == 3 and lt > 0.8:
        for k in range(3):
            ph = seg(lt, 0.8 + k * 0.12, 1.5 + k * 0.12)
            if 0 < ph < 1: sparkle(c, 590 + k * 46, 1215 - k * 40 - 30 * ph, 26 * math.sin(ph * math.pi), GOLD, 1)
    c.restore()
    if lab: cap2(c, t, tb + 0.05, [lab], y=235, size=76, t1=tb + (1.7 if i < 3 else 2.0), gold=(i == 3))
    if i > 0 and lt < 0.12:
        c.rectangle(0, 0, W, H); rgb(c, WHITE, 0.3 * (1 - lt / 0.12)); c.fill()


def scC(c, t, f, g):
    S = 0.9; X1, X2 = 532, 400
    door = 1 - ease(seg(t, 4.1, 4.7))
    c.save(); int_cam(c)
    bus_int_back(c, f, g, "02:48", door=door)
    if t < 0.5:
        otto_seat(c, f, g, 4, t); bus_int_front(c, f, g)
        snail(c, 638, 1400, 0.85, 'sn', f, face=-1, ticket=True, look=(-1, -0.4))
        txt(c, "!", 300, 810, 120, GOLD, SERIF)
        c.restore(); return
    bus_int_front(c, f, g)
    if t < 1.7: ox = lerp(250, X1, ease(seg(t, 0.5, 1.7))); walking = True
    elif t < 2.3: ox = X1; walking = False
    elif t < 3.3: ox = lerp(X1, X2, ease(seg(t, 2.3, 3.3))); walking = True
    else: ox = X2; walking = False
    bob = abs(math.sin(g * 10)) * 10 if walking else 0
    if t < 1.7: rh = (98, 40)
    elif t < 2.0: rh = lerp2((98, 40), (118, 150), ease(seg(t, 1.7, 2.0)))
    elif t < 2.3: rh = lerp2((118, 150), (100, 20), ease(seg(t, 2.0, 2.3)))
    elif t < 3.3: rh = (100, 20)
    elif t < 3.8: rh = lerp2((100, 20), (130, 30), ease(seg(t, 3.3, 3.8)))
    else: rh = lerp2((130, 30), (98, 40), ease(seg(t, 3.8, 4.1)))
    hand = (ox + rh[0] * S, 1400 + (rh[1] - 175 + bob) * S)
    if t < 2.0: sp = (638, 1400)
    elif t < 3.3: sp = (hand[0] + 12, hand[1] + 14)
    elif t < 3.8: sp = lerp2((hand[0] + 12, hand[1] + 14), (520, 1224), ease(seg(t, 3.3, 3.8)))
    else: sp = (520, 1224)
    lift = 30 * math.sin(seg(t, 4.0, 4.6) * math.pi)
    salute = ease(seg(t, 4.0, 4.3))
    lh = lerp2((-98, 40), (-70, -150), salute)
    otto_full(c, ox, 1400, S, 'of', f, eyes='open', mouth='smile', look=(1, 0.6) if t < 3.9 else (0.8, 0.2), lh=lh, rh=rh, bob=bob)
    snail(c, sp[0], sp[1], 0.85, 'sn', f, face=-1, ticket=(t < 2.0), hat_lift=lift, happy=(t > 2.3), look=(-1, -0.6))
    hq = seg(t, 4.1, 5.0)
    if 0 < hq < 1: heart(c, 545, 1040 - 70 * hq, 0.9, CORAL, 1 - ein(hq))
    c.restore()


TUFT = [(150, 1572), (455, 1580), (600, 1590), (210, 1640), (560, 1700), (120, 1760), (380, 1690), (700, 1640), (830, 1600), (900, 1730)]


def ext_world(c, f, g, bx, door, stop, rot, eyes, mouth, hdoor=0.0, passenger=False):
    night(c, f, g, 1180)
    for sx in (844, 574):
        wline(c, [(sx, 1215), (sx, 832)], ('sp', sx), f, lw=9, col=hx('9AA3C7'), amp=0.5)
        rrect(c, sx - 40, 770, 80, 62, 12); fs(c, GOLD, 6); txt(c, "N1", sx, 814, 34, INK, SANS)
    bus_ext(c, f, g, bx, 890, 0.6, door=door, stop=stop, rot=rot, otto=(eyes, mouth) if eyes else None, look=(1, 0.4),
            passenger=passenger)
    reflect(c, g, bx + 20, bx + 500, 1180, n=4, depth=40)
    c.rectangle(-300, 1215, W + 600, H); c.set_source(grad(0, 1215, 0, H, [(0, hx('24402F')), (1, hx('12241C'))])); c.fill()
    c.rectangle(-300, 1215, W + 600, 14); rgb(c, hx('4A5594')); c.fill()
    for i, (tx, ty) in enumerate(TUFT):
        for dx in (-14, 0, 14):
            sw = math.sin(g * 2 + i) * 3
            c.new_path(); c.move_to(tx + dx * 0.4, ty); c.line_to(tx + dx + sw, ty - 26 - (8 if dx == 0 else 0))
            rgb(c, hx('4E8A5B')); c.set_line_width(6); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    for (mx, my, r) in [(520, 1640, 26), (175, 1700, 20), (640, 1590, 16)]:
        c.rectangle(mx - r * 0.3, my - r * 0.9, r * 0.6, r * 0.9); fs(c, hx('FFF1D6'), 4)
        c.new_path(); c.arc(mx, my - r * 0.9, r, math.pi, 2 * math.pi); c.close_path(); fs(c, hx('E2504A'), 4)
    house(c, f, g, 300, 1560, hdoor)


def scD(c, t, f, g):
    mv = ease(seg(t, 0.5, 1.9)); bx = lerp(400, 130, mv)
    bx -= 8 * math.sin(seg(t, 1.9, 2.3) * math.pi)
    stop = t > 1.05
    c.save(); c.translate(W / 2, 1100); c.scale(1.3, 1.3); c.translate(-520, -1200)
    ext_world(c, f, g, bx, ease(seg(t, 2.5, 3.1)), stop and t < 3.4, -(400 - bx) / 38.0, 'sleepy' if stop else 'open',
              'flat' if stop else 'smile', passenger=True)
    if stop and t < 1.9:
        for k in range(3):
            ph = seg(t, 1.05 + k * 0.08, 1.5 + k * 0.08)
            c.new_path(); c.arc(bx + 240, 950, 40 + 70 * ph, -2.4, -0.7); rgb(c, hx('FF4D4D'), 0.9 * (1 - ph)); c.set_line_width(7); c.stroke()
    rain(c, g)
    c.restore()
    cap2(c, t, 0.15, ["Next stop:"], y=250, size=80)
    cap2(c, t, 1.95, ["nine metres later."], y=354, size=80, gold=True)


BABY = [(338, 1566), (318, 1582), (362, 1586)]


def scE(c, t, f, g):
    k = ease(seg(t, 0.0, 0.8)); z = lerp(1.3, 2.05, k)
    c.save(); c.translate(W / 2, lerp(1100, 1180, k)); c.scale(z, z); c.translate(-lerp(520, 400, k), -lerp(1200, 1425, k))
    hd = ease(seg(t, 1.8, 2.2))
    ext_world(c, f, g, 130, 1.0, False, 0, None, None, hd)
    S = 0.62
    w = ease(seg(t, 0.0, 0.9)); ox, oy = lerp(484, 505, w), lerp(1240, 1566, w)
    bob = abs(math.sin(g * 10)) * 8 if t < 0.9 else 0
    if t < 1.0: rh = (-98, 10)
    elif t < 1.8: rh = lerp2((-98, 10), (-128, 150), ease(seg(t, 1.0, 1.8)))
    else: rh = lerp2((-128, 150), (-98, 40), ease(seg(t, 1.9, 2.3)))
    hand = (ox + rh[0] * S, oy + (rh[1] - 175 + bob) * S)
    sal = ease(seg(t, 3.9, 4.2))
    lh = lerp2((98, 40), (72, -150), sal)
    a = seg(t, 0.0, 0.25)
    if a < 1: c.push_group()
    otto_full(c, ox, oy, S, 'of', f, eyes='open' if t < 4.4 else 'closed', mouth='smile', look=(-1, 0.7), lh=rh, rh=lh, bob=bob)
    if t < 1.8: sp = (hand[0] - 8, hand[1] + 12)
    else: sp = (412, 1566)
    for i, (bxp, byp) in enumerate(BABY):
        q = seg(t, 2.25 + i * 0.22, 2.75 + i * 0.22); u = eback(q)
        if q > 0:
            px, py = lerp(300, bxp, u), lerp(1560, byp, u) - 26 * math.sin(q * math.pi) - abs(math.sin(g * 7 + i)) * 5
            snail(c, px, py, 0.26, ('bb', i), f, face=1, hat=False)
    facing = -1 if t < 3.2 else 1
    snail(c, sp[0], sp[1], 0.46, 'sn', f, face=facing, hat_lift=22 * math.sin(seg(t, 3.3, 3.9) * math.pi), look=(1, -0.6))
    if a < 1: c.pop_group_to_source(); c.paint_with_alpha(a)
    for i in range(3):
        hq = seg(t, 2.6 + i * 0.35, 4.0 + i * 0.35)
        if 0 < hq < 1: heart(c, 330 + i * 34, 1440 - 110 * hq, 0.45 + 0.1 * i, CORAL, 1 - ein(hq))
    rain(c, g, 0.3)
    c.restore()
    cap2(c, t, 3.3, ["Every passenger gets home."], y=250, size=78, gold=True)


def scF(c, t, f, g):
    zz = 1 + 0.07 * ease(seg(t, 2.15, 4.5))
    c.save(); c.translate(700, 720); c.scale(zz, zz); c.translate(-700, -720)
    c.save(); c.translate(430, 1080); c.scale(1.75, 1.75); c.translate(-150, -960)
    bus_int_back(c, f, g, None, moving=1.0, door=0.0, bars=False)
    scared = t > 2.15
    wcirc(c, 150, 1150, 108, 'ob', f, amp=1.2, ry=140); fs(c, UNI, 9)
    for i in range(2):
        c.new_path(); c.arc(150, 1080 + i * 46, 7, 0, 2 * math.pi); rgb(c, GOLD); c.fill()
    jump = 26 * math.sin(seg(t, 2.15, 2.5) * math.pi)
    if scared: otto_head(c, 150 + math.sin(g * 44) * 2.4, 935 - jump, 98, 'oh', f, eyes='wide', mouth='o', look=(0.9, -0.9))
    elif t > 1.85: otto_head(c, 150, 935, 98, 'oh', f, eyes='open', mouth='flat', look=(0.9, -0.9))
    else: otto_head(c, 150 + math.sin(g * 4) * 5, 935, 98, 'oh', f, eyes='closed', mouth='smile', tilt=math.sin(g * 4) * 0.06)
    bus_int_front(c, f, g)
    wline(c, [(215, 1085), (262, 1010)], 'oa', f, lw=40, col=INK, amp=0.8); wline(c, [(215, 1085), (262, 1010)], 'oa2', f, lw=28, col=UNI, amp=0.5)
    c.new_path(); c.arc(264, 1004, 22, 0, 2 * math.pi); fs(c, STRIPE, 6)
    if scared:
        for k in range(3):
            ph = (g * 1.4 + k / 3) % 1
            c.new_path(); c.arc(60 + k * 14, 800 + ph * 90, 7 * (1 - ph) + 3, 0, 2 * math.pi); rgb(c, hx('BFE4FF'), 0.9 * (1 - ph)); c.fill()
    c.restore()
    if t < 1.85:
        for k in range(3):
            ph = (g * 0.6 + k / 3) % 1
            x, y = 600 + k * 50 + ph * 60, 1010 - ph * 170
            c.new_path(); c.arc(x, y, 15, 0, 2 * math.pi); rgb(c, CREAMT, math.sin(ph * math.pi)); c.fill()
            c.new_path(); c.move_to(x + 13, y); c.line_to(x + 13, y - 52); c.line_to(x + 36, y - 44)
            c.set_line_width(6); rgb(c, CREAMT, math.sin(ph * math.pi)); c.stroke()
    wline(c, [(790, 318), (790, 494)], 'mir', f, lw=14, amp=0.4)
    rrect(c, 548, 482, 484, 286, 44); fs(c, hx('C9CFE6'), 10)
    rrect(c, 574, 508, 432, 234, 26); fs(c, hx('0A0F24'), 8)
    c.save(); rrect(c, 578, 512, 424, 226, 22); c.clip()
    for sx in (610, 760, 910):
        rrect(c, sx - 60, 624, 120, 200, 24); rgb(c, hx('1B2550')); c.fill()
    c.new_path(); c.move_to(600, 742); c.line_to(690, 508); c.line_to(730, 508); c.line_to(640, 742); c.close_path(); rgb(c, WHITE, 0.07); c.fill()
    blink = (2.9 < t < 3.02) or (3.92 < t < 4.04)
    e = ease(seg(t, 1.5, 1.8)) * (0.12 if blink else 1.0)
    px = -9 * ease(seg(t, 3.15, 3.5))
    if e > 0:
        for sg in (-1, 1):
            c.save(); c.translate(790 + sg * 44, 620); c.scale(1, max(0.05, e)); c.new_path(); c.arc(0, 0, 26, 0, 2 * math.pi); c.restore()
            rgb(c, hx('FFE14D')); c.fill()
            c.save(); c.translate(790 + sg * 44 + px, 620); c.scale(0.3, max(0.05, e)); c.new_path(); c.arc(0, 0, 22, 0, 2 * math.pi); c.restore()
            rgb(c, INK); c.fill()
    c.restore()
    c.restore()
    cap2(c, t, 2.3, ["Who is in the back seat?"], y=250, size=84, gold=True)
    cap2(c, t, 3.0, ["Fox, owl or ghost? You pick."], y=360, size=72)


SCENES = [(0.0, 4.0, scA), (4.0, 11.0, scB), (11.0, 16.0, scC), (16.0, 20.0, scD), (20.0, 25.5, scE), (25.5, 30.0, scF)]


def draw(c, g, f):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= g < b or (i == len(SCENES) - 1 and g >= b):
            c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, g - a, f, g); c.restore()
            fa = 1 - seg(g - a, 0, 0.18)
            if i > 0 and fa > 0 and fn is not scE:
                c.rectangle(0, 0, W, H); rgb(c, NAVY, fa); c.fill()
            return
