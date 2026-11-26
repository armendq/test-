from base2 import *

PAPER = hx('FFF7E6'); BOX = hx('3F7FE8'); BOXD = hx('2C5FC0'); OFFICE = hx('E9F1F7')


def env(c, x, y, s, key, f, face='smile', eyes='dot', rot=0.0, look=(0, 0), postmark=False, barcode=0.0, sq=1.0, plain=False):
    """x, y = centre of the envelope"""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    rrect(c, -150, -100, 300, 200, 18); fs(c, PAPER, 10)
    wline(c, [(-146, -96), (0, 6), (146, -96)], (key, 'fl'), f, lw=6, col=INK, amp=0.8, a=0.22)
    rrect(c, 82, -86, 52, 60, 6); fs(c, CORAL, 5)
    c.new_path(); c.arc(108, -56, 13, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
    if postmark:
        for k in range(3):
            pts = [(-10 + i * 14, -78 + k * 16 + 5 * math.sin(i * 1.6)) for i in range(7)]
            wline(c, pts, (key, 'pm', k), f, lw=5, col=INK, amp=0.3, a=0.75)
        c.new_path(); c.arc(-36, -62, 26, 0, 2 * math.pi); rgb(c, INK, 0.75); c.set_line_width(5); c.stroke()
    if not plain:
        facef(c, -6, 14, 74, face, look, eyes)
        for k in range(2):
            pts = [(-128 + i * 12, 58 + k * 18 + 5 * math.sin(i * 2.3 + k)) for i in range(7)]
            wline(c, pts, (key, 'ad', k), f, lw=5, col=hx('4C8DF6'), amp=1.2, a=0.9)
    else:
        for k in range(3):
            c.rectangle(-70, -10 + k * 26, 150 - k * 30, 9); rgb(c, INK, 0.5); c.fill()
    if barcode > 0:
        c.save(); c.rectangle(-140, 70, 280 * barcode, 26); c.clip()
        xx = -24
        for (bw, gp) in BARS:
            if xx > 132: break
            c.rectangle(xx, 72, max(3, bw * 0.45), 20); rgb(c, INK); c.fill(); xx += bw * 0.45 + gp * 0.5
        c.restore()
    c.restore()


def street(c, f, g):
    bg(c, hx('9FDCF5'), hx('FFE9C9'))
    wcirc(c, 880, 420, 70, 'sun', f, amp=3); rgb(c, hx('FFE28A')); c.fill()
    for i, (x, w, h, col) in enumerate(((40, 300, 420, hx('F3D7B0')), (330, 260, 520, hx('F7C9A8')), (590, 330, 400, hx('E9D9B8')), (900, 240, 480, hx('F3D7B0')))):
        wrect(c, x, 1380 - h, w, h, ('hs', i), f); fs(c, col, 8)
        wpoly(c, [(x - 16, 1380 - h), (x + w / 2, 1380 - h - 120), (x + w + 16, 1380 - h)], ('rf', i), f); fs(c, hx('D9705A'), 8)
        for k in range(2):
            rrect(c, x + 40 + k * (w - 150), 1380 - h + 70, 70, 90, 10); fs(c, hx('BFE4F5'), 6)
    c.rectangle(0, 1380, W, H - 1380); c.set_source(grad(0, 1380, 0, H, [(0, hx('D9D2C3')), (1, hx('BFB6A3'))])); c.fill()
    wline(c, [(0, 1380), (W, 1380)], 'kerb', f, lw=7, amp=0.8)


def mailbox(c, f, x, y, key='mb'):
    wline(c, [(x - 60, y), (x - 60, y - 60)], (key, 'l1'), f, lw=20, col=BOXD, amp=0.6); wline(c, [(x + 60, y), (x + 60, y - 60)], (key, 'l2'), f, lw=20, col=BOXD, amp=0.6)
    c.new_path(); c.move_to(x - 120, y - 50); c.line_to(x - 120, y - 330); c.arc(x, y - 330, 120, math.pi, 2 * math.pi); c.line_to(x + 120, y - 50); c.close_path()
    fs(c, BOX, 10)
    rrect(c, x - 84, y - 356, 168, 34, 12); fs(c, hx('10172B'), 6)
    rrect(c, x - 70, y - 270, 140, 74, 12); fs(c, WHITE, 6); txt(c, "MAIL", x, y - 214, 50, BOXD)


# ------------------------------------------------------------------ scene 1: the drop
HIP = (300, 1190); SLOT = (700, 1040)


def scene1(c, t, f, g):
    drop = ease(seg(t, 1.35, 2.25))
    hand0 = (HIP[0] + 150, HIP[1] - 230)
    px = lerp(hand0[0] + 40, SLOT[0], drop); py = lerp(hand0[1] - 30, SLOT[1], drop) - 170 * math.sin(drop * math.pi)
    k = ease(seg(t, 0.6, 1.3)); z = lerp(2.05, 1.0, k)
    fx, fy = lerp((px + SLOT[0]) / 2 + 10, 540, k), lerp((py + SLOT[1]) / 2 - 30, 960, k)
    fear = 1 - seg(t, 1.2, 1.35)
    jx = 5 * math.sin(g * 41) * fear; jy = 4 * math.sin(g * 53 + 1) * fear
    es = lerp(0.84, 0.62, k)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)
    street(c, f, g)
    mailbox(c, f, 700, 1380)
    if t < 1.35:                                   # the slot gapes like a mouth
        gp = 12 + 14 * abs(math.sin(g * 5))
        rrect(c, 610, 1024 - gp / 2, 180, 34 + gp, 16); fs(c, hx('10172B'), 6)
    stick(c, HIP[0], HIP[1], 1.0, 'you', f, lh=(-60, -20), rh=(150, -230) if t < 2.3 else (110 + 12 * math.sin(g * 9), -300), face='smile', eyes='closed',
          shirt=TEAL, bob=math.sin(g * 3) * 2)
    if drop < 1:
        if t < 1.3:                                # sweat flies off the letter
            for i in range(4):
                ph = (g * 2.4 + i / 4) % 1
                ang = -2.75 + i * 0.5
                rr = (150 + 95 * ph) * es
                wcirc(c, px + jx + math.cos(ang) * rr, py + jy + math.sin(ang) * rr * 0.8, (13 - 9 * ph) * es / 0.62, ('sw', i), f, amp=1)
                fs(c, hx('8FD9FA'), 4)
        env(c, px + jx, py + jy, es * (1 - 0.35 * ein(seg(drop, 0.8, 1.0))), 'hero', f, face='o', eyes='big',
            rot=0.12 * math.sin(g * 30) * fear + 0.1 * math.sin(g * 7) * (1 - fear) + drop * 0.5, look=(1, 0.6))
    rrect(c, 616, 1024, 168, 34, 12); rgb(c, hx('10172B'), 1.0 if drop > 0.85 else 0.0); c.fill()
    c.restore()
    caption(c, t, -1, [[("WHERE DOES", CREAM)], [("YOUR LETTER GO?", GOLD)]], y=300, size=92, pop=False)
    w = ein(seg(t, 2.8, 3.2))
    if w > 0:
        c.new_path(); c.arc(700, 1010, 2300 * w, 0, 2 * math.pi); rgb(c, NIGHT); c.fill()


# ------------------------------------------------------------------ scene 2: flipped and postmarked
def stream(c, f, g, y, sp, s=0.36, n=5, key='st', skip=None):
    for k in range(n):
        xx = ((k * 330 + g * sp) % 1700) - 300
        if skip and skip[0] < xx < skip[1]: continue
        env(c, xx, y - 100 * s, s, (key, k), f, plain=True)


def scene2(c, t, f, g):
    boh(c, f, g)
    c.save(); c.translate(540, 1350); c.scale(1.2, 1.2); c.translate(-540, -1300)
    belt(c, -80, W + 80, 1300, g, f, sp=700)
    stream(c, f, g, 1300, 900, skip=(300, 780))
    if t < 2.9: bx = lerp(-200, 540, eout(seg(t, 0.0, 0.9)))
    else: bx = lerp(540, 1320, ein(seg(t, 2.9, 4.3)))
    flip = ease(seg(t, 1.0, 1.6))
    slam = seg(t, 1.95, 2.25)
    stamped = t > 2.05
    rot = math.pi * (1 - flip) + 0.5 * math.sin(flip * math.pi)
    lift = 150 * math.sin(flip * math.pi)
    sq = 1 - 0.2 * math.sin(clamp(seg(t, 2.02, 2.3)) * math.pi)
    env(c, bx, 1300 - 100 * 0.85 - lift, 0.85, 'hero', f, face='o' if t < 1.0 else ('flat' if stamped and t < 2.9 else 'smile'),
        eyes='big' if t < 1.6 else ('closed' if stamped and t < 2.9 else 'dot'), rot=rot, postmark=stamped, sq=sq, look=(1, 0))
    # the machine: two posts, a head with the stamper
    for px in (360, 720):
        wline(c, [(px, 760), (px, 1300)], ('cp', px), f, lw=24, col=STEELD, amp=0.8)
    rrect(c, 320, 690, 440, 120, 24); fs(c, STEEL, 10)
    rrect(c, 350, 716, 380, 66, 16); fs(c, STEELD, 7); txt(c, "POSTMARK", 540, 768, 46, CREAM)
    sy = 810 + 240 * math.sin(slam * math.pi) if 0 < slam < 1 else 810
    wline(c, [(540, 800), (540, sy + 20)], 'arm', f, lw=30, col=STEELD, amp=0.5)
    rrect(c, 470, sy + 10, 140, 60, 14); fs(c, GOLD, 9)
    if 2.02 < t < 2.4:
        q = seg(t, 2.02, 2.4)
        for k in range(7):
            a = math.pi * (1.05 + 0.9 * k / 6)
            wline(c, [(bx + math.cos(a) * (120 + 60 * q), 1150 + math.sin(a) * (90 + 50 * q)), (bx + math.cos(a) * (160 + 90 * q), 1150 + math.sin(a) * (120 + 80 * q))],
                  ('bang', k), f, lw=8, col=WHITE, amp=0.6, a=1 - q)
    c.restore()
    caption(c, t, 0.25, [[("A MACHINE FLIPS IT", CREAM)], [("AND POSTMARKS IT.", GOLD)]], y=300, size=84, t1=2.6)
    caption(c, t, 2.65, [[("36,000", GOLD)], [("LETTERS AN HOUR.", CREAM)]], y=300, size=96)


# ------------------------------------------------------------------ scene 3: the camera reads
def monitor(c, f, x, y, w, h, key='mon'):
    wline(c, [(x + w / 2, y + h), (x + w / 2, y + h + 60)], (key, 's'), f, lw=18, col=STEELD, amp=0.6)
    rrect(c, x, y, w, h, 28); fs(c, hx('3A3F4F'), 10)
    rrect(c, x + 22, y + 22, w - 44, h - 44, 16); rgb(c, hx('0B1430')); c.fill()


def scene3(c, t, f, g):
    boh(c, f, g)
    c.save(); c.translate(0, 60)
    belt(c, -80, W + 80, 1300, g, f, sp=520)
    # first a typed letter, then the hero
    nx = lerp(-200, 1320, seg(t, 0.2, 2.0))
    env(c, nx, 1300 - 62, 0.62, 'neat', f, plain=True)
    if t < 3.6: hx_ = lerp(-220, 540, eout(seg(t, 1.9, 2.7)))
    else: hx_ = lerp(540, 1320, ein(seg(t, 3.6, 4.7)))
    unread = 2.9 < t < 3.6
    env(c, hx_, 1300 - 85, 0.85, 'hero', f, face='flat' if unread else 'smile', eyes='big' if unread else 'dot', look=(0, -1) if unread else (1, 0),
        postmark=True, rot=0.03 * math.sin(g * 9))
    # camera on an arm
    wline(c, [(540, 620), (540, 900)], 'cam1', f, lw=22, col=STEELD, amp=0.6)
    rrect(c, 430, 880, 220, 130, 26); fs(c, STEEL, 10)
    look_at = nx if t < 2.0 else hx_
    lx = clamp((look_at - 540) / 500, -1, 1) * 22
    c.new_path(); c.arc(540 + lx, 965, 46, 0, 2 * math.pi); fs(c, hx('10172B'), 8)
    c.new_path(); c.arc(540 + lx, 965, 20 * (0.5 if unread else 1), 0, 2 * math.pi); rgb(c, hx('6FE7FF')); c.fill()
    for dx in (-60, 0, 60):
        c.new_path(); c.move_to(540 + lx, 1012); c.line_to(look_at + dx, 1205); rgb(c, hx('6FE7FF'), 0.25 if 0.5 < t < 4.2 else 0); c.set_line_width(4); c.stroke()
    c.restore()
    # monitor shows what the camera sees
    monitor(c, f, 240, 560, 600, 300)
    c.save(); rrect(c, 262, 582, 556, 256, 16); c.clip()
    if 0.7 < t < 2.0:
        k = eout(seg(t, 0.7, 0.95))
        txt(c, "12 MAPLE ST", 540, 700, 62, hx('6FE7FF'), SANSF, a=k); txt(c, "SPRINGFIELD", 540, 778, 48, hx('6FE7FF'), SANSF, a=k)
    elif 2.75 <= t < 3.9:
        for k in range(2):
            pts = [(330 + i * 30, 690 + k * 70 + 22 * math.sin(i * 2.3 + k) + 6 * math.sin(g * 20 + i)) for i in range(15)]
            wline(c, pts, ('scr', k), f, lw=9, col=hx('6FE7FF'), amp=2.5)
    c.restore()
    okk = eback(seg(t, 1.1, 1.35)) * (1 - ein(seg(t, 1.9, 2.05)))
    if okk > 0.01:
        c.save(); c.translate(826, 580); c.scale(okk, okk); c.new_path(); c.arc(0, 0, 54, 0, 2 * math.pi); fs(c, GREEN, 8)
        wline(c, [(-24, 2), (-7, 20), (26, -18)], 'tk3', f, lw=13, col=WHITE, amp=0.5); c.restore()
    qk = eback(seg(t, 2.95, 3.2)) * (1 - ein(seg(t, 3.8, 3.95)))
    if qk > 0.01:
        c.save(); c.translate(826, 580); c.scale(qk, qk); c.new_path(); c.arc(0, 0, 56, 0, 2 * math.pi); fs(c, hx('FF4D4D'), 8)
        txt(c, "?", 0, 30, 82, WHITE); c.restore()
    caption(c, t, 0.25, [[("A CAMERA READS", CREAM)], [("THE ADDRESS.", GOLD)]], y=300, size=90, t1=2.45)
    caption(c, t, 2.5, [[("IT WORKS", CREAM)], [("99% OF THE TIME.", GOLD)]], y=300, size=90)


# ------------------------------------------------------------------ scene 4: one room in Utah
def scene4(c, t, f, g):
    bg(c, OFFICE, hx('F7FAFC'))
    c.rectangle(0, 1380, W, H - 1380); c.set_source(grad(0, 1380, 0, H, [(0, hx('C9D6E3')), (1, hx('AEBFD0'))])); c.fill()
    wline(c, [(0, 1380), (W, 1380)], 'fl4', f, lw=7, amp=0.8)
    rrect(c, 60, 600, 250, 300, 22); fs(c, hx('BFE4F5'), 8)
    wpoly(c, [(70, 890), (150, 760), (200, 830), (250, 720), (300, 890)], 'mts', f); rgb(c, hx('8FA3B8')); c.fill()
    # desk, monitor, keyer
    rrect(c, 300, 1150, 720, 40, 12); fs(c, WOOD, 8)
    for xx in (340, 980): wline(c, [(xx, 1190), (xx, 1380)], ('dl', xx), f, lw=18, col=WOODD, amp=0.6)
    monitor(c, f, 500, 760, 470, 320)
    arrive = eout(seg(t, 0.6, 1.1)); solved = t > 3.9
    c.save(); rrect(c, 522, 782, 426, 276, 16); c.clip()
    ox = lerp(480, 0, arrive)
    if not solved:
        for k in range(2):
            pts = [(570 + ox + i * 24, 880 + k * 64 + 20 * math.sin(i * 2.3 + k)) for i in range(15)]
            wline(c, pts, ('scr4', k), f, lw=8, col=hx('6FE7FF'), amp=2.0)
    else:
        kk = eout(seg(t, 3.9, 4.1))
        txt(c, "12 MAPLE ST", 735, 910, 52, hx('8CFFB0'), SANSF, a=kk); txt(c, "SPRINGFIELD", 735, 980, 42, hx('8CFFB0'), SANSF, a=kk)
    if 1.9 < t <= 3.9:
        q = seg(t, 1.9, 3.9)
        rrect(c, 560, 1016, 350, 22, 11); rgb(c, WHITE, 0.2); c.fill()
        rrect(c, 560, 1016, 350 * q, 22, 11); rgb(c, GOLD); c.fill()
    c.restore()
    typing = 1.9 < t <= 3.9
    tap = math.sin(g * 26) * 10 if typing else 0
    hd = stick(c, 330, 1190, 1.05, 'key', f, lh=(120, -60 + tap), rh=(170, -60 - tap), lf=(-30, 180), rf=(50, 180), face='flat' if not solved else 'grin',
               eyes='dot' if not solved else 'closed', shirt=CORAL, look=(1, 0.2), bob=math.sin(g * 3) * 2)
    c.new_path(); c.arc(hd[0], hd[1], hd[2] + 8, math.pi * 1.1, math.pi * 1.9); rgb(c, INK); c.set_line_width(11); c.stroke()
    c.new_path(); c.arc(hd[0] + hd[2] + 4, hd[1] + 6, 16, 0, 2 * math.pi); fs(c, hx('3A3F4F'), 5)
    rrect(c, 520, 1112, 240, 40, 10); fs(c, hx('3A3F4F'), 6)
    if solved:
        k = eback(seg(t, 3.95, 4.2))
        c.save(); c.translate(960, 770); c.scale(k, k); c.new_path(); c.arc(0, 0, 58, 0, 2 * math.pi); fs(c, GREEN, 8)
        wline(c, [(-26, 2), (-8, 22), (28, -20)], 'tk4', f, lw=14, col=WHITE, amp=0.5); c.restore()
    caption(c, t, 0.25, [[("THE REST? A PHOTO GOES", CREAM)], [("TO ONE ROOM IN UTAH.", GOLD)]], y=300, size=78, t1=2.55)
    caption(c, t, 2.6, [[("A HUMAN DECODES IT", CREAM)], [("IN A FEW SECONDS.", GOLD)]], y=300, size=80)
    k = eout(seg(t, 3.0, 3.3))
    if k > 0:
        c.save(); c.translate(540, 560)
        rrect(c, -330, -38, 660, 72, 24); rgb(c, INK, 0.88 * k); c.fill()
        txt(c, "About 2.3 million images a day.", 0, 12, 38, CREAM, HAND, a=k)
        c.restore()


# ------------------------------------------------------------------ scene 5: barcode and sorting
def scene5(c, t, f, g):
    boh(c, f, g, speed=1.4 if 1.6 < t < 3.2 else 0)
    c.save(); c.translate(540, 1270); c.scale(1.12, 1.12); c.translate(-540, -1300)
    fast = ease(seg(t, 1.5, 2.0)) * (1 - ease(seg(t, 3.3, 3.6)))
    belt(c, -80, 640, 1300, g, f, sp=300 + 900 * fast)
    if t < 1.5: bx = lerp(-200, 380, eout(seg(t, 0.0, 0.6)))
    elif t < 3.0: bx = 380 + 50 * math.sin(seg(t, 1.5, 3.0) * math.pi)
    else: bx = lerp(380, 800, ease(seg(t, 3.0, 3.5)))
    bar = seg(t, 0.7, 1.3)
    for k in range(4):
        if fast > 0.1 and t < 3.2:
            yy = 1150 - k * 34 + math.sin(g * 9 + k) * 5
            wline(c, [(bx - 330 - (k % 2) * 60, yy), (bx - 190, yy)], ('sl', k), f, lw=8, col=WHITE, amp=1.0, a=0.85 * fast)
    rrect(c, 650, 1250, 300, 230, 20); fs(c, hx('3A4670'), 9)
    for k in range(3):
        env(c, 720 + k * 46, 1292 - k * 6, 0.3, ('tr', k), f, plain=True, rot=-0.25 + k * 0.1)
    u = seg(t, 3.0, 3.8)
    hy = 1300 - 85 + 110 * ein(seg(t, 3.4, 3.8)) - 70 * math.sin(clamp(seg(t, 3.0, 3.5)) * math.pi)
    env(c, bx, hy, 0.85 - 0.2 * ease(seg(t, 3.3, 3.8)), 'hero', f, face='smile' if t < 1.5 else 'grin', eyes='closed' if t > 3.8 else 'dot', postmark=True,
        barcode=bar, look=(1, 0), rot=-0.06 * fast + 0.03 * math.sin(g * 14) + 0.5 * math.sin(clamp(seg(t, 3.0, 3.8)) * math.pi))
    rrect(c, 650, 1340, 300, 150, 20); fs(c, hx('4A5890'), 9)
    rrect(c, 674, 1372, 252, 84, 16); fs(c, GOLD, 7); txt(c, "MAPLE ST", 800, 1432, 46, INK)
    wline(c, [(380, 760), (380, 980)], 'nz1', f, lw=22, col=STEELD, amp=0.6)
    wpoly(c, [(346, 970), (414, 970), (396, 1040), (364, 1040)], 'nz2', f); fs(c, GOLD, 8)
    if 0.7 < t < 1.35:
        for k in range(7):
            ph = (g * 6 + k * 0.14) % 1
            c.new_path(); c.arc(380 + (k - 3) * 9 * ph * 3, 1050 + 120 * ph, 6, 0, 2 * math.pi); rgb(c, hx('FF7FB0'), 1 - ph); c.fill()
    if t > 3.85:
        k = eback(seg(t, 3.85, 4.1))
        c.save(); c.translate(960, 1250); c.scale(k, k); c.new_path(); c.arc(0, 0, 50, 0, 2 * math.pi); fs(c, GREEN, 8)
        wline(c, [(-22, 2), (-6, 19), (24, -17)], 'tk5', f, lw=13, col=WHITE, amp=0.5); c.restore()
    c.restore()
    caption(c, t, 0.25, [[("NOW IT GETS", CREAM)], [("A BARCODE.", GOLD)]], y=300, size=92, t1=2.05)
    caption(c, t, 2.1, [[("SORTED BY MACHINE", CREAM)], [("INTO DELIVERY ORDER.", GOLD)]], y=300, size=80)
    k = eout(seg(t, 2.6, 2.9))
    if k > 0:
        c.save(); c.translate(540, 560)
        rrect(c, -430, -32, 860, 62, 20); rgb(c, INK, 0.88 * k); c.fill()
        txt(c, "US figures. Sources: USPS Postal Facts, USPS Link, Postal Museum.", 0, 10, 27, CREAM, HAND, a=k)
        c.restore()


# ------------------------------------------------------------------ scene 6: the door
def granny(c, f, g, x, y, s, lh, rh, face, eyes, key='gran'):
    hd = stick(c, x, y, s, key, f, lh=lh, rh=rh, face=face, eyes=eyes, shirt=PINK, look=(-1, 0.2), bob=math.sin(g * 3) * 2)
    c.new_path(); c.arc(hd[0], hd[1] - hd[2] * 0.25, hd[2] * 1.02, math.pi, 2 * math.pi); c.close_path(); fs(c, hx('D9DDE6'), 6 * s)
    c.new_path(); c.arc(hd[0] + hd[2] * 0.2, hd[1] - hd[2] * 1.15, hd[2] * 0.42, 0, 2 * math.pi); fs(c, hx('D9DDE6'), 6 * s)
    for sg in (-1, 1):
        c.new_path(); c.arc(hd[0] + sg * hd[2] * 0.36, hd[1] - hd[2] * 0.06, hd[2] * 0.26, 0, 2 * math.pi); rgb(c, INK); c.set_line_width(5 * s); c.stroke()
    return hd


def scene6(c, t, f, g):
    bg(c, hx('9FDCF5'), hx('FFE9C9'))
    wrect(c, 380, 520, 760, 880, 'house', f); fs(c, hx('F7C9A8'), 9)
    wpoly(c, [(340, 520), (760, 330), (1180, 520)], 'roof6', f); fs(c, hx('D9705A'), 9)
    rrect(c, 820, 700, 200, 220, 16); fs(c, hx('BFE4F5'), 8)
    wline(c, [(920, 700), (920, 920)], 'wm', f, lw=7, amp=0.6); wline(c, [(820, 810), (1020, 810)], 'wm2', f, lw=7, amp=0.6)
    c.rectangle(0, 1400, W, H - 1400); c.set_source(grad(0, 1400, 0, H, [(0, hx('A8D08D')), (1, hx('8FBF7A'))])); c.fill()
    wline(c, [(0, 1400), (W, 1400)], 'gr6', f, lw=7, amp=0.8)
    op = ease(seg(t, 1.3, 1.8))
    rrect(c, 500, 900, 250, 500, 16); fs(c, hx('3A2A22'), 9)
    if op > 0.05:
        granny(c, f, g, 640, 1215, 0.95, lh=(-110, -150) if t > 2.2 else (-60, -20), rh=(50, -30), face='grin' if t > 2.3 else 'smile', eyes='closed' if t > 2.9 else 'dot')
    c.save(); c.translate(500, 900); c.scale(1 - 0.82 * op, 1)
    rrect(c, 0, 0, 250, 500, 16); fs(c, hx('2F9E8F'), 9)
    c.new_path(); c.arc(206, 260, 14, 0, 2 * math.pi); fs(c, GOLD, 5)
    c.restore()
    # the carrier walks in and hands over the hero
    cx = lerp(-160, 330, ease(seg(t, 0.2, 1.4)))
    walking = t < 1.4
    give = ease(seg(t, 1.9, 2.3))
    rh = lerp2((70, -60), (150, -180), give)
    hd = stick(c, cx, 1215, 0.95, 'car', f, lh=(-50, -20), rh=rh, lf=(-45 + (18 * math.sin(g * 10) if walking else 0), 190), rf=(45 - (18 * math.sin(g * 10) if walking else 0), 190),
               face='smile', eyes='dot', shirt=BLUE, look=(1, 0), hat='cap', bob=abs(math.sin(g * 10)) * 6 if walking else 0)
    rrect(c, cx - 96, 1215 - 120, 78, 96, 14); fs(c, hx('8A5A33'), 7)
    wline(c, [(cx - 60, 1215 - 120), (cx + 14, 1215 - 250)], 'strap', f, lw=9, col=hx('8A5A33'), amp=0.6)
    hand = (cx + rh[0] * 0.95, 1215 + rh[1] * 0.95)
    if t < 2.3:
        env(c, hand[0] + 30, hand[1] - 24, 0.42, 'hero', f, face='smile', eyes='dot', postmark=True, barcode=1.0, rot=0.08 * math.sin(g * 6))
    else:
        u = ease(seg(t, 2.3, 2.7))
        env(c, lerp(hand[0] + 30, 540, u), lerp(hand[1] - 24, 1000, u), lerp(0.42, 0.6, u), 'hero', f, face='grin', eyes='closed' if t > 3.0 else 'dot',
            postmark=True, barcode=1.0, rot=0.06 * math.sin(g * 5))
        for i in range(3):
            q = seg(t, 2.8 + i * 0.3, 4.2 + i * 0.3)
            if 0 < q < 1: heart(c, 600 + i * 60, 880 - 150 * q, 0.9 + 0.2 * i, CORAL, 1 - ein(q))
    caption(c, t, 0.3, [[("YOUR SCRIBBLE?", CREAM)], [("IT ARRIVED.", GOLD)]], y=300, size=96)


# ------------------------------------------------------------------ scene 7: on the fridge
def scene7(c, t, f, g):
    bg(c, hx('FFE9C9'), hx('FFF6E5'))
    rrect(c, 190, 520, 700, 1500, 50); fs(c, hx('E3EEF5'), 10)
    wline(c, [(190, 1180), (890, 1180)], 'fr', f, lw=8, amp=0.6)
    rrect(c, 240, 700, 30, 300, 15); fs(c, STEEL, 6); rrect(c, 240, 1260, 30, 300, 15); fs(c, STEEL, 6)
    sw = math.sin(g * 2.2) * 0.04
    env(c, 560, 860, 0.95, 'hero', f, face='smile', eyes='closed' if int(g * 1.2) % 3 == 0 else 'dot', postmark=True, barcode=1.0, rot=-0.08 + sw)
    c.new_path(); c.arc(560, 772, 26, 0, 2 * math.pi); fs(c, CORAL, 7)
    rrect(c, 640, 1010, 190, 150, 10); fs(c, WHITE, 6)
    wcirc(c, 700, 1070, 30, 'kd1', f, amp=3); rgb(c, hx('FFD23D')); c.fill()
    wline(c, [(660, 1140), (810, 1140)], 'kd2', f, lw=8, col=GREEN, amp=2.0)
    c.new_path(); c.arc(736, 1012, 16, 0, 2 * math.pi); fs(c, TEAL, 5)
    caption(c, t, 0.15, [[("WHEN DID YOU LAST", CREAM)], [("POST A LETTER?", GOLD)]], y=300, size=88)


SCENES = [(0.0, 3.2, scene1), (3.2, 7.8, scene2), (7.8, 12.6, scene3), (12.6, 18.2, scene4), (18.2, 22.8, scene5),
          (22.8, 27.4, scene6), (27.4, 30.0, scene7)]
TR = 0.22


def draw(c, g, f):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= g < b or (i == len(SCENES) - 1 and g >= b):
            loc = g - a
            if i >= 2 and loc < TR:
                o = eout(loc / TR)
                pa, pb, pfn = SCENES[i - 1]
                c.save(); c.translate(0, -H * o); c.rectangle(0, 0, W, H); c.clip(); pfn(c, pb - pa - 0.001, f, pb - 0.001); c.restore()
                c.save(); c.translate(0, H * (1 - o)); c.rectangle(0, 0, W, H); c.clip(); fn(c, loc, f, g); c.restore()
            else:
                c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, loc, f, g); c.restore()
            return
