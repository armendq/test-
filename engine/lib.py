import cairocffi as cairo, math, random, os

# Shorts default to 1080x1920 at 30 fps. Long-form: STUDIO_W=1920 STUDIO_H=1080 (STUDIO_FPS=24 renders faster).
W, H, FPS, DUR = int(os.environ.get("STUDIO_W", 1080)), int(os.environ.get("STUDIO_H", 1920)), int(os.environ.get("STUDIO_FPS", 30)), 30.0
N = int(FPS * DUR)


def hx(h):
    h = h.lstrip('#')
    return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))


INK = hx('1E1B2E'); CREAM = hx('FFF6E5'); GOLD = hx('FFC83D'); GOLDD = hx('E39A12'); CORAL = hx('FF6B5A')
TEAL = hx('35C4C9'); TEALD = hx('0B5D73'); STONE = hx('F3E2C3'); STONED = hx('D8BF98'); SAND = hx('E6D2AE')
WOOD = hx('D49A6A'); WOODD = hx('A86F45'); WHITE = (1, 1, 1); ORANGE = hx('FF8A3D'); PINK = hx('FF9FB0')
GREEN = hx('5BBF6A'); BLUE = hx('4C8DF6'); SOUP = hx('FFA24D')
CAP = "Archivo Black"; HAND = "Comic Relief"


def clamp(x, a=0.0, b=1.0): return a if x < a else b if x > b else x
def seg(t, a, b): return clamp((t - a) / (b - a))
def ease(t): t = clamp(t); return t * t * (3 - 2 * t)
def eout(t): t = clamp(t); return 1 - (1 - t) ** 3
def ein(t): t = clamp(t); return t ** 3
def eback(t):
    t = clamp(t); c1 = 1.70158; c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2
def lerp(a, b, u): return a + (b - a) * u
def lerp2(p, q, u): return (lerp(p[0], q[0], u), lerp(p[1], q[1], u))


def jr(key, f, step=4):
    return random.Random(hash((key, f // step)))


def rgb(c, col, a=1.0): c.set_source_rgba(col[0], col[1], col[2], a)


def rrect(c, x, y, w, h, r):
    c.new_path()
    c.arc(x + w - r, y + r, r, -math.pi / 2, 0); c.arc(x + w - r, y + h - r, r, 0, math.pi / 2)
    c.arc(x + r, y + h - r, r, math.pi / 2, math.pi); c.arc(x + r, y + r, r, math.pi, 1.5 * math.pi); c.close_path()


def fs(c, fill, lw=8, ink=INK, a=1.0):
    rgb(c, fill, a); c.fill_preserve(); rgb(c, ink); c.set_line_width(lw)
    c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()


def blob(c, pts):
    n = len(pts)
    mids = [((pts[i][0] + pts[(i + 1) % n][0]) / 2, (pts[i][1] + pts[(i + 1) % n][1]) / 2) for i in range(n)]
    c.new_path(); c.move_to(*mids[-1])
    for i in range(n):
        p = pts[i]; m = mids[i]; x0, y0 = c.get_current_point()
        c.curve_to(x0 + 2 / 3 * (p[0] - x0), y0 + 2 / 3 * (p[1] - y0), m[0] + 2 / 3 * (p[0] - m[0]),
                   m[1] + 2 / 3 * (p[1] - m[1]), m[0], m[1])
    c.close_path()


def wcirc(c, x, y, r, key, f, amp=None, k=12, ry=None):
    if amp is None: amp = max(1.0, r * 0.035)
    rr = jr(key, f); ry = r if ry is None else ry
    pts = []
    for i in range(k):
        a = 2 * math.pi * i / k
        pts.append((x + (r + rr.uniform(-amp, amp)) * math.cos(a), y + (ry + rr.uniform(-amp, amp)) * math.sin(a)))
    blob(c, pts)


def wline(c, pts, key, f, lw=10, col=INK, amp=1.6, a=1.0):
    rr = jr(key, f)
    c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_join(cairo.LINE_JOIN_ROUND); c.set_line_width(lw); rgb(c, col, a)
    q = [(x + rr.uniform(-amp, amp), y + rr.uniform(-amp, amp)) for x, y in pts]
    c.new_path(); c.move_to(*q[0])
    for p in q[1:]: c.line_to(*p)
    c.stroke()


def wpoly(c, pts, key, f, amp=2.0):
    rr = jr(key, f)
    q = [(px + rr.uniform(-amp, amp), py + rr.uniform(-amp, amp)) for px, py in pts]
    c.new_path(); c.move_to(*q[0])
    for p in q[1:]: c.line_to(*p)
    c.close_path()


def wrect(c, x, y, w, h, key, f, amp=2.0):
    wpoly(c, [(x, y), (x + w, y), (x + w, y + h), (x, y + h)], key, f, amp)


def grad(x0, y0, x1, y1, stops):
    g = cairo.LinearGradient(x0, y0, x1, y1)
    for o, col in stops: g.add_color_stop_rgb(o, *col)
    return g


def bg(c, top, bot):
    c.set_source(grad(0, 0, 0, H, [(0, top), (1, bot)])); c.rectangle(0, 0, W, H); c.fill()


def tw(c, s, size, font=CAP):
    c.select_font_face(font); c.set_font_size(size); return c.text_extents(s)[4]


def txt(c, s, x, y, size, col=INK, font=CAP, anchor='c', a=1.0):
    c.select_font_face(font); c.set_font_size(size)
    adv = c.text_extents(s)[4]
    if anchor == 'c': x -= adv / 2
    elif anchor == 'r': x -= adv
    rgb(c, col, a); c.move_to(x, y); c.show_text(s); c.new_path()
    return adv


def caption(c, t, t0, lines, y=300, size=80, t1=None, pop=True):
    """lines: list of lists of (text, colour). Screen space."""
    if t < t0 or (t1 is not None and t > t1): return
    for i, segs in enumerate(lines):
        c.select_font_face(CAP); c.set_font_size(size)
        w = sum(c.text_extents(s)[4] for s, _ in segs)
        padx = 34; fit = min(1.0, (W - 90 - 2 * padx) / w)
        if fit < 1.0:
            size = size * fit; c.set_font_size(size); w = sum(c.text_extents(s)[4] for s, _ in segs)
        h = size * 1.3
        k = eback(seg(t, t0 + 0.07 * i, t0 + 0.07 * i + 0.25)) if pop else 1.0
        if t1 is not None: k *= 1 - ein(seg(t, t1 - 0.12, t1))
        if k <= 0.01: continue
        c.save(); c.translate(W / 2, y + i * (h + 16)); c.scale(k, k); c.rotate(math.radians(-1.6 if i % 2 == 0 else 1.2))
        rrect(c, -w / 2 - padx + 9, -h / 2 + 10, w + 2 * padx, h, 24); rgb(c, CORAL); c.fill()
        rrect(c, -w / 2 - padx, -h / 2, w + 2 * padx, h, 24); rgb(c, INK); c.fill()
        x = -w / 2
        for s, col in segs:
            rgb(c, col); c.move_to(x, size * 0.36); c.show_text(s); x += c.text_extents(s)[4]
        c.new_path(); c.restore()


def facef(c, x, y, r, face, look=(0, 0), eyes='dot'):
    ex = r * 0.36; ey = -r * 0.08; lx = look[0] * r * 0.12; ly = look[1] * r * 0.12
    c.set_line_cap(cairo.LINE_CAP_ROUND)
    if eyes == 'dot':
        rgb(c, INK)
        for sg in (-1, 1):
            c.new_path(); c.arc(x + sg * ex + lx, y + ey + ly, r * 0.095, 0, 2 * math.pi); c.fill()
    elif eyes == 'closed':
        rgb(c, INK); c.set_line_width(r * 0.1)
        for sg in (-1, 1):
            c.new_path(); c.arc(x + sg * ex, y + ey + r * 0.1, r * 0.15, math.pi * 1.15, math.pi * 1.85); c.stroke()
    elif eyes == 'big':
        for sg in (-1, 1):
            c.new_path(); c.arc(x + sg * ex, y + ey, r * 0.2, 0, 2 * math.pi)
            rgb(c, WHITE); c.fill_preserve(); rgb(c, INK); c.set_line_width(r * 0.06); c.stroke()
            c.new_path(); c.arc(x + sg * ex + lx, y + ey + ly, r * 0.095, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.set_line_width(r * 0.1); rgb(c, INK)
    my = y + r * 0.4
    if face == 'smile':
        c.new_path(); c.arc(x, my - r * 0.24, r * 0.34, math.radians(25), math.radians(155)); c.stroke()
    elif face == 'grin':
        c.new_path(); c.arc(x, my - r * 0.2, r * 0.36, 0, math.pi); c.close_path()
        rgb(c, CORAL); c.fill_preserve(); rgb(c, INK); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    elif face == 'o':
        c.save(); c.translate(x, my); c.scale(1, 1.3); c.new_path(); c.arc(0, 0, r * 0.15, 0, 2 * math.pi); c.restore()
        rgb(c, INK); c.fill()
    elif face == 'flat':
        c.new_path(); c.move_to(x - r * 0.2, my); c.line_to(x + r * 0.2, my); c.stroke()
    c.new_path()


def coin(c, x, y, r, key, f, face='smile', eyes='dot', flip=1.0, rot=0.0, sx=1.0, sy=1.0, look=(0, 0)):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(sx * max(0.1, abs(flip)), sy)
    lw = max(3.0, r * 0.11)
    wcirc(c, 0, 0, r, key, f); fs(c, GOLD, lw)
    c.new_path(); c.arc(0, 0, r * 0.76, 0, 2 * math.pi); rgb(c, GOLDD); c.set_line_width(lw * 0.6); c.stroke()
    c.new_path(); c.arc(0, 0, r * 0.58, math.radians(195), math.radians(245)); rgb(c, WHITE, 0.9)
    c.set_line_width(lw * 0.7); c.set_line_cap(cairo.LINE_CAP_ROUND); c.stroke()
    if flip > 0 and face:
        facef(c, 0, 0, r * 0.95, face, look, eyes)
    elif flip <= 0:
        txt(c, "1", 0, r * 0.3, r * 0.9, GOLDD)
    c.restore()


def stick(c, hxp, hyp, s, key, f, lh, rh, lf=(-45, 190), rf=(45, 190), face='smile', eyes='dot', shirt=CORAL,
          look=(0, 0), bob=0.0, hat=None, legs=True):
    P = lambda p: (hxp + p[0] * s, hyp + p[1] * s)
    if legs:
        for i, ft in enumerate((lf, rf)):
            sg = -1 if i == 0 else 1
            knee = (ft[0] * 0.5 + sg * 8, ft[1] * 0.5)
            wline(c, [P((sg * 10, 0)), P(knee), P(ft), P((ft[0] + sg * 24, ft[1]))], (key, 'leg', i), f, lw=13 * s)
    wline(c, [P((0, -8)), P((0, -128 + bob))], (key, 't1'), f, lw=60 * s, col=INK, amp=1.0)
    wline(c, [P((0, -8)), P((0, -128 + bob))], (key, 't2'), f, lw=44 * s, col=shirt, amp=0.6)
    for i, hd in enumerate((lh, rh)):
        sg = -1 if i == 0 else 1
        shp = (sg * 26, -124 + bob)
        el = ((shp[0] + hd[0]) / 2 + sg * 16, (shp[1] + hd[1]) / 2 + 14)
        wline(c, [P(shp), P(el), P(hd)], (key, 'arm', i), f, lw=12 * s)
        x, y = P(hd); c.new_path(); c.arc(x, y, 10 * s, 0, 2 * math.pi); rgb(c, CREAM); c.fill_preserve()
        rgb(c, INK); c.set_line_width(5 * s); c.stroke()
    x, y = P((0, -205 + bob)); hr = 54 * s
    wcirc(c, x, y, hr, (key, 'head'), f); fs(c, CREAM, 9 * s)
    facef(c, x, y, hr, face, look, eyes)
    if hat == 'chef':
        wcirc(c, x, y - hr * 1.05, hr * 0.8, (key, 'hat'), f, ry=hr * 0.55); fs(c, WHITE, 7 * s)
        wrect(c, x - hr * 0.7, y - hr * 0.95, hr * 1.4, hr * 0.35, (key, 'hat2'), f, 1.0); fs(c, WHITE, 7 * s)
    elif hat == 'cap':
        c.new_path(); c.arc(x, y - hr * 0.25, hr * 1.02, math.pi, 2 * math.pi); c.close_path(); fs(c, ORANGE, 7 * s)
        wline(c, [(x - hr * 1.5, y - hr * 0.25), (x + hr * 0.2, y - hr * 0.25)], (key, 'brim'), f, lw=10 * s)
    return (x, y, hr)


def heart(c, x, y, s, col=CORAL, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s); c.new_path()
    c.move_to(0, 30); c.curve_to(-60, -10, -30, -50, 0, -20); c.curve_to(30, -50, 60, -10, 0, 30); c.close_path()
    rgb(c, col, a); c.fill_preserve(); rgb(c, INK, a); c.set_line_width(5); c.stroke(); c.restore()


def sparkle(c, x, y, s, col=WHITE, a=1.0):
    c.new_path(); c.move_to(x, y - s); c.curve_to(x, y - s * 0.2, x + s * 0.2, y, x + s, y)
    c.curve_to(x + s * 0.2, y, x, y + s * 0.2, x, y + s); c.curve_to(x, y + s * 0.2, x - s * 0.2, y, x - s, y)
    c.curve_to(x - s * 0.2, y, x, y - s * 0.2, x, y - s); c.close_path(); rgb(c, col, a); c.fill()


def bowl(c, x, y, s, full=1.0, key='bowl', f=0):
    c.new_path(); c.arc(x, y, 60 * s, 0, math.pi); c.close_path(); fs(c, CREAM, 7 * s)
    c.save(); c.translate(x, y); c.scale(1, 0.28); c.new_path(); c.arc(0, 0, 60 * s, 0, 2 * math.pi); c.restore()
    fs(c, CREAM, 7 * s)
    if full > 0.02:
        c.save(); c.translate(x, y); c.scale(1, 0.28); c.new_path(); c.arc(0, 0, 50 * s * full, 0, 2 * math.pi); c.restore()
        rgb(c, SOUP); c.fill()


def steam(c, x, y, g, key, n=3, hgt=150, a=0.8, spread=34, lw=9):
    for i in range(n):
        ph = (g * 0.55 + i / n) % 1.0
        x0 = x + (i - (n - 1) / 2) * spread
        pts = []
        for j in range(9):
            u = j / 8
            yy = y - (ph * 0.6 + u * 0.5) * hgt
            xx = x0 + math.sin(u * 5 + g * 3 + i) * 12
            pts.append((xx, yy))
        al = a * math.sin(math.pi * ph)
        c.set_line_cap(cairo.LINE_CAP_ROUND); c.set_line_width(lw); rgb(c, WHITE, al)
        c.new_path(); c.move_to(*pts[0])
        for p in pts[1:]: c.line_to(*p)
        c.stroke()
