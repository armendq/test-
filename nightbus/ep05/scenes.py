from ep2 import *

SHEET = hx('FBFAF4'); BLANK = hx('F4ECD6'); BLANKS = hx('7FA3E0'); PEGW = hx('E6BE7E'); EYE = hx('1A1F3D')
HOUSEC = hx('4B4585'); HOUSED = hx('37326B'); ROOFC = hx('7A4560'); OWLL = hx('EBDCBE'); OWLD = hx('5E452E'); HEDGE = hx('2F5A3C')
RND = cairo.LINE_CAP_ROUND


# ------------------------------------------------------------------ helpers copied from episodes 3 and 4
def feather(c, x, y, s, rot, f, key='fe'):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.save(); c.scale(0.34, 1.0); c.new_path(); c.arc(0, -50, 52, 0, 2 * math.pi); c.restore(); fs(c, OWLL, 5)
    wline(c, [(0, 10), (0, -100)], (key, 'q'), f, lw=5, col=OWLD, amp=0.3)
    c.restore()


def souvenirs(c, f):
    kid_drawing(c, 196, 560, 0.52, f, rot=-0.07)
    c.save(); c.translate(330, 742); c.rotate(0.12)
    rrect(c, -44, -60, 88, 120, 10); fs(c, WHITE, 6)
    for k in range(3):
        c.rectangle(-28, -36 + k * 26, 56, 9); rgb(c, CORAL if k == 0 else hx('B9C0D6')); c.fill()
    c.new_path(); c.arc(0, -60, 9, 0, 2 * math.pi); fs(c, TEAL, 4)
    c.restore()


def ltag(c, x, y, s, rot, f, key='lt', string=True):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    if string: wline(c, [(0, -44), (0, -80)], (key, 's'), f, lw=5, amp=0.5)
    c.new_path(); c.move_to(-24, -28); c.line_to(0, -48); c.line_to(24, -28); c.line_to(24, 46); c.line_to(-24, 46); c.close_path(); fs(c, PAPER, 6)
    c.new_path(); c.arc(0, -27, 6, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.rectangle(-14, -8, 28, 9); rgb(c, CORAL); c.fill()
    c.rectangle(-14, 10, 28, 5); rgb(c, INK, 0.5); c.fill(); c.rectangle(-14, 24, 18, 5); c.fill()
    c.restore()


def bush(c, x, base, s):
    B = ((-52, -44, 52), (0, -72, 64), (56, -40, 50))
    for (ax, ay, r) in B:
        c.new_path(); c.arc(x + ax * s, base + ay * s, (r + 7) * s, math.pi, 2 * math.pi); c.close_path(); rgb(c, INK); c.fill()
    for (ax, ay, r) in B:
        c.new_path(); c.arc(x + ax * s, base + ay * s, r * s, 0, 2 * math.pi); rgb(c, HEDGE); c.fill()


def road2(c, y, off):
    c.rectangle(-400, y, W + 800, 96); rgb(c, hx('2A3044')); c.fill()
    c.rectangle(-400, y, W + 800, 8); rgb(c, hx('4A5594')); c.fill()
    for k in range(9):
        xx = ((k * 170 + off) % 1530) - 220
        rrect(c, xx, y + 42, 90, 12, 6); rgb(c, hx('E9DFC8'), 0.8); c.fill()


def drops(c, x, y, g, n=3):
    for k in range(n):
        ph = (g * 1.4 + k / n) % 1
        c.new_path(); c.arc(x + k * 12, y + ph * 60, 6 * (1 - ph) + 3, 0, 2 * math.pi); rgb(c, hx('BFE4FF'), 0.9 * (1 - ph)); c.fill()


def stop_lamp(c, x, y, on, f):
    if on:
        gl = cairo.RadialGradient(x, y, 20, x, y, 260)
        gl.add_color_stop_rgba(0, 1, 0.3, 0.25, 0.5); gl.add_color_stop_rgba(1, 1, 0.3, 0.25, 0)
        c.set_source(gl); c.rectangle(x - 280, y - 260, 560, 520); c.fill()
    rrect(c, x - 138, y - 52, 276, 104, 20); fs(c, hx('121A40'), 8)
    txt(c, "STOP", x + 30, y + 23, 64, hx('FF4D4D') if on else hx('4A2F45'), SANS)
    col = GOLD if on else hx('6B5A3A')
    c.new_path(); c.arc(x - 88, y + 2, 24, math.pi, 2 * math.pi); c.line_to(x - 58, y + 16); c.line_to(x - 118, y + 16); c.close_path(); rgb(c, col); c.fill()
    c.new_path(); c.arc(x - 88, y + 24, 7, 0, 2 * math.pi); c.fill()


# ------------------------------------------------------------------ the ghost and its things
def ghost(c, x, y, s, key, f, g, own=False, eyes='open', look=(0, 0), rot=0.0, arms=None, blush=1.0, sq=1.0, holes=1.0):
    """x, y = middle of the hem. About 180 wide and 250 tall at s=1. own=False wears Otto's striped cloth."""
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    col = SHEET if own else BLANK
    if arms:
        for i, hd in enumerate(arms):
            if hd is None: continue
            sg = -1 if i == 0 else 1
            wline(c, [(sg * 60, -126), hd], (key, 'arm', i), f, lw=48, col=INK, amp=0.6)
            wline(c, [(sg * 60, -126), hd], (key, 'arm2', i), f, lw=32, col=col, amp=0.4)
    c.new_path(); c.move_to(-88, 0)
    c.curve_to(-98, -130, -86, -250, 0, -250); c.curve_to(86, -250, 98, -130, 88, 0)
    n = 4; wd = 176 / n
    for i in range(n):
        x1 = 88 - i * wd; x2 = x1 - wd; dip = 17 + 7 * math.sin(g * 5 + i * 1.9)
        c.curve_to(x1 - wd * 0.2, dip, x2 + wd * 0.2, dip, x2, 0)
    c.close_path(); path = c.copy_path(); fs(c, col, 8)
    c.save(); c.new_path(); c.append_path(path); c.clip()
    if not own:
        for yy in (-62, -38):
            c.rectangle(-120, yy, 240, 11); rgb(c, BLANKS); c.fill()
    else:
        heart(c, 44, -64, 0.42, CORAL)
    c.restore()
    c.new_path(); c.append_path(path); rgb(c, INK); c.set_line_width(8); c.set_line_join(cairo.LINE_JOIN_ROUND); c.stroke()
    if holes > 0.02:
        for sg in (-1, 1):
            ex, ey = sg * 32 + look[0] * 7, -160 + look[1] * 6
            if eyes == 'closed':
                c.new_path(); c.arc(ex, ey + 9, 17, 1.15 * math.pi, 1.85 * math.pi); rgb(c, EYE); c.set_line_width(8); c.set_line_cap(RND); c.stroke()
            else:
                rx, ry = (20, 27) if eyes == 'big' else (15, 21)
                c.save(); c.translate(ex, ey); c.scale(rx * holes, ry * holes); c.new_path(); c.arc(0, 0, 1, 0, 2 * math.pi); c.restore(); rgb(c, EYE); c.fill()
                if eyes == 'big':
                    c.new_path(); c.arc(ex - 6, ey - 9, 5.5 * holes, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
        if blush > 0.02:
            for sg in (-1, 1):
                c.new_path(); c.arc(sg * 58, -120, 14, 0, 2 * math.pi); rgb(c, hx('FF8FA3'), 0.6 * blush); c.fill()
    c.restore()


def peg(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rrect(c, -11, -38, 22, 76, 7); fs(c, PEGW, 5)
    c.new_path(); c.move_to(0, 4); c.line_to(0, 38); rgb(c, INK); c.set_line_width(4.5); c.stroke()
    c.new_path(); c.arc(0, 4, 5, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.rectangle(-14, -14, 28, 7); rgb(c, hx('9AA3C7')); c.fill_preserve(); rgb(c, INK); c.set_line_width(2.5); c.stroke()
    c.restore()


def cloth(c, x, y, w, h, rot, f, key='cl', own=False):
    c.save(); c.translate(x, y); c.rotate(rot)
    r = min(w, h) * 0.2
    rrect(c, -w / 2, -h / 2, w, h, r); fs(c, SHEET if own else BLANK, 7)
    if not own:
        c.save(); rrect(c, -w / 2, -h / 2, w, h, r); c.clip()
        for u in (0.60, 0.78):
            c.rectangle(-w / 2, -h / 2 + h * u, w, h * 0.09); rgb(c, BLANKS); c.fill()
        c.restore()
        rrect(c, -w / 2, -h / 2, w, h, r); rgb(c, INK); c.set_line_width(7); c.stroke()
    c.restore()


def strap(c, x, y, ang, f, L=92):
    c.save(); c.translate(x, y); c.rotate(ang)
    wline(c, [(0, 0), (0, L)], ('bs', x), f, lw=12, col=INK, amp=0.3)
    wline(c, [(0, 0), (0, L)], ('bs2', x), f, lw=6, col=GOLD, amp=0.2)
    c.new_path(); c.arc(0, L + 20, 20, 0, 2 * math.pi); rgb(c, INK); c.set_line_width(14); c.stroke()
    c.new_path(); c.arc(0, L + 20, 20, 0, 2 * math.pi); rgb(c, GOLD); c.set_line_width(7); c.stroke()
    c.restore()


def note(c, x, y, s, col, a=1.0):
    if a <= 0.01: return
    c.save(); c.translate(x, y); c.scale(s, s)
    c.save(); c.rotate(-0.35); c.scale(1.25, 0.9); c.new_path(); c.arc(0, 0, 13, 0, 2 * math.pi); c.restore(); rgb(c, col, a); c.fill()
    c.new_path(); c.move_to(13, -2); c.line_to(13, -56); c.line_to(36, -46); c.set_line_width(6); c.set_line_cap(RND)
    c.set_line_join(cairo.LINE_JOIN_ROUND); rgb(c, col, a); c.stroke()
    c.restore()


def rays(c, x, y, r0, r1, n, col, a, f, key, lw=6, a0=0.0, span=2 * math.pi):
    for i in range(n):
        an = a0 + span * i / (n if span >= 6.2 else max(1, n - 1))
        wline(c, [(x + math.cos(an) * r0, y + math.sin(an) * r0), (x + math.cos(an) * r1, y + math.sin(an) * r1)], (key, i), f, lw=lw, col=col, amp=0.5, a=a)


def house_card(c, x, y, k, f, rot=0.0):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k); c.rotate(rot)
    rrect(c, -192, -142, 400, 300, 16); rgb(c, INK, 0.3); c.fill()
    rrect(c, -200, -150, 400, 300, 16); fs(c, PAPER, 8)
    c.save(); rrect(c, -182, -132, 364, 264, 10); c.clip()
    c.rectangle(-200, -150, 400, 300); rgb(c, hx('27326A')); c.fill()
    c.rectangle(-200, 96, 400, 60); rgb(c, hx('24402F')); c.fill()
    c.rectangle(24, -36, 132, 134); rgb(c, hx('6A63B0')); c.fill()
    c.new_path(); c.move_to(4, -36); c.line_to(90, -112); c.line_to(176, -36); c.close_path(); rgb(c, hx('A0577A')); c.fill()
    for wx in (48, 104):
        c.rectangle(wx, -10, 30, 36); rgb(c, hx('FFD98A')); c.fill()
    c.new_path(); c.move_to(-150, 98); c.line_to(-150, -24); c.move_to(-150, -16); c.line_to(24, -16); rgb(c, CREAMT); c.set_line_width(6); c.stroke()
    c.rectangle(-116, -14, 76, 90); rgb(c, WHITE); c.fill()
    c.restore()
    wline(c, [(-164, -112), (-104, -40)], 'hca', f, lw=10, col=CORAL, amp=0.5)
    wline(c, [(-132, -44), (-100, -34), (-96, -68)], 'hcb', f, lw=10, col=CORAL, amp=0.5)
    c.new_path(); c.arc(0, -150, 12, 0, 2 * math.pi); fs(c, TEAL, 5)
    c.restore()


# ------------------------------------------------------------------ sets
def cabin(c, f, g, head, moving=1.0, lhand=None):
    """the driver's seat seen from the aisle. lhand = Otto's left paw in bus coordinates"""
    c.save(); c.translate(430, 1080); c.scale(1.75, 1.75); c.translate(-150, -960)
    bus_int_back(c, f, g, None, moving=moving, door=0.0, bars=False)
    wcirc(c, 150, 1150, 108, 'ob', f, amp=1.2, ry=140); fs(c, UNI, 9)
    for i in range(2):
        c.new_path(); c.arc(150, 1080 + i * 46, 7, 0, 2 * math.pi); rgb(c, GOLD); c.fill()
    head()
    if lhand:
        wline(c, [(72, 1085), lhand], 'la', f, lw=40, col=INK, amp=0.8); wline(c, [(72, 1085), lhand], 'la2', f, lw=28, col=UNI, amp=0.5)
        c.new_path(); c.arc(lhand[0], lhand[1], 22, 0, 2 * math.pi); fs(c, STRIPE, 6)
    bus_int_front(c, f, g)
    wline(c, [(215, 1085), (262, 1010)], 'oa', f, lw=40, col=INK, amp=0.8); wline(c, [(215, 1085), (262, 1010)], 'oa2', f, lw=28, col=UNI, amp=0.5)
    c.new_path(); c.arc(264, 1004, 22, 0, 2 * math.pi); fs(c, STRIPE, 6)
    c.restore()


def cab(p): return (430 + 1.75 * (p[0] - 150), 1080 + 1.75 * (p[1] - 960))


def mirror(c, f, sw=0.0, dent=0.0):
    wline(c, [(790, 318), (790, 494)], 'mir', f, lw=14, amp=0.4)
    rrect(c, 548, 482, 484, 286, 44); fs(c, hx('C9CFE6'), 10)
    rrect(c, 574, 508, 432, 234, 26); fs(c, hx('0A0F24'), 8)
    c.save(); rrect(c, 578, 512, 424, 226, 22); c.clip()
    for sx in (610, 760, 910):
        rrect(c, sx - 60, 624 + (dent if sx == 760 else 0), 120, 200, 24); rgb(c, hx('1B2550')); c.fill()
    c.new_path(); c.move_to(600, 742); c.line_to(690, 508); c.line_to(730, 508); c.line_to(640, 742); c.close_path(); rgb(c, WHITE, 0.07); c.fill()
    c.new_path(); c.move_to(838, 512); c.line_to(838 + sw, 590); rgb(c, GOLD); c.set_line_width(7); c.stroke()
    c.new_path(); c.arc(838 + sw * 1.2, 608, 17, 0, 2 * math.pi); rgb(c, GOLD); c.set_line_width(7); c.stroke()
    c.restore()


def collection(c, f, g, peg_at=None):
    souvenirs(c, f)
    feather(c, 92, 830, 0.95, 0.3, f, key='pinf')
    c.new_path(); c.arc(98, 812, 9, 0, 2 * math.pi); fs(c, CORAL, 4)
    ltag(c, 212, 800 + 4 * math.sin(g * 3), 1.5, -0.08 + 0.05 * math.sin(g * 3), f, key='pint', string=False)
    c.new_path(); c.arc(212, 760, 9, 0, 2 * math.pi); fs(c, GOLD, 4)
    if peg_at:
        peg(c, peg_at[0], peg_at[1], 1.9, 0.1 + 0.03 * math.sin(g * 3))
        c.new_path(); c.arc(peg_at[0] + 6, peg_at[1] - 56, 9, 0, 2 * math.pi); fs(c, CORAL, 4)


def bench7(c, f, dent=0.0):
    rrect(c, 800, 1000, 64, 262, 24); fs(c, SEATD, 8)
    rrect(c, 650, 1220, 214, 90, 26); fs(c, SEAT, 8)
    if dent > 0.02:
        c.rectangle(674, 1211, 132, 10); rgb(c, WALL); c.fill()
        c.save(); c.translate(740, 1219); c.scale(1, dent * 0.27); c.new_path(); c.arc(0, 0, 66, 0, math.pi); c.close_path(); c.restore(); rgb(c, WALL); c.fill()
        c.save(); c.translate(740, 1219); c.scale(1, dent * 0.27); c.new_path(); c.arc(0, 0, 66, 0, math.pi); c.restore()
        rgb(c, INK); c.set_line_width(8); c.set_line_cap(RND); c.stroke()
    wline(c, [(676, 1310), (676, 1400)], 'bl', f, lw=12); wline(c, [(836, 1310), (836, 1400)], 'br', f, lw=12)
    c.new_path(); c.arc(832, 1062, 25, 0, 2 * math.pi); fs(c, GOLD, 6); txt(c, "7", 832, 1076, 38, INK, SANS)


def rear_set(c, f, g, dent=0.0):
    rear(c, f, g)
    for wx in (210, 500):                          # the bus stands still: night and rain in the windows
        rrect(c, wx, 610, 230, 320, 26); fs(c, hx('121A40'), 9)
        for k in range(6):
            yy = 620 + ((k * 0.17 + g * 0.5) % 1) * 290
            c.new_path(); c.move_to(wx + 25 + k * 36, yy); c.line_to(wx + 21 + k * 36, yy + 24); rgb(c, hx('BFD4FF'), 0.5); c.set_line_width(3); c.stroke()
    bench7(c, f, dent)


def rcam(c, u=0.0, pan=0.0):
    """rear view of the bus. u=0 is the old rear_cam, u=1 pushes in a little and keeps the ceiling line in place"""
    sc = 1.3 + 0.1 * u
    c.translate(-sc * (250 + 10 * u + pan), 301 - sc * 524); c.scale(sc, sc)


# ------------------------------------------------------------------ scene A 0-3.6: who rang the bell
LAMP = (790, 1080)


def scA(c, t, f, g):
    k = ease(seg(t, 0.6, 1.3)); z = lerp(1.5, 1.0, k)
    fx, fy = lerp(626.67, 540, k), lerp(882.67, 960, k)
    BR, D2, D3 = 1.55, 2.1, 3.0
    qb = t - BR; q2 = t - D2; q3 = t - D3
    sh = 13 * math.exp(-7 * qb) * math.sin(qb * 50) if 0 <= qb < 0.6 else 0
    c.save(); c.translate(W / 2 + sh, H / 2); c.scale(z, z); c.translate(-fx, -fy)

    def head():
        jump = (20 * math.sin(clamp(q2 / 0.3) * math.pi) if q2 > 0 else 0) + (18 * math.sin(clamp(q3 / 0.3) * math.pi) if q3 > 0 else 0)
        look = (0.9, 0.3) if t < 1.35 else ((0.9, -0.8) if (t < 2.9 or t > 3.3) else (0.9, 0.3))
        otto_head(c, 150 + math.sin(g * 44) * 2.0, 935 - jump, 98, 'oh', f, eyes='wide', mouth='o', look=look)
        drops(c, 54, 800, g); drops(c, 240, 806, g + 0.3)
    cabin(c, f, g, head, moving=1.0 if t < BR else 0.0)
    collection(c, f, g)
    ring = t < 1.45 or q3 >= 0
    on = (t < 0.45) or (t < 1.45 and int(t * 5) % 2 == 0) or (q3 >= 0 and (q3 < 0.35 or int(q3 * 5) % 2 == 0))
    stop_lamp(c, LAMP[0], LAMP[1], on, f)
    if ring:
        bxp, byp = LAMP[0] - 88, LAMP[1] + 4
        for i in range(3):
            ph = (t * 2.6 + i / 3) % 1
            for sg in (-1, 1):
                c.new_path(); c.arc(bxp, byp, 34 + 46 * ph, -math.pi / 2 + sg * 0.5 - 0.42, -math.pi / 2 + sg * 0.5 + 0.42)
                rgb(c, GOLD, 0.95 * (1 - ph)); c.set_line_width(6); c.set_line_cap(RND); c.stroke()
    for i, (td, dx, dy) in enumerate(((-0.3, 800, 985), (0.42, 700, 890), (D3, 800, 985), (D3 + 0.22, 700, 890))):
        kk = eback(seg(t, td, td + 0.16)) * (1 - ein(seg(t, td + 0.55, td + 0.75)))
        if kk > 0.01:
            c.save(); c.translate(dx, dy); c.scale(kk, kk); c.rotate(-0.12 + 0.12 * (i % 2))
            txt(c, "DING!", 0, 0, 72, GOLD, SERIF); c.restore()
    sw = 46 * math.exp(-0.7 * t) * math.sin(t * 10 + 1.2) + (44 * math.exp(-0.9 * q3) * math.sin(q3 * 10) if q3 > 0 else 0)
    dent = (9 + 12 * math.exp(-3 * q2) * abs(math.cos(q2 * 9))) if q2 >= 0 else 0
    mirror(c, f, sw, dent)
    if 0 <= q2 < 0.45:
        u = q2 / 0.45
        for sg in (-1, 1):
            wline(c, [(760 + sg * (66 + 26 * u), 628 - 6 * u), (760 + sg * (84 + 40 * u), 610 - 14 * u)], ('md', sg), f, lw=6, col=WHITE, amp=0.6, a=0.9 * (1 - u))
    c.restore()
    if k < 1:                                        # the tight shot gets a calm dark band behind the caption
        gl = cairo.LinearGradient(0, 0, 0, 480)
        gl.add_color_stop_rgba(0, NAVY[0], NAVY[1], NAVY[2], 0.96 * (1 - k)); gl.add_color_stop_rgba(0.62, NAVY[0], NAVY[1], NAVY[2], 0.82 * (1 - k))
        gl.add_color_stop_rgba(1, NAVY[0], NAVY[1], NAVY[2], 0)
        c.set_source(gl); c.rectangle(0, 0, W, 480); c.fill()
    cap2(c, t, -1, ["Who rang the bell?"], y=250, size=88, gold=True, t1=2.25)
    cap2(c, t, 2.35, ["The bus is empty."], y=250, size=86)


# ------------------------------------------------------------------ scene B 3.6-8: nobody there, somebody there
def fog_face(c, t, f, g):
    """window 2 of the rear set fogs up and a finger nobody can see draws a sad face"""
    fog = ease(seg(t, 2.3, 2.85))
    if fog <= 0.01: return
    cx, cy = 615, 778
    c.save(); rrect(c, 505, 615, 220, 310, 22); c.clip()
    gl = cairo.RadialGradient(cx, cy, 30, cx, cy, 140)
    gl.add_color_stop_rgba(0, 0.82, 0.87, 0.97, 0.62 * fog); gl.add_color_stop_rgba(0.8, 0.82, 0.87, 0.97, 0.5 * fog); gl.add_color_stop_rgba(1, 0.82, 0.87, 0.97, 0)
    c.set_source(gl); c.rectangle(440, 600, 360, 360); c.fill()
    clear = hx('0F1638'); tip = None
    for i, (ex, t0) in enumerate(((cx - 34, 2.9), (cx + 34, 3.1))):
        k = eout(seg(t, t0, t0 + 0.14))
        if k > 0:
            c.new_path(); c.arc(ex, cy - 30, 13 * k, 0, 2 * math.pi); rgb(c, clear); c.fill()
            if k < 1: tip = (ex, cy - 30)
    p = seg(t, 3.3, 3.8)
    if p > 0:
        a0, a1 = 1.2 * math.pi, 1.8 * math.pi; a = a0 + (a1 - a0) * p
        c.new_path(); c.arc(cx, cy + 62, 40, a0, a); rgb(c, clear); c.set_line_width(13); c.set_line_cap(RND); c.stroke()
        if p < 1: tip = (cx + 40 * math.cos(a), cy + 62 + 40 * math.sin(a))
    d = seg(t, 3.95, 4.38)
    if d > 0:
        y0 = cy - 18; y1 = y0 + 74 * ein(d) + 18 * d
        c.new_path(); c.move_to(cx - 34, y0); c.line_to(cx - 34, y1); rgb(c, clear); c.set_line_width(9); c.set_line_cap(RND); c.stroke()
        c.new_path(); c.arc(cx - 34, y1, 8, 0, 2 * math.pi); rgb(c, hx('BFE4FF')); c.fill()
    c.restore()
    if tip:
        sparkle(c, tip[0], tip[1], 16 + 5 * math.sin(g * 40), WHITE, 0.95)
        for i in range(2):
            wline(c, [(tip[0] + 22 + i * 12, tip[1] - 20 - i * 8), (tip[0] + 34 + i * 12, tip[1] - 30 - i * 8)], ('sq', i), f, lw=5, col=WHITE, amp=0.8, a=0.8)


def scB(c, t, f, g):
    S = 0.9; D, ST = 1.25, 1.95
    q = t - D; qs = t - ST
    c.save(); rcam(c)
    dent = (1 + 0.55 * math.exp(-5 * q) * math.cos(q * 22)) if q >= 0 else 0
    rear_set(c, f, g, dent=dent)
    sw = 0.62 * math.exp(-0.8 * qs) * math.sin(qs * 9 + 0.6) if qs >= 0 else 0.03 * math.sin(g * 2)
    strap(c, 470, 566, sw, f)
    fog_face(c, t, f, g)
    if 0 <= q < 0.4:
        u = q / 0.4
        for sg in (-1, 1):
            wline(c, [(740 + sg * (78 + 24 * u), 1206 - 10 * u), (740 + sg * (96 + 40 * u), 1184 - 22 * u)], ('dn', sg), f, lw=6, col=WHITE, amp=0.6, a=0.9 * (1 - u))
        wcirc(c, 740, 1196 - 26 * u, 16 + 22 * u, 'dpf', f, amp=2); rgb(c, WHITE, 0.5 * (1 - u)); c.fill()
    walking = t < 1.1
    ox = lerp(286, 400, ease(seg(t, 0.0, 1.1)))
    bob = abs(math.sin(g * 9)) * 7 if walking else 0
    jump = 34 * math.sin(clamp(q / 0.32) * math.pi) if q > 0 else 0
    jit = math.sin(g * 46) * 2.2 if (0 < q < 0.7 or 0 < qs < 0.5) else 0
    if t < D: look, eyes, mouth = (1, 0.1), 'open', 'flat'
    elif t < ST: look, eyes, mouth = (1, 0.5), 'wide', 'o'
    elif t < 2.45: look, eyes, mouth = (0.75, -1), 'wide', 'o'
    elif t < 3.95: look, eyes, mouth = (1, -0.75), 'wide', 'flat'
    else: look, eyes, mouth = (1, -0.6), 'open', 'o'
    lh = (-98, 40); rh = (98, 40)
    if D <= t < 2.45: lh, rh = (-112, -150), (112, -150)
    elif t >= 3.95: rh = lerp2((98, 40), (104, -120), ease(seg(t, 3.95, 4.25)))
    otto_full(c, ox + jit, 1400 - jump, S, 'of', f, eyes=eyes, mouth=mouth, look=look, lh=lh, rh=rh, bob=bob, tilt=0.06 if t >= 3.95 else 0)
    hy = 1400 - 392 * S - jump
    if D <= t < 1.85: txt(c, "!", ox + 118, hy - 20, 110, GOLD, SERIF)
    elif 2.5 <= t < 3.9: txt(c, "?", ox + 118, hy - 20, 100, CREAMT, SERIF)
    if t >= D: drops(c, ox - 86, hy + 30, g)
    c.restore()
    cap2(c, t, 0.2, ["Nobody there."], y=240, size=88, t1=2.15)
    cap2(c, t, 2.25, ["Somebody there."], y=240, size=88, gold=True)


# ------------------------------------------------------------------ scene C 8-12.4: one spare sheet
GX, GY_ = 742, 1228          # where the ghost sits on seat 7
GS = 0.95


def scC(c, t, f, g):
    S = 0.9; ox = 400
    u = ease(seg(t, 1.5, 2.2))
    c.save(); rcam(c, u)
    LAND, EYES, GIVE = 1.55, 1.85, 3.4
    rear_set(c, f, g, dent=1.0 if t < LAND else 0)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    # Otto: finds the cloth, winds up, throws
    if t < 0.35: rh = (98, 40)
    elif t < 0.7: rh = lerp2((98, 40), (136, -96), ease(seg(t, 0.35, 0.7)))
    elif t < 0.92: rh = lerp2((136, -96), (40, -176), ease(seg(t, 0.7, 0.92)))
    elif t < 1.08: rh = lerp2((40, -176), (168, -120), eout(seg(t, 0.92, 1.08)))
    elif t < 1.7: rh = lerp2((168, -120), (98, 40), ease(seg(t, 1.2, 1.7)))
    elif t >= GIVE + 0.3: rh = lerp2((98, 40), (142, -30), ease(seg(t, GIVE + 0.3, GIVE + 0.7)))
    else: rh = (98, 40)
    sal = ease(seg(t, 2.65, 2.9)) * (1 - ease(seg(t, 3.25, 3.5)))
    lh = lerp2((-98, 40), (-70, -150), sal)
    if t < LAND: eyes, mouth, look = 'open', ('smile' if t > 0.3 else 'flat'), (1, 0.2)
    elif t < 2.3: eyes, mouth, look = 'wide', 'o', (1, 0.1)
    elif t < GIVE: eyes, mouth, look = 'open', 'smile', (1, 0.1)
    else: eyes, mouth, look = 'wide', 'o', (1, 0.0)
    otto_full(c, ox, 1400, S, 'of', f, eyes=eyes, mouth=mouth, look=look, lh=lh, rh=rh, bob=math.sin(g * 3) * 2)
    hand = (ox + rh[0] * S, 1400 + (rh[1] - 175) * S)
    if 0.1 < t < 0.75:
        kk = eback(seg(t, 0.1, 0.32)) * (1 - ein(seg(t, 0.6, 0.75)))
        sparkle(c, ox + 96, 1400 - 430 * S, 34 * kk, GOLD)
    if 0.4 <= t < 1.0:                               # the folded cloth in his paw
        kk = eback(seg(t, 0.4, 0.62))
        cloth(c, hand[0] + 14, hand[1] - 26, 84 * kk, 58 * kk, -0.12, f, 'fold')
    elif 1.0 <= t < LAND:                            # it flies and opens
        p = seg(t, 1.0, LAND); e = ease(p)
        x0, y0 = ox + 168 * S + 14, 1400 + (-120 - 175) * S - 26
        cx_ = lerp(x0, GX, e); cy_ = lerp(y0, GY_ - 150, e) - 170 * math.sin(p * math.pi)
        cloth(c, cx_, cy_, lerp(84, 200, e), lerp(58, 178, e), -0.12 + 5.2 * e + 0.15 * math.sin(p * 12), f, 'fly')
        for i in range(3):
            wline(c, [(cx_ - 90 - i * 26, cy_ + 30 + i * 12), (cx_ - 130 - i * 26, cy_ + 44 + i * 12)], ('fl', i), f, lw=6, col=WHITE, amp=1.0, a=0.6)
    if t >= LAND:
        ql = t - LAND
        sq = lerp(0.42, 1.0, eback(seg(t, LAND, LAND + 0.3)))
        hop = 0
        if 2.65 <= t < 3.3: hop = 26 * abs(math.sin((t - 2.65) / 0.325 * math.pi))
        holes = eback(seg(t, EYES, EYES + 0.18))
        blink = 2.42 < t < 2.52
        shy = 1.9 <= t < 2.65
        gv = ease(seg(t, GIVE, GIVE + 0.3))
        arms = ((lerp(-70, -168, gv), lerp(-110, -150, gv)), None) if gv > 0.02 else None
        if 2.65 <= t < 3.3: arms = ((-130, -224), (130, -224))
        ghost(c, GX, GY_ - hop, GS, 'gh', f, g, eyes='closed' if (blink or 2.65 <= t < 3.3) else ('big' if t >= GIVE else 'open'),
              look=(-0.7, 0.7) if shy else (-1, 0.0), rot=-0.07 if shy else 0.04 * math.sin(g * 4), arms=arms, blush=ease(seg(t, 2.0, 2.4)),
              sq=sq, holes=holes)
        if ql < 0.35:
            for i in range(6):
                wcirc(c, GX - 120 + i * 48 + (i - 2.5) * 30 * ql / 0.35, GY_ - 6 - (i % 2) * 14 - 40 * ql, 26 * (1 - ql / 0.35) + 5, ('pf', i), f, amp=2)
                rgb(c, WHITE, 0.8 * (1 - ql / 0.35)); c.fill()
        if gv > 0.02:
            px = GX + lerp(-70, -168, gv) * GS - 22; py = GY_ - hop + lerp(-110, -150, gv) * GS - 22
            peg(c, px, py, 1.5 * eback(seg(t, GIVE + 0.05, GIVE + 0.3)), -0.5)
            if GIVE + 0.3 < t:
                qq = (t - GIVE - 0.3) % 0.6 / 0.6
                rays(c, px, py, 52 + 20 * qq, 72 + 34 * qq, 7, GOLD, 1 - qq, f, 'pr')
        for i in range(2):
            hq = seg(t, 2.7 + i * 0.3, 3.9 + i * 0.3)
            if 0 < hq < 1: heart(c, GX - 20 + i * 70, GY_ - 270 - 90 * hq, 0.7 + 0.15 * i, CORAL, 1 - ein(hq))
    if t >= GIVE + 0.25: txt(c, "?", ox + 118, 1400 - 392 * S - 20, 100, CREAMT, SERIF)
    c.restore()
    if LAND + 0.28 <= t < LAND + 0.4:
        c.rectangle(0, 0, W, H); rgb(c, WHITE, 0.32 * (1 - (t - LAND - 0.28) / 0.12)); c.fill()
    cap2(c, t, 0.15, ["Otto has an idea."], y=240, size=86, t1=1.8)
    cap2(c, t, 1.95, ["A ghost who lost its sheet."], y=240, size=82, gold=True)


# ------------------------------------------------------------------ scene D 12.4-16.8: the fare, then the road
CUT = 1.75


def fare(c, t, f, g):
    S = 0.9; ox = 400
    c.save(); rcam(c, 1.0)
    rear_set(c, f, g)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    if t < 0.3: rh = lerp2((142, -30), (176, -64), ease(seg(t, 0.0, 0.3)))
    elif t < 0.55: rh = (176, -64)
    else: rh = lerp2((176, -64), (60, -300), ease(seg(t, 0.55, 0.95)))
    sal = ease(seg(t, 1.1, 1.35))
    otto_full(c, ox, 1400, S, 'of', f, eyes='open', mouth='smile', look=(1, 0.0) if t < 0.55 else (0.5, -1), lh=lerp2((-98, 40), (-70, -150), sal), rh=rh,
              bob=math.sin(g * 3) * 2)
    hand = (ox + rh[0] * S, 1400 + (rh[1] - 175) * S)
    took = t >= 0.42
    hop = 24 * abs(math.sin(seg(t, 0.6, 1.5) * math.pi * 2)) if t > 0.6 else 0
    gv = 1 - ease(seg(t, 0.5, 0.8))
    arms = ((lerp(-70, -168, gv), lerp(-110, -150, gv)), None) if gv > 0.02 else ((-128, -222), (128, -222))
    ghost(c, GX, GY_ - hop, GS, 'gh', f, g, eyes='big' if t < 0.6 else 'closed', look=(-1, 0), rot=0.04 * math.sin(g * 5), arms=arms)
    gp = (GX - 168 * GS - 22, GY_ - 150 * GS - 22)
    if not took: pp = lerp2(gp, (hand[0] + 16, hand[1] - 20), ease(seg(t, 0.3, 0.42))); pr = -0.5
    else: pp = (hand[0] + 16, hand[1] - 34); pr = -0.5 + 0.6 * ease(seg(t, 0.55, 0.95))
    peg(c, pp[0], pp[1], 1.5, pr)
    if 0.9 < t < 1.5:
        qq = seg(t, 0.9, 1.5)
        rays(c, pp[0], pp[1], 56 + 30 * qq, 80 + 46 * qq, 8, GOLD, 1 - qq, f, 'fr')
    for i in range(2):
        hq = seg(t, 0.7 + i * 0.25, 1.7 + i * 0.25)
        if 0 < hq < 1: heart(c, GX - 10 + i * 70, GY_ - 280 - 80 * hq, 0.7 + 0.15 * i, CORAL, 1 - ein(hq))
    c.restore()


def drive(c, t, f, g):
    c.rectangle(0, 0, W, H); rgb(c, NAVY); c.fill()
    c.save(); c.translate(500, 1320); c.scale(1.18, 1.18); c.translate(-500, -1320); c.translate(0, 120)
    country(c, f, g, 1250)
    sp = 520; off = sp * (t + 3.0)
    for i, tk in enumerate((-0.35, 0.85, 1.9)):
        bush(c, -160 + (t - tk) * sp, 1250, 1.5 - 0.3 * (i % 2))
    road2(c, 1300, off)
    by = 963 + math.sin(g * 11) * 3; bx = 150
    R0 = 1.2
    bus_ext(c, f, g, bx, by, 0.8, door=0.0, rot=-off / 34.0, otto=('open', 'smile') if t < R0 + 0.2 else ('wide', 'o'), look=(-1, -0.3) if t < R0 + 0.2 else (0.6, -1))
    gxw = bx + 0.8 * 250
    if t < R0 + 0.12:
        c.save(); c.rectangle(bx + 0.8 * 194, by + 0.8 * 64, 0.8 * 112, 0.8 * 142); c.clip()
        ghost(c, gxw, by + 0.8 * 232 - 240 * ein(seg(t, R0 - 0.05, R0 + 0.12)), 0.42, 'gw', f, g, eyes='open', look=(-1, -0.2))
        c.restore()
    if t >= R0:
        k = eback(seg(t, R0, R0 + 0.35)); wv = math.sin(g * 14)
        c.save(); c.rectangle(-200, -400, W + 400, by + 404); c.clip()
        ghost(c, gxw - 16, by + 204 - 136 * k, 0.8, 'gr', f, g, eyes='closed', rot=0.17 + 0.05 * wv, arms=((-118, -236 + 12 * wv), (122, -240 - 12 * wv)))
        c.restore()
        for i in range(3):
            yy = by - 128 + i * 32 + 5 * math.sin(g * 9 + i)
            wline(c, [(gxw + 92 + (i % 2) * 22, yy), (gxw + 158 + (i % 2) * 34, yy)], ('wl', i), f, lw=6, col=WHITE, amp=1.0, a=0.6)
        q = t - R0
        if q < 0.35: rays(c, gxw - 16, by + 4, 40 + 110 * q, 66 + 150 * q, 7, WHITE, 1 - q / 0.35, f, 'rf', a0=-math.pi * 0.95, span=math.pi * 0.9)
    reflect(c, g, bx + 20, bx + 640, 1396, n=4, depth=60)
    rain(c, g, 0.2)
    c.restore()
    house_card(c, 846, 720, eback(seg(t, 0.3, 0.6)) * 0.58, f, rot=0.06 + 0.02 * math.sin(g * 2))


def scD(c, t, f, g):
    if t < CUT:
        fare(c, t, f, g)
        cap2(c, t, 0.15, ["Fare: one clothes peg."], y=240, size=86, gold=True, t1=CUT - 0.02)
    else:
        lt = t - CUT
        drive(c, lt, f, g)
        cap2(c, t, CUT + 0.12, ["Stop requested:"], y=240, size=80)
        cap2(c, t, CUT + 0.7, ["the house with the washing line."], y=338, size=68, gold=True)
        fa = 1 - seg(lt, 0, 0.15)
        if fa > 0:
            c.rectangle(0, 0, W, H); rgb(c, NAVY, fa); c.fill()


# ------------------------------------------------------------------ scene E 16.8-21.2: home, and washing day
GY5 = 1390; HX = 700; LA, LB, LY = 318, 566, 1062; SX5 = 446


def old_house(c, f, g, x, base, door=0.0, kids=(0, 0), chim=0.0):
    gl = cairo.RadialGradient(x + 88, base - 110, 20, x + 88, base - 110, 320)
    gl.add_color_stop_rgba(0, 1, 0.85, 0.5, 0.16 + 0.3 * door); gl.add_color_stop_rgba(1, 1, 0.85, 0.5, 0)
    c.set_source(gl); c.rectangle(x - 300, base - 440, 720, 460); c.fill()
    if chim > 0.01:
        wv = math.sin(g * 10)
        ghost(c, x + 112, base - 752 + 150 * (1 - chim), 0.36, 'chg', f, g, own=True, eyes='open', arms=((-126, -214 + 22 * wv), None))
    c.save(); c.translate(x + 112, base - 640); c.rotate(0.07)
    rrect(c, -32, -112, 64, 160, 6); fs(c, HOUSED, 8); rrect(c, -42, -126, 84, 28, 6); fs(c, ROOFC, 7); c.restore()
    wpoly(c, [(x - 190, base + 6), (x - 190, base - 500), (x + 190, base - 500), (x + 190, base + 6)], 'ohb', f, 1.5); fs(c, HOUSEC, 9)
    for k in range(4):
        wline(c, [(x - 186, base - 110 - k * 100), (x + 186, base - 104 - k * 100)], ('ohp', k), f, lw=4, col=INK, amp=0.8, a=0.22)
    wpoly(c, [(x - 232, base - 492), (x - 14, base - 730), (x + 232, base - 492)], 'ohr', f, 1.5); fs(c, ROOFC, 9)
    c.new_path(); c.arc(x - 12, base - 588, 34, 0, 2 * math.pi); fs(c, hx('FFD98A'), 7)
    wline(c, [(x - 12, base - 622), (x - 12, base - 554)], 'oa1', f, lw=6, amp=0.4); wline(c, [(x - 46, base - 588), (x + 22, base - 588)], 'oa2', f, lw=6, amp=0.4)
    for i, wx in enumerate((x - 146, x + 46)):
        rrect(c, wx, base - 436, 100, 126, 12); fs(c, hx('FFE7A8'), 8)
        k = kids[i]
        if k > 0.01:
            c.save(); rrect(c, wx + 4, base - 432, 92, 118, 9); c.clip()
            wv = math.sin(g * 10 + i * 2)
            arms = (None, (118, -214 + 24 * wv)) if i == 0 else ((-118, -214 + 24 * wv), None)
            ghost(c, wx + 50, base - 306 + 110 * (1 - k), 0.4, ('kid', i), f, g, own=True, eyes='closed' if i else 'open', arms=arms)
            c.restore()
        rrect(c, wx - 9, base - 312, 118, 15, 6); fs(c, HOUSED, 6)
    dx = x + 40
    c.new_path(); c.move_to(dx, base + 4); c.line_to(dx, base - 150); c.arc(dx + 56, base - 150, 56, math.pi, 2 * math.pi); c.line_to(dx + 112, base + 4); c.close_path()
    fs(c, (lerp(0.36, 1.0, door), lerp(0.24, 0.86, door), lerp(0.3, 0.5, door)), 8)
    c.new_path(); c.arc(dx + 90, base - 96, 7, 0, 2 * math.pi); rgb(c, GOLD); c.fill()


def hung_sheet(c, f, g, x, top, w=156, h=226):
    pts = [(x - w / 2, top)]
    n = 6
    for i in range(1, n + 1):
        u = i / n; pts.append((x - w / 2 + 10 * math.sin(g * 4 + u * 3) * u, top + h * u))
    for i in range(n, -1, -1):
        u = i / n; pts.append((x + w / 2 + 14 * math.sin(g * 4 + 1 + u * 3) * u, top + h * u + (8 * math.sin(g * 5) if i == n else 0)))
    c.new_path(); c.move_to(*pts[0])
    for p in pts[1:]: c.line_to(*p)
    c.close_path(); fs(c, SHEET, 8)
    heart(c, x + 36, top + h - 64, 0.4, CORAL)
    wline(c, [(x - 30, top + 30), (x - 26 + 6 * math.sin(g * 4), top + h - 30)], 'hsf', f, lw=5, col=INK, amp=0.6, a=0.18)


def scE(c, t, f, g):
    SWAP, PEGS = 1.2, 1.62
    country(c, f, g, 1450)
    c.save(); c.translate(530, 1450); c.scale(1.3, 1.3); c.translate(-530, -GY5)
    door = ease(seg(t, 2.3, 2.8))
    old_house(c, f, g, HX, GY5, door=door, kids=(eback(seg(t, 2.5, 2.8)), eback(seg(t, 2.8, 3.1))), chim=eback(seg(t, 3.7, 3.95)))
    bus_ext(c, f, g, -440, 1010, 0.8, door=1.0, otto=None)
    reflect(c, g, -400, 250, 1396, n=3, depth=50)
    # the washing line
    for px in (LA, LB):
        wline(c, [(px, GY5 + 4), (px, LY - 34)], ('lp', px), f, lw=17, col=INK, amp=0.5); wline(c, [(px, GY5 + 4), (px, LY - 34)], ('lp2', px), f, lw=8, col=hx('8A6A4A'), amp=0.3)
    c.new_path(); c.move_to(LA, LY - 22); c.curve_to(LA + 80, LY + 6, LB - 80, LY + 6, LB, LY - 22); rgb(c, CREAMT); c.set_line_width(5); c.stroke()
    c.save(); c.translate(LA + 34, LY - 4); c.rotate(0.12 * math.sin(g * 4)); rrect(c, -12, 0, 24, 52, 9); fs(c, CORAL, 5); rrect(c, -12, 38, 40, 22, 9); fs(c, CORAL, 5); c.restore()
    S = 0.55; ox = 232
    own_alive = t >= SWAP
    if not own_alive:
        hung_sheet(c, f, g, SX5, LY)
        for sg in (-1, 1): peg(c, SX5 + sg * 54, LY + 2, 0.9, 0.0)
    # Otto
    catch = ease(seg(t, 1.15, 1.45)); held = t >= 1.75
    sal = ease(seg(t, 3.1, 3.4))
    if not held: rh = lerp2((98, 40), (128, -150), catch); lh = lerp2((-98, 40), (-40, -150), catch)
    else: rh = lerp2((128, -150), (104, -20), ease(seg(t, 1.75, 2.1))); lh = lerp2(lerp2((-40, -150), (-98, 40), ease(seg(t, 1.75, 2.1))), (-70, -150), sal)
    otto_full(c, ox, 1396, S, 'of', f, eyes='wide' if SWAP <= t < 2.2 else ('closed' if t > 3.6 else 'open'), mouth='o' if SWAP <= t < 2.2 else 'smile',
              look=(1, -0.5), lh=lh, rh=rh, bob=math.sin(g * 3) * 2)
    hand = (ox + rh[0] * S, 1396 + (rh[1] - 175) * S)
    # the ghost in Otto's cloth floats to the line
    if t < SWAP:
        p = ease(seg(t, 0.1, 0.8)); up = ein(seg(t, 0.85, SWAP))
        gx_ = lerp(352, SX5, p); gy_ = lerp(1352, 1338, p) - 46 * up - 10 * abs(math.sin(g * 6))
        ghost(c, gx_, gy_, 0.8, 'gh', f, g, eyes='big', look=(0.5, -1), rot=0.05 * math.sin(g * 5), arms=((-118, -226), (120, -230)) if t > 0.45 else None)
        if 0.3 < t < 1.0: txt(c, "!", gx_ + 96, gy_ - 190, 90, GOLD, SERIF)
    elif t < 1.75:
        p = seg(t, SWAP, 1.75); e = ease(p)
        cloth(c, lerp(SX5, hand[0] - 8, e), lerp(1226, hand[1] - 20, e) - 110 * math.sin(p * math.pi), lerp(150, 84, e), lerp(190, 58, e), -3.2 * e, f, 'back')
    else:
        cloth(c, hand[0] - 4, hand[1] + 6, 84, 58, 0.08, f, 'back')
    # its own sheet comes alive
    if own_alive:
        q = t - SWAP; qp = t - PEGS
        if qp < 0: gx_, gy_ = SX5, LY + 232; rot = 0.07 * math.sin(q * 30) * (1 - q / (PEGS - SWAP))
        else:
            e = eout(seg(t, PEGS, PEGS + 0.6))
            gx_ = lerp(SX5, 462, e) + 10 * math.sin(g * 2); gy_ = lerp(LY + 232, 1268, e) - 12 * math.sin(g * 3.2)
            rot = 0.5 * math.exp(-3.5 * qp) * math.sin(qp * 13)
        wv = math.sin(g * 10)
        if qp < 0: arms = None
        elif t < 2.6: arms = ((-124, -228), (126, -230))
        else: arms = ((-128, -214 + 22 * wv), None)
        ghost(c, gx_, gy_, 0.92 * lerp(0.9, 1.0, eback(seg(q, 0, 0.25))), 'own', f, g, own=True, eyes='big' if qp < 0.25 else ('closed' if (t < 2.6 or t > 3.5) else 'open'),
              look=(-0.6, 0.3), rot=rot, arms=arms, holes=eback(seg(q, 0.08, 0.26)))
        if qp < 0:
            for sg in (-1, 1): peg(c, SX5 + sg * 54, LY + 2, 0.9, 0.0)
        elif qp < 0.9:
            for sg in (-1, 1):
                peg(c, SX5 + sg * (54 + 150 * qp), LY + 2 - 330 * qp + 520 * qp * qp, 0.9, sg * qp * 9)
        if q < 0.3: rays(c, SX5, LY + 110, 110 + 130 * q, 140 + 190 * q, 9, WHITE, 1 - q / 0.3, f, 'sw5', lw=7)
        for i in range(3):
            hq = seg(t, 2.25 + i * 0.4, 3.5 + i * 0.4)
            if 0 < hq < 1: heart(c, gx_ - 40 + i * 50, gy_ - 270 - 110 * hq, 0.62 + 0.12 * i, CORAL, 1 - ein(hq))
    if 3.7 <= t < 4.05:
        qq = (t - 3.7) / 0.35
        rays(c, HX + 112, GY5 - 770, 30 + 50 * qq, 50 + 80 * qq, 6, GOLD, 1 - qq, f, 'chr', a0=-math.pi * 0.9, span=math.pi * 0.8)
    c.restore()
    rain(c, g, 0.16)
    cap2(c, t, 0.2, ["Home. And its own sheet!"], y=250, size=82, t1=1.95)
    cap2(c, t, 2.05, ["It was washing day."], y=250, size=88, gold=True)


# ------------------------------------------------------------------ scene F 21.2-25.6: the peg joins the collection
PEGP = (150, 972)


def scF(c, t, f, g):
    PIN, PERK = 1.4, 3.7
    zz = 1 + 0.045 * ease(seg(t, 0.0, 4.4))
    c.save(); c.translate(300, 860); c.scale(zz, zz); c.translate(-300, -860)
    perk = t >= PERK

    def head():
        if perk:
            otto_head(c, 150, 935 - 16 * math.sin(clamp((t - PERK) / 0.28) * math.pi), 98, 'oh', f, eyes='open', mouth='flat', look=(1.0, 0.25), tilt=0.05)
        elif t < 1.95: otto_head(c, 150, 935, 98, 'oh', f, eyes='open', mouth='smile', look=(-1.0, 0.1), tilt=-0.05)
        else: otto_head(c, 150 + math.sin(g * 4) * 5, 935, 98, 'oh', f, eyes='closed', mouth='smile', tilt=math.sin(g * 4) * 0.06)
    pin_b = (-8, 912)
    if t < 0.95: lhand = lerp2((64, 1060), pin_b, ease(seg(t, 0.05, 0.95)))
    elif t < PIN + 0.2: lhand = (pin_b[0] - 7 * math.sin(clamp((t - PIN + 0.12) / 0.3) * math.pi), pin_b[1])
    elif t < 2.1: lhand = lerp2(pin_b, (84, 1150), ease(seg(t, PIN + 0.2, 2.1)))
    else: lhand = None
    cabin(c, f, g, head, moving=1.0, lhand=lhand)
    pinned = t >= PIN
    collection(c, f, g, peg_at=PEGP if pinned else None)
    if not pinned:
        hs = cab(lhand); peg(c, hs[0] - 4, hs[1] - 46, 1.9, 0.1)
    else:
        q = t - PIN
        if q < 0.45: rays(c, PEGP[0], PEGP[1], 70 + 50 * q, 96 + 100 * q, 8, GOLD, 1 - q / 0.45, f, 'pin')
    for i, (sx, sy) in enumerate(((330, 742), (196, 560), (92, 790), (212, 800), PEGP)):
        ph = seg(t, 1.85 + i * 0.3, 2.5 + i * 0.3)
        if 0 < ph < 1: sparkle(c, sx + 36, sy - 40 - 14 * ph, 34 * math.sin(ph * math.pi), GOLD, 1)
    stop_lamp(c, LAMP[0], LAMP[1], False, f)
    if 1.95 <= t < PERK:
        for k in range(3):
            ph = (g * 0.6 + k / 3) % 1
            note(c, 596 + k * 46 + ph * 50, 1000 - ph * 150, 1.0, CREAMT, math.sin(ph * math.pi))
    mirror(c, f, 3 * math.sin(g * 2.2), 0)
    if t >= PERK - 0.5:                              # tiny notes drift in from the back of the bus
        for k in range(3):
            ph = seg(t, PERK - 0.5 + k * 0.22, PERK + 0.5 + k * 0.22)
            if 0 < ph < 1: note(c, 1000 - 200 * ph - k * 24, 905 - 60 * math.sin(ph * 3) + k * 44, 0.8, TEAL, math.sin(ph * math.pi))
    if perk: txt(c, "?", 640, 930, 96, CREAMT, SERIF)
    c.restore()
    cap2(c, t, 1.0, ["Every passenger gets home."], y=250, size=80, gold=True)


# ------------------------------------------------------------------ scene G 25.6-30: seat 7
def scG(c, t, f, g):
    S = 0.9
    OUT, BACK = 3.15, 3.5
    pan = 46 * ease(seg(t, 0.2, 2.0))
    c.save(); rcam(c, 0.0, pan)
    rear_set(c, f, g)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    lit = 0.0 if OUT <= t < BACK else 1.0
    fl = lit * (0.8 + 0.2 * math.sin(g * 13) * math.sin(g * 7.3))
    c.rectangle(-900, -900, 4000, 5000); rgb(c, DARK, 0.3); c.fill()
    gx_, gy_ = 756, 1366
    if fl > 0:
        gl = cairo.RadialGradient(gx_, gy_, 8, gx_, gy_, 210)
        gl.add_color_stop_rgba(0, 1, 0.86, 0.45, 0.75 * fl); gl.add_color_stop_rgba(0.45, 1, 0.8, 0.4, 0.3 * fl); gl.add_color_stop_rgba(1, 1, 0.8, 0.4, 0)
        c.set_source(gl); c.rectangle(gx_ - 240, gy_ - 240, 480, 480); c.fill()
        c.save(); c.translate(gx_, 1398); c.scale(1, 0.16); c.new_path(); c.arc(0, 0, 96, 0, 2 * math.pi); c.restore(); rgb(c, hx('FFE9A8'), 0.7 * fl); c.fill()
        sparkle(c, gx_, gy_ - 4, 15 + 5 * math.sin(g * 17), hx('FFF3C4'), 0.95 * fl)
    # Otto tiptoes over and bends down
    walking = t < 0.9
    ox = lerp(250, 372, ease(seg(t, 0.0, 0.9)))
    bend = 0.82 * ease(seg(t, 0.95, 1.6))
    qb = t - BACK
    jump = 26 * math.sin(clamp(qb / 0.3) * math.pi) if qb > 0 else 0
    kw = dict(eyes='wide', mouth='flat' if t < 1.6 else 'o', look=(1, 0.2) if t < 0.95 else (1, 0.9), lh=(-98, 40) if t < 0.95 else (-116, -30),
              rh=(98, 40) if t < 0.95 else (124, -20), bob=abs(math.sin(g * 9)) * 6 if walking else 0)
    fy_ = 1400 - jump
    c.save(); c.rectangle(ox - 300, fy_ - 74 * S, 600, 200); c.clip(); otto_full(c, ox, fy_, S, 'of', f, **kw); c.restore()      # the legs stay upright
    c.save(); c.translate(ox, fy_ - 95 * S); c.rotate(bend); c.rectangle(-600, -900, 1200, 900 + 31 * S); c.clip()             # the rest bends at the hip
    otto_full(c, 0, 95 * S, S, 'of', f, **kw)
    if t >= 1.5: drops(c, -96, -300 * S + 30, g)
    c.restore()
    # the notes
    burst = eback(seg(t, BACK, BACK + 0.25)) if t >= BACK else 0
    for k in range(6):
        ph = (t * 0.5 + k / 6) % 1
        born = t - ph / 0.5
        if born < 0.15 or OUT - 0.02 <= born < BACK: continue
        xx = 668 + (k * 37) % 150 + 26 * math.sin(ph * 7 + k * 1.7); yy = 1322 - 330 * ph
        note(c, xx, yy, (0.5 + 0.45 * ph) * (1 + 0.25 * burst), (GOLD, CREAMT, TEAL)[k % 3], math.sin(ph * math.pi) ** 0.6)
    if 0 <= qb < 0.4: rays(c, gx_, gy_, 60 + 150 * qb, 96 + 230 * qb, 9, GOLD, 1 - qb / 0.4, f, 'bk7', lw=6, a0=-math.pi, span=math.pi)
    c.restore()
    gl = cairo.LinearGradient(0, 0, 0, 560)            # the lights dim: a calm dark band behind the two captions
    gl.add_color_stop_rgba(0, NAVY[0], NAVY[1], NAVY[2], 0.96); gl.add_color_stop_rgba(0.72, NAVY[0], NAVY[1], NAVY[2], 0.9)
    gl.add_color_stop_rgba(1, NAVY[0], NAVY[1], NAVY[2], 0)
    c.new_path(); c.set_source(gl); c.paint_with_alpha(ease(seg(t, 0.0, 0.9)))
    cap2(c, t, 1.25, ["Who is playing under seat 7?"], y=250, size=78, gold=True)
    cap2(c, t, 2.0, ["Mice, crickets or a moth?"], y=362, size=74)


SCENES = [(0.0, 3.6, scA), (3.6, 8.0, scB), (8.0, 12.4, scC), (12.4, 16.8, scD), (16.8, 21.2, scE), (21.2, 25.6, scF), (25.6, 30.0, scG)]


def draw(c, g, f):
    for i, (a, b, fn) in enumerate(SCENES):
        if a <= g < b or (i == len(SCENES) - 1 and g >= b):
            c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, g - a, f, g); c.restore()
            fa = 1 - seg(g - a, 0, 0.18)
            if i > 0 and fa > 0 and fn is not scD:
                c.rectangle(0, 0, W, H); rgb(c, NAVY, fa); c.fill()
            return
