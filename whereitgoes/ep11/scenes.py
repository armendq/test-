from kit import *

DURATION = 24.0
RND = cairo.LINE_CAP_ROUND
WOOD = hx('E8BE7E'); WOODD = hx('B98552'); BARK = hx('6E4A2E'); LEAF = hx('3E8F5A'); LEAFD = hx('2C6B43')
TORII = hx('D9442B'); DUSKA = hx('2A2F55'); DUSKB = hx('C9705A')
_r = random.Random(5)
RACK = [(_r.uniform(-1, 1), _r.randint(0, 3), _r.choice((WOOD, hx('F0CC8E'), hx('DDB070'))), _r.uniform(-0.15, 0.15)) for _ in range(60)]


def ema(c, x, y, s, key, f, face='smile', eyes='dot', rot=0.0, look=(0, 0), writing=1.0, col=WOOD, faceon=True):
    """hero wish plaque, x, y = centre, about 260 x 200 (house shape)"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-40, -96); c.curve_to(-30, -150, 30, -150, 40, -96); rgb(c, RED); c.set_line_width(8); c.set_line_cap(RND); c.stroke()
    c.new_path(); c.move_to(-130, -40); c.line_to(0, -110); c.line_to(130, -40); c.line_to(130, 100); c.line_to(-130, 100); c.close_path(); fs(c, col, 10)
    c.new_path(); c.move_to(-112, -32); c.line_to(0, -92); c.line_to(112, -32); rgb(c, WOODD, 0.6); c.set_line_width(5); c.stroke()
    if writing > 0:
        for i in range(3):
            w = 130 * min(1, max(0, writing * 3 - i))
            if w > 2:
                c.new_path(); c.move_to(-65, -44 + i * 22)
                for k in range(int(w / 10)):
                    c.line_to(-65 + k * 10, -44 + i * 22 + 5 * math.sin(k * 1.7 + i))
                rgb(c, INK, 0.75); c.set_line_width(5); c.stroke()
    if faceon: facef(c, 0, 56, 54, face, look, eyes)
    c.restore()


def tiny(c, x, y, s, col, rot):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.move_to(-26, -8); c.line_to(0, -22); c.line_to(26, -8); c.line_to(26, 20); c.line_to(-26, 20); c.close_path(); rgb(c, col); c.fill_preserve(); rgb(c, INK); c.set_line_width(4); c.stroke()
    c.new_path(); c.move_to(-14, 2); c.line_to(12, 2); c.move_to(-14, 10); c.line_to(8, 10); rgb(c, INK, 0.5); c.set_line_width(2.5); c.stroke()
    c.restore()


def tree_rack(c, g, glow=0.0, rows=4, cx=540, base=1500):
    c.rectangle(cx - 70, 300, 140, base - 300); fs(c, BARK, 9)
    for i in range(5):
        c.new_path(); c.move_to(cx - 40 + i * 20, 340); c.line_to(cx - 44 + i * 20, base - 20); rgb(c, INK, 0.15); c.set_line_width(5); c.stroke()
    for (dx, dy, r) in ((-260, 220, 230), (0, 120, 270), (260, 220, 230), (-120, 330, 200), (140, 330, 200)):
        c.new_path(); c.arc(cx + dx, dy, r, 0, 2 * math.pi); rgb(c, LEAFD); c.fill()
    for (dx, dy, r) in ((-240, 200, 200), (10, 100, 240), (250, 200, 200)):
        c.new_path(); c.arc(cx + dx, dy, r, 0, 2 * math.pi); rgb(c, LEAF); c.fill()
    for row in range(rows):
        y = 900 + row * 140
        c.rectangle(80, y - 10, 920, 20); fs(c, hx('8A5A33'), 6)
        for (u, rr, col, rot) in RACK:
            if rr != row: continue
            x = 540 + u * 430
            tiny(c, x, y + 40, 1.0, col, rot + 0.04 * math.sin(g * 2 + u * 5))
    for x in (90, 990):
        c.rectangle(x - 14, 860, 28, base - 860); fs(c, hx('8A5A33'), 6)
    if glow > 0:
        for i in range(12):
            ph = (g * 0.5 + i / 12) % 1
            sparkle(c, 140 + (i * 83) % 800, 1460 - 600 * ph, 22 * math.sin(ph * math.pi), GOLD, glow)


def flames(c, x, y, s, g, a=1.0):
    c.save(); c.translate(x, y); c.scale(s, s)
    for (col, k) in ((hx('E8452C'), 1.0), (hx('FF9A2E'), 0.72), (hx('FFE06A'), 0.42)):
        c.new_path(); c.move_to(-180 * k, 0)
        for i in range(9):
            xx = -180 * k + i * 45 * k
            hh = (230 + 90 * math.sin(g * 9 + i * 1.7)) * k * (1 if i % 2 else 0.6)
            c.line_to(xx + 22 * k, -hh)
            c.line_to(xx + 45 * k, -20 * k)
        c.line_to(180 * k, 0); c.close_path(); rgb(c, col, a); c.fill()
    c.restore()


def sparks(c, x, y, g, n=14, a=1.0, w=300, h=700):
    for i in range(n):
        ph = (g * 0.7 + i / n) % 1
        c.new_path(); c.arc(x - w / 2 + (i * 97) % w + 30 * math.sin(ph * 7 + i), y - h * ph, 7 * (1 - ph) + 2, 0, 2 * math.pi); rgb(c, hx('FFD36A'), a * (1 - ph)); c.fill()


def torii(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    for sx in (-110, 110):
        c.rectangle(sx - 16, -300, 32, 300); fs(c, TORII, 6)
    c.new_path(); c.move_to(-190, -330); c.curve_to(-60, -310, 60, -310, 190, -330); c.line_to(180, -300); c.curve_to(60, -284, -60, -284, -180, -300); c.close_path(); fs(c, INK, 4)
    c.rectangle(-150, -260, 300, 26); fs(c, TORII, 6)
    c.restore()


def scene1(c, t, f, g):
    k = ease(seg(t, 0.7, 1.6)); z = lerp(2.2, 1.0, k)
    c.save(); cam(c, z, lerp(540, 540, k), lerp(1000, 960, k))
    bg(c, DUSKA, DUSKB)
    tree_rack(c, g)
    c.rectangle(0, 1500, W, 420); fs(c, hx('B9A68A'), 8)
    ema(c, 540, 1010 + 6 * math.sin(g * 3), 0.95, 'hero', f, face='o', eyes='big', rot=0.05 * math.sin(g * 4), look=(0, 1))
    sweat(c, 540, 960, 1.0, g, f)
    c.restore()
    fl = 0.5 + 0.5 * math.sin(g * 11)
    gl = cairo.LinearGradient(0, H, 0, H - 700)
    gl.add_color_stop_rgba(0, 1, 0.45, 0.15, 0.55 + 0.1 * fl); gl.add_color_stop_rgba(1, 1, 0.45, 0.15, 0)
    c.set_source(gl); c.rectangle(0, H - 700, W, 700); c.fill()
    sparks(c, 540, 1920, g, 10, 0.9, 900, 600)
    caption(c, t, -1, [[("YOUR WISH PLAQUE", CREAM)], [("ENDS UP IN A FIRE.", GOLD)]], y=300, size=88, pop=False)
    strip(c, 1700, ["Meiji Jingu, Tokyo"], seg(t, 1.0, 1.4), size=40)


def scene2(c, t, f, g):
    bg(c, hx('F6E7C8'), hx('EAD3A6'))
    c.rectangle(0, 1380, W, 540); fs(c, hx('8A5A33'), 9)
    wr = ease(seg(t, 0.6, 2.8))
    ema(c, 540, 1060, 1.9, 'hero', f, face='smile' if t > 2.8 else 'flat', eyes='dot', writing=wr, look=(1, -0.2))
    i = min(2, int(wr * 3)); px = -75 + 150 * min(1, max(0, wr * 3 - i))
    bx, by = 540 + px * 1.9 * 130 / 150, 1060 + (-44 + i * 22) * 1.9
    if wr < 1:
        c.save(); c.translate(bx, by); c.rotate(-0.6)
        rrect(c, -10, -190, 20, 180, 8); fs(c, INK, 4); c.new_path(); c.move_to(-10, -10); c.line_to(0, 14); c.line_to(10, -10); c.close_path(); rgb(c, INK); c.fill()
        c.restore()
    sign(c, 860, 700, "¥500", GOLD, INK, size=70, rot=0.08, k=eback(seg(t, 0.3, 0.6)))
    caption(c, t, 0.15, [[("FIRST, YOU WRITE A WISH", CREAM)], [("ON A WOODEN PLAQUE.", GOLD)]], y=300, size=76)
    strip(c, 1640, ["¥500, or ¥1,000 at New Year. Source: Meiji Jingu."], seg(t, 1.0, 1.4), size=34)


def scene3(c, t, f, g):
    bg(c, hx('9FD8F2'), hx('E9F8FF'))
    tree_rack(c, g)
    c.rectangle(0, 1500, W, 420); fs(c, hx('D8C7A6'), 8)
    hop = seg(t, 0.3, 1.5)
    x = lerp(540, 760, ease(hop)); y = lerp(1640, 1180, ease(hop)) - 220 * math.sin(hop * math.pi)
    ema(c, x, y + 4 * math.sin(g * 3), 0.55, 'hero', f, face='grin' if hop >= 1 else 'smile', eyes='dot', look=(1, -0.3) if hop < 1 else (0, 0), rot=0.1 * math.sin(g * 3))
    caption(c, t, 0.15, [[("YOU HANG IT AROUND", CREAM)], [("THE CAMPHOR TREE.", GOLD)]], y=300, size=82)
    strip(c, 1700, ["In front of the main shrine. Source: Meiji Jingu."], seg(t, 0.9, 1.3), size=34)


def scene4(c, t, f, g):
    dawn = ease(seg(t, 0.0, 2.6))
    top = tuple(lerp(a, b, dawn) for a, b in zip(hx('1F2550'), hx('F7B27A'))); bot = tuple(lerp(a, b, dawn) for a, b in zip(hx('3A3F70'), hx('FFE3A8')))
    bg(c, top, bot)
    c.new_path(); c.arc(540, 1500 - 380 * dawn, 120, 0, 2 * math.pi); rgb(c, hx('FFD98A')); c.fill()
    if dawn > 0.2:
        for i in range(12):
            a = i * math.pi / 6 + g * 0.2
            c.new_path(); c.move_to(540 + 150 * math.cos(a), 1500 - 380 * dawn + 150 * math.sin(a)); c.line_to(540 + 900 * math.cos(a), 1500 - 380 * dawn + 900 * math.sin(a)); rgb(c, hx('FFF0B8'), 0.12 * dawn); c.set_line_width(46); c.stroke()
    tree_rack(c, g, glow=dawn)
    c.rectangle(0, 1500, W, 420); fs(c, hx('D8C7A6'), 8)
    ema(c, 760, 1180 + 4 * math.sin(g * 3), 0.55, 'hero', f, face='grin', eyes='closed' if dawn > 0.6 else 'dot', look=(0, -0.5))
    caption(c, t, 0.15, [[("EVERY MORNING, PRIESTS", CREAM)], [("OFFER THE WISHES.", GOLD)]], y=300, size=80)
    strip(c, 1700, ["At the morning rite. Source: Meiji Jingu sign text, Japan Tourism Agency."], seg(t, 0.9, 1.3), size=30)


def scene5(c, t, f, g):
    bg(c, hx('1D1A30'), hx('4A2A3A'))
    c.rectangle(0, 1560, W, 360); fs(c, hx('3A3040'), 8)
    for i in range(5):
        c.save(); c.translate(540, 1560); c.rotate(-0.5 + i * 0.25); rrect(c, -230, -22, 460, 44, 20); fs(c, BARK, 6); c.restore()
    for i, (dx, rot) in enumerate(((-150, 0.4), (-40, -0.3), (80, 0.2), (170, -0.5))):
        tiny(c, 540 + dx, 1500 - 20 * (i % 2), 2.0, WOOD, rot)
    flames(c, 540, 1560, 1.6, g)
    rise = ease(seg(t, 0.8, 3.6))
    ema(c, 540, lerp(1150, 860, rise) + 6 * math.sin(g * 3), 0.7, 'hero', f, face='grin', eyes='closed', rot=0.05 * math.sin(g * 3), writing=1.0)
    sparks(c, 540, 1500, g, 22, 1.0, 700, 1100)
    caption(c, t, 0.15, [[("LATER, THE PLAQUES", CREAM)], [("GO INTO A RITUAL FIRE.", GOLD)]], y=300, size=80)
    strip(c, 1720, ["Source: Meiji Jingu sign text, Japan Tourism Agency."], seg(t, 0.9, 1.3), size=32)


def scene6(c, t, f, g):
    bg(c, hx('2A2F55'), hx('6A4A6A'))
    c.rectangle(0, 1440, W, 480); fs(c, hx('3A3040'), 8)
    for i, (x, s) in enumerate(((200, 0.8), (540, 1.0), (880, 0.8))):
        k = eback(seg(t, 0.2 + i * 0.3, 0.5 + i * 0.3))
        if k <= 0.01: continue
        torii(c, x, 1300, s * k)
        flames(c, x, 1440, 0.55 * s * k, g + i)
        sparks(c, x, 1400, g + i * 0.3, 8, k, 200, 500)
    caption(c, t, 0.15, [[("MANY SHRINES AND TEMPLES", CREAM)], [("BURN THEIR PLAQUES.", GOLD)]], y=300, size=74)
    strip(c, 1700, ["Often in rituals called ema kuyo. Source: National Geographic."], seg(t, 0.9, 1.3), size=32)


def scene7(c, t, f, g):
    bg(c, hx('FF7A5A'), hx('FFC83D'))
    hop = abs(math.sin(g * 5)) * 30
    ema(c, 540, 1180 - hop, 1.5, 'hero', f, face='grin', look=(0, -0.3), rot=0.05 * math.sin(g * 5))
    qmarks(c, ((200, 760, -0.3), (880, 800, 0.3), (230, 1400, 0.2)), t, 0.6)
    caption(c, t, 0.1, [[("WHAT WOULD", CREAM)], [("YOUR WISH SAY?", GOLD)]], y=300, size=96)


SCENES = [(0.0, 3.0, scene1), (3.0, 6.8, scene2), (6.8, 10.4, scene3), (10.4, 13.6, scene4), (13.6, 17.8, scene5), (17.8, 21.4, scene6), (21.4, 24.0, scene7)]
draw = make_draw(SCENES)
