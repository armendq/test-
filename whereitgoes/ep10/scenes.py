from kit import *

DURATION = 24.0
RND = cairo.LINE_CAP_ROUND
SAND = hx('E8C98A'); SANDD = hx('C9A466'); CORK = hx('C08A55'); DUSK1 = hx('2E3466'); DUSK2 = hx('F2956A')
SEA1 = hx('2F8FC4'); SEA2 = hx('15507E')


def bottle(c, x, y, s, key, f, face='smile', eyes='dot', rot=0.0, look=(0, 0), paper=True):
    """hero bottle, x, y = centre of the body, about 130 x 400"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rrect(c, -26, -196, 52, 40, 8); fs(c, CORK, 7)
    rrect(c, -30, -162, 60, 80, 14); rgb(c, GLASS, 0.9); c.fill_preserve(); rgb(c, INK); c.set_line_width(9); c.stroke()
    rrect(c, -66, -100, 132, 230, 46); rgb(c, GLASS, 0.9); c.fill_preserve(); rgb(c, INK); c.set_line_width(9); c.stroke()
    if paper:
        rrect(c, -20, -132, 40, 92, 8); fs(c, PAPER, 5)
        c.rectangle(-22, -92, 44, 10); rgb(c, CORAL); c.fill()
    c.new_path(); c.move_to(-44, -70); c.line_to(-44, 70); rgb(c, WHITE, 0.6); c.set_line_width(10); c.set_line_cap(RND); c.stroke()
    facef(c, 4, 40, 56, face, look, eyes)
    c.restore()


def mini(c, x, y, s, rot=0.0, weight=False):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if weight:
        c.new_path(); c.move_to(0, 60); c.line_to(0, 120); rgb(c, INK); c.set_line_width(5); c.stroke()
        c.new_path(); c.arc(0, 132, 16, 0, 2 * math.pi); fs(c, IRON, 5)
    rrect(c, -10, -78, 20, 18, 4); fs(c, CORK, 4)
    rrect(c, -12, -62, 24, 30, 6); rgb(c, GLASS, 0.9); c.fill_preserve(); rgb(c, INK); c.set_line_width(5); c.stroke()
    rrect(c, -26, -36, 52, 96, 18); rgb(c, GLASS, 0.9); c.fill_preserve(); rgb(c, INK); c.set_line_width(5); c.stroke()
    rrect(c, -8, -50, 16, 40, 3); rgb(c, PAPER); c.fill()
    c.restore()


def sky(c, top=DUSK1, bot=DUSK2, y1=1250):
    gl = cairo.LinearGradient(0, -400, 0, y1)
    gl.add_color_stop_rgb(0, *top); gl.add_color_stop_rgb(1, *bot)
    c.set_source(gl); c.rectangle(-600, -600, W + 1200, y1 + 600); c.fill()


def sea(c, y0, g, top=SEA1, bot=SEA2, amp=14, crest=True):
    gl = cairo.LinearGradient(0, y0, 0, H + 300)
    gl.add_color_stop_rgb(0, *top); gl.add_color_stop_rgb(1, *bot)
    c.new_path(); c.move_to(-600, H + 600)
    for i in range(0, 50):
        xx = -600 + i * 50; c.line_to(xx, y0 + amp * math.sin(xx * 0.012 + g * 2.2))
    c.line_to(W + 600, H + 600); c.close_path(); c.set_source(gl); c.fill_preserve(); rgb(c, INK); c.set_line_width(8); c.stroke()
    if crest:
        for r in range(3):
            yy = y0 + 110 + r * 150
            for k in range(6):
                xx = ((k * 230 + r * 110 + g * (40 + 20 * r)) % (W + 300)) - 150
                c.new_path(); c.move_to(xx, yy); c.curve_to(xx + 30, yy - 18, xx + 60, yy - 18, xx + 90, yy); rgb(c, WHITE, 0.35); c.set_line_width(6); c.set_line_cap(RND); c.stroke()


def splash(c, x, y, q, f, key='spl', n=7, r=110):
    if not (0 <= q < 1): return
    for i in range(n):
        a = math.pi + (i + 0.5) * math.pi / n
        wline(c, [(x + 40 * math.cos(a), y + 20 * math.sin(a)), (x + (60 + r * q) * math.cos(a), y + (30 + r * 1.1 * q) * math.sin(a))], (key, i), f, lw=8, col=WHITE, amp=0.5, a=1 - q)
    c.save(); c.translate(x, y); c.scale(1, 0.28); c.new_path(); c.arc(0, 0, 60 + 160 * q, 0, 2 * math.pi); c.restore(); rgb(c, WHITE, 0.7 * (1 - q)); c.set_line_width(6); c.stroke()


def scene1(c, t, f, g):
    drop = 1.9
    k = ease(seg(t, 0.55, 1.35)); z = lerp(1.85, 1.0, k)
    c.save(); cam(c, z, lerp(560, 540, k), lerp(900, 960, k))
    sky(c)
    c.new_path(); c.arc(820, 1120, 120, math.pi, 2 * math.pi); rgb(c, hx('FFD98A')); c.fill()
    sea(c, 1250, g)
    fall = ein(seg(t, 1.2, drop))
    bx, by = 540, lerp(840, 1240, fall)
    if t < drop:
        sweat(c, bx, by - 40, 1.0, g, f)
        bottle(c, bx + 3 * math.sin(g * 41), by, 0.95, 'hero', f, face='o', eyes='big', rot=0.25 * math.sin(g * 6) + 0.6 * fall, look=(0, 1))
    else:
        bob = 10 * math.sin(g * 3)
        bottle(c, bx, 1250 + bob, 0.95, 'hero', f, face='o' if t < 2.4 else 'flat', eyes='big', rot=0.12 * math.sin(g * 2.5), look=(0.6, -0.6))
        c.save(); c.rectangle(-600, 1290 + bob, W + 1200, 800); c.clip(); sea(c, 1250, g, crest=False); c.restore()
        splash(c, bx, 1260, (t - drop) / 0.6, f)
    c.restore()
    caption(c, t, -1, [[("THIS BOTTLE WAS AT SEA", CREAM)], [("FOR 108 YEARS.", GOLD)]], y=300, size=86, pop=False)
    strip(c, 1640, ["North Sea, 1906"], seg(t, 0.9, 1.3), size=40)


def boat(c, x, y, s, g):
    c.save(); c.translate(x, y + 6 * math.sin(g * 2.4)); c.rotate(0.02 * math.sin(g * 2.4)); c.scale(s, s)
    rrect(c, -150, -230, 170, 130, 14); fs(c, CREAM, 8)
    for i in range(2):
        rrect(c, -128 + i * 74, -206, 52, 44, 8); fs(c, GLASS, 5)
    c.rectangle(-60, -330, 34, 100); fs(c, CORAL, 7)
    c.new_path(); c.move_to(-330, -110); c.line_to(330, -110); c.line_to(250, 20); c.line_to(-280, 20); c.close_path(); fs(c, hx('2F6D8F'), 9)
    c.rectangle(-300, -100, 590, 26); rgb(c, WHITE, 0.85); c.fill()
    c.restore()


def scene2(c, t, f, g):
    sky(c, hx('8FD3F4'), hx('E9F8FF'))
    cloud(c, 220, 560, 1.1); cloud(c, 820, 700, 0.9)
    boat(c, 420, 1260, 1.0, g)
    n = int(1020 * eout(seg(t, 0.6, 3.2)))
    for i in range(6):
        ph = (t * 1.4 + i / 6) % 1
        if t < 0.5: break
        x = 720 + 40 * ph; y = lerp(1120, 1290, ein(ph))
        if ph < 0.85: mini(c, x, y, 0.8, ph * 3)
        else: splash(c, x, 1280, (ph - 0.85) / 0.15, f, ('s2', i), n=5, r=50)
    sea(c, 1270, g)
    for i in range(min(9, n // 110)):
        mini(c, 640 + (i * 97) % 380, 1360 + (i % 3) * 70 + 6 * math.sin(g * 3 + i), 0.55, 0.3 * math.sin(g * 2 + i))
    panel(c, 540, 720, 640, 150, "{:,} BOTTLES".format(n), 86, eback(seg(t, 0.4, 0.75)))
    caption(c, t, 0.15, [[("SCIENTISTS DROPPED", CREAM)], [("1,020 ON PURPOSE.", GOLD)]], y=300, size=82)
    strip(c, 1720, ["1904 to 1906. Marine Biological Association, UK.", "Sources: National Geographic, Smithsonian Magazine."], seg(t, 1.0, 1.4), size=30)


def scene3(c, t, f, g):
    gl = cairo.LinearGradient(0, 420, 0, 1400)
    gl.add_color_stop_rgb(0, *SEA1); gl.add_color_stop_rgb(1, *hx('0E3A5E'))
    c.set_source(gl); c.rectangle(0, 0, W, H); c.fill()
    for i in range(7):
        c.new_path(); c.move_to(i * 180 - 40, 420); c.line_to(i * 180 + 60, 1400); rgb(c, WHITE, 0.05); c.set_line_width(40); c.stroke()
    c.rectangle(0, 1420, W, 500); rgb(c, SAND); c.fill()
    c.new_path(); c.move_to(0, 1420)
    for i in range(23): c.line_to(i * 50, 1420 + 10 * math.sin(i * 1.3))
    c.line_to(W, 1420); rgb(c, INK); c.set_line_width(8); c.stroke()
    for i in range(5):
        x = ((i * 260 - g * 90) % (W + 200)) - 100
        wline(c, [(x + 120, 1200 + 40 * (i % 2)), (x, 1200 + 40 * (i % 2))], ('cur', i), f, lw=8, col=WHITE, amp=0.6, a=0.45)
        c.new_path(); c.move_to(x - 4, 1200 + 40 * (i % 2)); c.line_to(x + 22, 1186 + 40 * (i % 2)); c.line_to(x + 22, 1214 + 40 * (i % 2)); c.close_path(); rgb(c, WHITE, 0.45); c.fill()
    for i in range(5):
        x = ((i * 250 + 120 - g * 70) % (W + 200)) - 100
        mini(c, x, 1160 + 14 * math.sin(g * 2 + i), 0.9, 0.15 * math.sin(g * 2 + i), weight=True)
    hb = 8 * math.sin(g * 2.6)
    c.new_path(); c.move_to(540, 1000 + hb + 130 * 0.85); c.line_to(540, 1290); rgb(c, INK); c.set_line_width(7); c.stroke()
    c.new_path(); c.arc(540, 1310, 28, 0, 2 * math.pi); fs(c, IRON, 7)
    bottle(c, 540, 1000 + hb, 0.85, 'hero', f, face='o' if t < 1.6 else 'smile', eyes='big', rot=0.08 * math.sin(g * 2.6), look=(-1, 0.4))
    for i in range(4):
        ph = (g * 0.7 + i / 4) % 1
        c.new_path(); c.arc(600 + 30 * math.sin(ph * 9 + i), 880 - 300 * ph, 8 + 6 * ph, 0, 2 * math.pi); rgb(c, WHITE, 0.6 * (1 - ph)); c.set_line_width(4); c.stroke()
    caption(c, t, 0.15, [[("WEIGHTED TO DRIFT", CREAM)], [("NEAR THE SEABED.", GOLD)]], y=300, size=84)
    strip(c, 1640, ["They tracked deep currents. Source: Smithsonian Magazine."], seg(t, 0.8, 1.2), size=32)


def postcard(c, x, y, k, rot=0.0):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(k, k)
    rrect(c, -230, -150, 460, 300, 14); rgb(c, INK, 0.3); c.translate(10, 12); c.fill(); c.translate(-10, -12)
    rrect(c, -230, -150, 460, 300, 14); fs(c, PAPER, 8)
    fit(c, "FOUND ME?", 0, -64, 56, 400, INK)
    fit(c, "WRITE WHERE.", 0, 4, 46, 400, CORAL)
    fit(c, "MAIL ME BACK.", 0, 64, 46, 400, CORAL)
    c.new_path(); c.move_to(-200, 106); c.line_to(200, 106); rgb(c, INK, 0.3); c.set_line_width(4); c.stroke()
    c.restore()


def coin(c, x, y, k, label="1 SHILLING", size=34):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k)
    c.new_path(); c.arc(0, 0, 110, 0, 2 * math.pi); fs(c, hx('D9DCE6'), 9)
    c.new_path(); c.arc(0, 0, 88, 0, 2 * math.pi); rgb(c, INK, 0.3); c.set_line_width(4); c.stroke()
    fit(c, label, 0, size * 0.36, size, 160, INK)
    c.restore()


def scene4(c, t, f, g):
    sky(c, hx('8FD3F4'), hx('E9F8FF'), 900)
    sea(c, 900, g)
    up = eout(seg(t, 0.1, 1.2))
    ny = lerp(1500, 1050, up)
    c.save(); c.translate(540, ny)
    c.new_path(); c.move_to(-260, -260); c.curve_to(-280, 40, -120, 220, 0, 220); c.curve_to(120, 220, 280, 40, 260, -260); rgb(c, hx('E8D9B0'), 0.25); c.fill()
    for i in range(11):
        xx = -250 + i * 50
        c.new_path(); c.move_to(xx, -260); c.curve_to(xx * 1.05, 0, xx * 0.6, 150, xx * 0.2, 210); rgb(c, hx('E8D9B0')); c.set_line_width(5); c.stroke()
    for j in range(6):
        yy = -220 + j * 70; ww = 260 - (j * j) * 6
        c.new_path(); c.move_to(-ww, yy); c.curve_to(-ww / 2, yy + 20, ww / 2, yy + 20, ww, yy); rgb(c, hx('E8D9B0')); c.set_line_width(5); c.stroke()
    for i, (bx, by, r) in enumerate(((-120, 40, 0.4), (40, 90, -0.5), (150, 10, 0.9), (-30, -60, -1.2))):
        mini(c, bx, by, 0.9, r + 0.1 * math.sin(g * 3 + i))
    c.restore()
    c.new_path(); c.move_to(280, -100); c.line_to(540 - 260, ny - 260); c.move_to(800, -100); c.line_to(540 + 260, ny - 260); rgb(c, INK); c.set_line_width(7); c.stroke()
    postcard(c, 400, 780, eback(seg(t, 1.3, 1.65)), -0.06)
    coin(c, 820, 940, eback(seg(t, 1.9, 2.25)))
    caption(c, t, 0.15, [[("FINDERS MAILED THE CARD", CREAM)], [("FOR ONE SHILLING.", GOLD)]], y=300, size=78)
    strip(c, 1720, ["The card asked where it was found. Source: Guinness World Records."], seg(t, 1.0, 1.4), size=30)


def scene5(c, t, f, g):
    cyc = (t * 0.9) % 1
    day = 0.5 + 0.5 * math.cos(cyc * 2 * math.pi)
    top = tuple(lerp(a, b, day) for a, b in zip(DUSK1, hx('8FD3F4'))); bot = tuple(lerp(a, b, day) for a, b in zip(hx('5A4E8A'), hx('E9F8FF')))
    sky(c, top, bot)
    a = cyc * 2 * math.pi
    c.new_path(); c.arc(540 + 420 * math.sin(a), 1150 - 520 * math.cos(a), 70, 0, 2 * math.pi); rgb(c, hx('FFD98A') if day > 0.4 else hx('F4F1E4')); c.fill()
    sea(c, 1250, g)
    bob = 14 * math.sin(g * 2.6)
    bottle(c, 540, 1230 + bob, 0.8, 'hero', f, face='flat' if t < 2.5 else 'o', eyes='dot', rot=0.15 * math.sin(g * 2.6), look=(-1, -0.2))
    c.save(); c.rectangle(-600, 1290 + bob, W + 1200, 800); c.clip(); sea(c, 1250, g, crest=False); c.restore()
    yr = int(round(lerp(1906, 2015, eout(seg(t, 1.0, 3.6)))))
    panel(c, 540, 700, 480, 170, str(yr), 110, eback(seg(t, 0.8, 1.15)))
    caption(c, t, 0.15, [[("ABOUT HALF CAME BACK.", CREAM)], [("ONE KEPT DRIFTING.", GOLD)]], y=300, size=80)
    strip(c, 1640, ["About 55% were returned. Source: MBA via Smithsonian Magazine."], seg(t, 1.0, 1.4), size=30)


def mailbox(c, x, y, s):
    c.save(); c.translate(x, y); c.scale(s, s)
    c.rectangle(-14, -40, 28, 120); fs(c, IRON, 6)
    rrect(c, -80, -210, 160, 180, 60); fs(c, RED, 8)
    rrect(c, -50, -150, 100, 20, 8); rgb(c, INK); c.fill()
    c.restore()


def scene6(c, t, f, g):
    sky(c, hx('8FD3F4'), hx('E9F8FF'), 1100)
    cloud(c, 260, 560, 1.0); cloud(c, 860, 640, 0.8)
    sea(c, 1100, g, crest=False)
    c.new_path(); c.move_to(-50, 1360); c.curve_to(300, 1250, 700, 1300, W + 50, 1220); c.line_to(W + 50, H + 50); c.line_to(-50, H + 50); c.close_path(); fs(c, SAND, 8)
    wash = eout(seg(t, 0.1, 1.0))
    bx, by = lerp(380, 520, wash), lerp(1240, 1330, wash)
    c.save(); c.translate(bx, by); c.rotate(-1.3 + 0.05 * math.sin(g * 3)); c.translate(-bx, -by)
    bottle(c, bx, by, 0.6, 'hero', f, face='o' if t < 1.2 else 'grin', eyes='big', look=(0, -1))
    c.restore()
    c.rectangle(782, 1060, 16, 220); fs(c, CARDD, 5)
    sign(c, 790, 1040, "AMRUM, GERMANY", GOLD, INK, size=40, rot=-0.04, k=eback(seg(t, 0.3, 0.6)), padx=18, lw=6)
    mailbox(c, 160, 1500, 0.9)
    fly = seg(t, 1.3, 2.1)
    if 0 < fly < 1:
        postcard(c, lerp(520, 160, ease(fly)), lerp(1250, 1360, ease(fly)) - 220 * math.sin(fly * math.pi), 0.28 * (1 - 0.6 * fly), fly * 4)
    coin(c, 760, 760, eback(seg(t, 2.2, 2.55)), "PAID!", 44)
    caption(c, t, 0.15, [[("IT WASHED UP IN 2015.", CREAM)], [("THE SHILLING WAS PAID.", GOLD)]], y=300, size=78)
    strip(c, 1720, ["108 years, 138 days. A Guinness World Record.", "The old shilling was bought online. Source: Guinness World Records."], seg(t, 0.9, 1.3), size=29)


def scene7(c, t, f, g):
    bg(c, hx('FF7A5A'), hx('FFC83D'))
    hop = abs(math.sin(g * 5)) * 30
    bottle(c, 540, 1180 - hop, 1.25, 'hero', f, face='grin', look=(0, -0.3), rot=0.06 * math.sin(g * 5))
    qmarks(c, ((200, 760, -0.3), (880, 800, 0.3), (230, 1340, 0.2)), t, 0.6)
    caption(c, t, 0.1, [[("WHAT WOULD YOU", CREAM)], [("WRITE IN YOURS?", GOLD)]], y=300, size=92)


SCENES = [(0.0, 3.0, scene1), (3.0, 6.8, scene2), (6.8, 10.4, scene3), (10.4, 13.6, scene4), (13.6, 17.8, scene5), (17.8, 21.4, scene6), (21.4, 24.0, scene7)]
draw = make_draw(SCENES)
