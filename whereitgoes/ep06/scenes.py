from kit import *

DURATION = 24.0
GUMC = (hx('FF6FA8'), hx('7FD1FF'), hx('FFD23D'), hx('8BE07A'), hx('C59BFF'), hx('FF8A5B'), WHITE)
BRICK = hx('B5553C'); BRICKD = hx('8E3F2C'); MORTAR = hx('D9B9A0')
_r = random.Random(11)
DOTS = [(_r.uniform(40, 1040), _r.uniform(420, 1470), _r.uniform(13, 26), _r.choice(GUMC), _r.random()) for _ in range(420)]


def gum(c, x, y, s, key, f, face='smile', eyes='dot', rot=0.0, look=(0, 0), sq=1.0, col=hx('FF6FA8')):
    """hero gum wad, x, y = centre, about 200 x 150"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s * (2 - sq), s * sq)
    wpoly(c, [(-96, -10), (-80, -62), (-30, -80), (20, -76), (74, -60), (100, -14), (90, 44), (40, 72), (-20, 74), (-78, 52)], (key, 'g'), f, 1.6); fs(c, col, 10)
    c.new_path(); c.arc(-40, -40, 16, 0, 2 * math.pi); rgb(c, WHITE, 0.45); c.fill()
    facef(c, 4, 4, 70, face, look, eyes)
    c.restore()


def brickwall(c, f, g, x0=0, x1=W, y0=380, y1=1480, gumk=1.0, clean_rect=None, heart=False, bricks=True):
    if x0 == 0:
        c.rectangle(-600, -600, W + 1200, y0 + 600); rgb(c, hx('3B3550')); c.fill()
        for i in range(6):
            rrect(c, 40 + i * 180, 120, 110, 150, 10); rgb(c, hx('FFD98A') if i % 2 == 0 else hx('5A5478')); c.fill()
        c.rectangle(-600, y0 - 26, W + 1200, 26); rgb(c, hx('2A2540')); c.fill()
    c.rectangle(x0, y0, x1 - x0, y1 - y0); rgb(c, BRICK); c.fill()
    if bricks:
        for r in range(int((y1 - y0) / 62) + 1):
            y = y0 + r * 62
            c.rectangle(x0, y, x1 - x0, 6); rgb(c, MORTAR, 0.7); c.fill()
            off = 0 if r % 2 else 70
            for k in range(-1, int((x1 - x0) / 140) + 2):
                c.rectangle(x0 + off + k * 140, y, 6, 62); rgb(c, MORTAR, 0.7); c.fill()
    for i, (x, y, r, col, ph) in enumerate(DOTS):
        if not (x0 <= x <= x1 and y0 <= y <= y1): continue
        if ph > gumk: continue
        if clean_rect and clean_rect[0] <= x <= clean_rect[2] and clean_rect[1] <= y <= clean_rect[3]: continue
        c.new_path(); c.arc(x, y, r, 0, 2 * math.pi); rgb(c, col); c.fill_preserve(); rgb(c, INK, 0.55); c.set_line_width(3); c.stroke()


def alley_floor(c):
    c.rectangle(0, 1480, W, 440); rgb(c, hx('6C6A78')); c.fill()
    c.move_to(0, 1480); c.line_to(W, 1480); rgb(c, INK); c.set_line_width(9); c.stroke()
    for i in range(8):
        c.rectangle(i * 150 - 20, 1530, 120, 8); rgb(c, hx('59576A')); c.fill()


def scene1(c, t, f, g):
    stick_t = 1.9
    k = ease(seg(t, 0.55, 1.35)); z = lerp(1.85, 1.0, k)
    c.save(); cam(c, z, lerp(560, 540, k), lerp(980, 960, k))
    brickwall(c, f, g)
    alley_floor(c)
    stick(c, 250, 1480 - 190, 1.0, 'you', f, lh=(-60, -20), rh=(lerp(150, 250, ease(seg(t, 1.2, stick_t))), lerp(-280, -330, ease(seg(t, 1.2, stick_t)))) if t < 2.5 else (150, -200),
          face='smile', eyes='closed', shirt=TEAL, look=(1, -0.3))
    hx_ = lerp(430, 540, ease(seg(t, 1.2, stick_t))); hy_ = lerp(840, 820, ease(seg(t, 1.2, stick_t)))
    sq = 1.0 if t < stick_t else lerp(0.62, 0.9, eback(seg(t, stick_t, stick_t + 0.35)))
    if t < stick_t: sweat(c, hx_, hy_ - 40, 1.0, g, f)
    gum(c, hx_ + (4 * math.sin(g * 41) if t < stick_t else 0), hy_, 0.95, 'hero', f, face='o', eyes='big', look=(1, 0) if t < stick_t else (0, -0.6), sq=sq)
    if stick_t <= t < stick_t + 0.3:
        q = (t - stick_t) / 0.3
        for i in range(8):
            a = i * math.pi / 4
            wline(c, [(hx_ + 110 * math.cos(a), hy_ + 90 * math.sin(a)), (hx_ + (150 + 40 * q) * math.cos(a), hy_ + (120 + 40 * q) * math.sin(a))], ('sp', i), f, lw=7, col=WHITE, amp=0.5, a=1 - q)
    c.restore()
    caption(c, t, -1, [[("THIS WALL IS COVERED", CREAM)], [("IN CHEWED GUM.", GOLD)]], y=300, size=88, pop=False)
    strip(c, 1560, ["Post Alley, Seattle"], seg(t, 0.9, 1.3), size=40)


def scene2(c, t, f, g):
    brickwall(c, f, g, gumk=0.05 + 0.5 * ease(seg(t, 1.2, 3.8)))
    alley_floor(c)
    rrect(c, 720, 720, 280, 220, 18); fs(c, hx('3A2E5A'), 9)
    rrect(c, 744, 744, 232, 70, 12); fs(c, GOLD, 6); fit(c, "BOX OFFICE", 860, 792, 40, 210, INK)
    rrect(c, 760, 830, 200, 90, 10); fs(c, GLASS, 6)
    for i, (x, sh) in enumerate(((140, PURPLE), (320, ORANGE), (500, BLUE))):
        k = eback(seg(t, 0.15 + i * 0.2, 0.45 + i * 0.2))
        if k <= 0.01: continue
        up = math.sin(seg(t, 1.3 + i * 0.6, 1.9 + i * 0.6) * math.pi)
        stick(c, x, 1480 - 190, 1.0, ('q', i), f, lh=(-50, -20), rh=(80 + 40 * up, -150 - 120 * up), face='smile' if up < 0.3 else 'grin', shirt=sh, look=(1, -0.2),
              bob=2 * math.sin(g * 5 + i))
    caption(c, t, 0.15, [[("IT STARTED IN THE 1990s", CREAM)], [("IN A THEATER LINE.", GOLD)]], y=300, size=76)
    strip(c, 1560, ["Source: Pike Place Market."], seg(t, 1.0, 1.4), size=36)


def scene3(c, t, f, g):
    scr = ease(seg(t, 0.4, 1.6)); back = ease(seg(t, 1.9, 3.3))
    cx = lerp(1040, 40, scr)
    gk = 0.55 if t < 1.9 else 0.55 * back
    brickwall(c, f, g, gumk=gk if t >= 1.9 else 0.55, clean_rect=(cx, 380, 1040, 1480) if t < 1.9 else None)
    alley_floor(c)
    if t < 1.9:
        wx = cx
        stick(c, wx + 120, 1480 - 190, 1.0, 'wk', f, lh=(-70, -60), rh=(-150, -200 + 30 * math.sin(g * 16)), face='flat', shirt=ORANGE, hat='cap', look=(-1, -0.3))
        wline(c, [(wx + 120 - 150, 1480 - 190 - 200 + 30 * math.sin(g * 16) - 20), (wx - 60, 1480 - 190 - 280 + 30 * math.sin(g * 16))], 'scr', f, lw=12, col=STEELD)
        for i in range(4):
            ph = (g * 2 + i / 4) % 1
            c.new_path(); c.arc(wx + 40 - 30 * i, 1300 + 180 * ph, 10, 0, 2 * math.pi); rgb(c, GUMC[i], 1 - ph); c.fill()
    else:
        for i in range(5):
            pk = eback(seg(t, 1.95 + i * 0.22, 2.25 + i * 0.22))
            if pk > 0.01:
                sign(c, 180 + i * 180, 1200 - 120 * (i % 2), "POP!", GOLD, INK, size=34, k=pk, rot=0.1 * (-1) ** i, padx=16, lw=6)
    caption(c, t, 0.15, [[("THE LANDLORD", CREAM)], [("WANTED IT GONE.", GOLD)]], y=300, size=82, t1=1.85)
    caption(c, t, 1.95, [[("IT CAME RIGHT BACK.", GOLD)]], y=300, size=82)
    strip(c, 1560, ["Sources: Unexpected Productions, The Columbian."], seg(t, 0.8, 1.2), size=36)


def scene4(c, t, f, g):
    c.rectangle(0, 0, W, H); rgb(c, hx('2B2F4A')); c.fill()
    grow = ease(seg(t, 0.2, 1.6))
    wx1 = lerp(420, 960, grow); wy0 = lerp(1100, 560, grow)
    brickwall(c, f, g, x0=200, x1=wx1, y0=wy0, y1=1400, gumk=1.0)
    c.rectangle(0, 1400, W, 520); rgb(c, hx('6C6A78')); c.fill()
    stick(c, 140, 1400 - 190 * 0.9, 0.9, 'sc', f, lh=(-40, -20), rh=(40, -20), face='o', shirt=TEAL, look=(1, -0.6))
    kk = eback(seg(t, 1.4, 1.75))
    if kk > 0.01:
        wline(c, [(wx1 + 40, wy0), (wx1 + 40, 1400)], 'hv', f, lw=8, col=GOLD, a=kk)
        wline(c, [(200, 1450), (wx1, 1450)], 'wv', f, lw=8, col=GOLD, a=kk)
    sign(c, wx1 - 10, (wy0 + 1400) / 2, "8+ FT HIGH", GOLD, INK, size=40, rot=-1.5708, k=kk, padx=18, lw=6)
    sign(c, (200 + wx1) / 2, 1520, "54 FT WIDE", GOLD, INK, size=44, k=eback(seg(t, 1.7, 2.05)), padx=20, lw=6)
    caption(c, t, 0.15, [[("NOW IT RUNS", CREAM)], [("DOWN THE ALLEY.", GOLD)]], y=300, size=86)
    strip(c, 1640, ["Pike Place Market spokesperson, 2024, via KOMO News."], seg(t, 1.0, 1.4), size=32)


def bucket(c, x, y, s, fill=0.0, label=None):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.new_path(); c.move_to(-70, -150); c.line_to(70, -150); c.line_to(56, 0); c.line_to(-56, 0); c.close_path(); fs(c, hx('E8ECF4'), 8)
    if fill > 0:
        for i in range(7):
            c.new_path(); c.arc(-46 + i * 15, -150 + 20 - 16 * math.sin(i * 1.7) + (1 - fill) * 150, 15, 0, 2 * math.pi); rgb(c, GUMC[i % 6]); c.fill()
    c.new_path(); c.arc(0, -150, 76, math.pi * 1.05, math.pi * 1.95); rgb(c, INK); c.set_line_width(6); c.stroke()
    c.restore()


def scene5(c, t, f, g):
    st = ease(seg(t, 0.3, 1.6))
    brickwall(c, f, g, y1=1480, clean_rect=(1040 - 1000 * st, 380, 1040, 1480))
    alley_floor(c)
    wx = 1040 - 1000 * st
    if st < 1:
        for i in range(6):
            ph = (g * 1.8 + i / 6) % 1
            wcirc(c, wx + 60 + 50 * ph, 900 + 80 * i - 60 * ph, 30 + 50 * ph, ('st', i), f, amp=2); rgb(c, WHITE, 0.6 * (1 - ph)); c.fill()
        stick(c, min(wx + 220, 980), 1480 - 190, 1.0, 'cl', f, lh=(-140, -170), rh=(-120, -140), face='flat', shirt=hx('E8ECF4'), hat='cap', look=(-1, -0.2))
    fall = seg(t, 1.0, 1.6)
    hx_ = lerp(540, 300, fall); hy_ = lerp(820, 1330, ein(fall))
    if fall < 1:
        gum(c, hx_, hy_, 0.9, 'hero', f, face='o', eyes='big', rot=fall * 2.5, look=(0, 1))
    for i in range(5):
        bucket(c, 160 + i * 150, 1500, 0.8, fill=min(1, max(0, (t - 1.2 - i * 0.25) * 1.5)))
    if fall >= 1:
        gum(c, 300, 1360 - 4 * math.sin(g * 4), 0.55, 'hero', f, face='o' if t < 3.2 else 'flat', eyes='dot', look=(0.6, -0.6))
    v = 2350 * eout(seg(t, 1.6, 3.4))
    panel(c, 540, 600, 760, 170, "{:,} LB".format(int(round(v))), 100, eback(seg(t, 1.5, 1.85)))
    caption(c, t, 0.15, [[("2015: CREWS STEAMED", CREAM)], [("IT ALL OFF.", GOLD)]], y=300, size=80)
    strip(c, 1640, ["3 days, about 94 buckets. Steam chosen to protect the brick.", "Sources: Pike Place Market via KOMO, NBC News."], seg(t, 2.0, 2.4), size=30)


def scene6(c, t, f, g):
    regrow = ease(seg(t, 0.5, 2.9))
    brickwall(c, f, g, gumk=0.02 + 0.98 * regrow)
    alley_floor(c)
    for i, (x, sh) in enumerate(((200, PURPLE), (430, ORANGE), (680, GREEN), (900, BLUE))):
        up = math.sin(((t * 1.6 + i * 0.37) % 1) * math.pi)
        stick(c, x, 1480 - 190, 1.0, ('v', i), f, lh=(-50, -20), rh=(70 + 60 * up, -150 - 110 * up), face='grin', shirt=sh, look=(0, -0.4), bob=2 * math.sin(g * 6 + i))
    caption(c, t, 0.15, [[("THEN VISITORS", CREAM)], [("FILLED IT AGAIN.", GOLD)]], y=300, size=84)
    strip(c, 1640, ["Cleaned again in 2019 and 2024. Source: Pike Place Market via KOMO."], seg(t, 0.9, 1.3), size=30)


def scene7(c, t, f, g):
    bg(c, hx('FF7A5A'), hx('FFC83D'))
    hop = abs(math.sin(g * 5)) * 30
    bucket(c, 540, 1440, 1.8, fill=1.0)
    gum(c, 540, 1110 - hop, 1.3, 'hero', f, face='grin', look=(0, -0.3), rot=0.05 * math.sin(g * 5))
    qmarks(c, ((200, 760, -0.3), (880, 800, 0.3), (230, 1300, 0.2)), t, 0.6)
    caption(c, t, 0.1, [[("WOULD YOU", CREAM)], [("ADD YOURS?", GOLD)]], y=300, size=96)


SCENES = [(0.0, 3.0, scene1), (3.0, 6.8, scene2), (6.8, 10.4, scene3), (10.4, 13.6, scene4), (13.6, 17.8, scene5), (17.8, 21.4, scene6), (21.4, 24.0, scene7)]
draw = make_draw(SCENES)
