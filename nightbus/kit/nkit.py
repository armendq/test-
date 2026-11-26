from ep5 import *

SNOWW = hx('F4F7FF'); SHADE = hx('C9D6F2'); STRAW = hx('E8C98A'); COAT = hx('C4673A'); HAT = hx('7A4B2A'); CARROT = hx('FF8A3D'); SIL = hx('0A0E22')


def band(c, a=1.0, h=480):
    gl = cairo.LinearGradient(0, 0, 0, h)
    gl.add_color_stop_rgba(0, NAVY[0], NAVY[1], NAVY[2], 0.96 * a); gl.add_color_stop_rgba(0.62, NAVY[0], NAVY[1], NAVY[2], 0.84 * a)
    gl.add_color_stop_rgba(1, NAVY[0], NAVY[1], NAVY[2], 0)
    c.set_source(gl); c.rectangle(0, 0, W, h); c.fill()


def make_draw(SCENES):
    def draw(c, g, f):
        for i, (a, b, fn) in enumerate(SCENES):
            if a <= g < b or (i == len(SCENES) - 1 and g >= b):
                c.save(); c.rectangle(0, 0, W, H); c.clip(); fn(c, g - a, f, g); c.restore()
                fa = 1 - seg(g - a, 0, 0.18)
                if i > 0 and fa > 0:
                    c.rectangle(0, 0, W, H); rgb(c, NAVY, fa); c.fill()
                return
    return draw


def pface(c, x, y, sp, mood, look=(0, 0), r=11, col=None):
    col = col or EYE; ex, ey = 7 * look[0], 5 * look[1]
    c.set_line_cap(RND)
    for sg in (-1, 1):
        if mood == 'joy':
            c.new_path(); c.arc(x + sg * sp + ex, y + ey + 5, r, math.pi * 1.1, math.pi * 1.9); rgb(c, col); c.set_line_width(6); c.stroke()
        else:
            c.new_path(); c.arc(x + sg * sp + ex, y + ey, r * (1.25 if mood == 'o' else 1), 0, 2 * math.pi); rgb(c, col); c.fill()
            c.new_path(); c.arc(x + sg * sp + ex + 3, y + ey - 4, r * 0.35, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
    my = y + r * 2.6
    if mood in ('happy', 'joy'):
        c.new_path(); c.arc(x + ex * 0.5, my - 8, 16, 0.15 * math.pi, 0.85 * math.pi); rgb(c, col); c.set_line_width(6); c.stroke()
    elif mood == 'sad':
        c.new_path(); c.arc(x + ex * 0.5, my + 14, 14, 1.15 * math.pi, 1.85 * math.pi); rgb(c, col); c.set_line_width(6); c.stroke()
    else:
        c.new_path(); c.arc(x + ex * 0.5, my + 2, 9, 0, 2 * math.pi); rgb(c, col); c.fill()
    for sg in (-1, 1):
        c.new_path(); c.arc(x + sg * (sp + 20), y + r * 1.9, 12, 0, 2 * math.pi); rgb(c, PINK, 0.5); c.fill()


CB = ((-78, -58, 56), (-22, -106, 72), (54, -88, 60), (94, -48, 44), (8, -50, 66), (-44, -42, 52))


def cloudp(c, x, y, s, key, f, g, mood='happy', look=(0, 0), rot=0.0, sq=1.0, **kw):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    for (ax, ay, r) in CB:
        c.new_path(); c.arc(ax, ay, r + 8, 0, 2 * math.pi); rgb(c, INK); c.fill()
    for (ax, ay, r) in CB:
        c.new_path(); c.arc(ax, ay, r, 0, 2 * math.pi); rgb(c, SNOWW); c.fill()
    c.new_path(); c.arc(8, -44, 58, 0.25, math.pi - 0.25); rgb(c, SHADE, 0.7); c.set_line_width(9); c.stroke()
    pface(c, 4, -86, 34, mood, look)
    c.restore()
    if mood == 'sad':
        drops(c, x - 70 * s, y - 10 * s, g); drops(c, x + 44 * s, y - 6 * s, g + 0.4)


def scarep(c, x, y, s, key, f, g, mood='happy', look=(0, 0), rot=0.0, sil=False, **kw):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    col = (lambda v: SIL) if sil else (lambda v: v)
    ink = SIL if sil else INK
    wline(c, [(0, 0), (0, -150)], (key, 'p'), f, lw=18, col=ink, amp=0.4)
    if not sil: wline(c, [(0, -2), (0, -150)], (key, 'p2'), f, lw=9, col=hx('8A6A4A'), amp=0.3)
    wline(c, [(-150, -196), (150, -196)], (key, 'a'), f, lw=18, col=ink, amp=0.4)
    for sg in (-1, 1):
        for a in (-0.6, 0, 0.6):
            wline(c, [(sg * 150, -196), (sg * (150 + 36 * math.cos(a)), -196 + 36 * math.sin(a))], (key, 'h', sg, a), f, lw=7, col=col(STRAW), amp=0.6)
    rrect(c, -64, -236, 128, 150, 22); fs(c, col(COAT), 8, ink)
    if not sil:
        c.rectangle(-46, -150, 34, 34); rgb(c, GOLD); c.fill(); c.rectangle(-46, -150, 34, 34); rgb(c, INK); c.set_line_width(4); c.stroke()
        for i in range(2):
            c.new_path(); c.arc(24, -200 + i * 44, 9, 0, 2 * math.pi); fs(c, hx('7A3F22'), 4)
    c.new_path(); c.arc(0, -290, 60, 0, 2 * math.pi); fs(c, col(STRAW), 8, ink)
    if not sil:
        pface(c, 0, -300, 24, mood, look, r=10, col=hx('3A2A1A'))
    elif sil == 'eyes':
        for sg in (-1, 1):
            c.new_path(); c.arc(sg * 24, -298, 9, 0, 2 * math.pi); rgb(c, WHITE); c.fill()
    wline(c, [(-92, -334), (92, -334)], (key, 'br'), f, lw=22, col=ink, amp=0.4)
    c.new_path(); c.move_to(-54, -338); c.line_to(-6, -424); c.line_to(22, -406); c.line_to(54, -338); c.close_path(); fs(c, col(HAT), 8, ink)
    if not sil: wline(c, [(-88, -334), (88, -334)], (key, 'br2'), f, lw=11, col=HAT, amp=0.3)
    c.restore()


def snowp(c, x, y, s, key, f, g, mood='happy', look=(0, 0), rot=0.0, sq=1.0, melt=0.0, **kw):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s * sq)
    for sg in (-1, 1):
        wline(c, [(sg * 70, -120), (sg * 134, -176 - (30 if mood == 'joy' else 0))], (key, 'tw', sg), f, lw=9, col=hx('6B4A2E'), amp=0.6)
    wcirc(c, 0, -88, 90, (key, 'b'), f, amp=1.2); fs(c, SNOWW, 8)
    wcirc(c, 0, -216, 62, (key, 'h'), f, amp=1.0); fs(c, SNOWW, 8)
    rrect(c, -60, -174, 120, 26, 12); fs(c, CORAL, 6); rrect(c, 26, -166, 26, 70, 10); fs(c, CORAL, 6)
    for i in range(2):
        c.new_path(); c.arc(-8, -106 + i * 44, 8, 0, 2 * math.pi); rgb(c, EYE); c.fill()
    pface(c, 0, -232, 24, mood, look, r=9)
    lx = 1 if look[0] > 0 else -1
    c.new_path(); c.move_to(0, -222); c.line_to(lx * 48, -212); c.line_to(0, -204); c.close_path(); fs(c, CARROT, 4)
    c.restore()
    if melt > 0:
        drops(c, x - 84 * s, y - 120 * s, g); drops(c, x + 60 * s, y - 60 * s, g + 0.5)


def jar(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    rrect(c, -20, -26, 40, 52, 10); rgb(c, hx('CFE8FF'), 0.6); c.fill_preserve(); rgb(c, INK); c.set_line_width(5); c.stroke()
    rrect(c, -16, -37, 32, 13, 4); fs(c, hx('B98552'), 4)
    c.new_path(); c.move_to(0, -12); c.curve_to(14, 6, 10, 18, 0, 18); c.curve_to(-10, 18, -14, 6, 0, -12); rgb(c, hx('5FB8FF')); c.fill()
    c.restore()


def button(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s)
    c.new_path(); c.arc(0, 0, 22, 0, 2 * math.pi); fs(c, COAT, 5)
    c.new_path(); c.arc(0, 0, 14, 0, 2 * math.pi); rgb(c, INK, 0.25); c.set_line_width(3); c.stroke()
    for dx, dy in ((-6, -6), (6, -6), (-6, 6), (6, 6)):
        c.new_path(); c.arc(dx, dy, 3.2, 0, 2 * math.pi); rgb(c, INK); c.fill()
    c.restore()


def flake(c, x, y, s, rot=0.0):
    c.save(); c.translate(x, y); c.rotate(rot); c.scale(s, s); c.set_line_cap(RND)
    for (lw, col) in ((10, INK), (5, hx('CFEFFF'))):
        for i in range(3):
            a = i * math.pi / 3
            c.new_path(); c.move_to(-26 * math.cos(a), -26 * math.sin(a)); c.line_to(26 * math.cos(a), 26 * math.sin(a)); rgb(c, col); c.set_line_width(lw); c.stroke()
    c.restore()


def note6(c, x, y, s, rot=0.0): note(c, x - 12 * s, y + 22 * s, 1.25 * s, GOLD)


SOUV = {6: note6, 7: jar, 8: button, 9: flake}
POS = {6: (64, 690), 7: (342, 606), 8: (56, 566), 9: (268, 912)}


def collection2(c, f, g, n):
    collection(c, f, g, peg_at=PEGP)
    for k in range(6, n + 1):
        x, y = POS[k]
        SOUV[k](c, x, y + 3 * math.sin(g * 3 + k), 1.5, 0.08 * math.sin(g * 3 + k))
        c.new_path(); c.arc(x, y - 46, 8, 0, 2 * math.pi); fs(c, CORAL, 4)


def pin_scene(c, t, f, g, n, line="Every passenger gets home."):
    PIN, PERK = 1.4, 3.7
    zz = 1 + 0.045 * ease(seg(t, 0.0, 4.4))
    c.save(); c.translate(300, 860); c.scale(zz, zz); c.translate(-300, -860)
    perk = t >= PERK

    def head():
        if perk: otto_head(c, 150, 935 - 16 * math.sin(clamp((t - PERK) / 0.28) * math.pi), 98, 'oh', f, eyes='open', mouth='flat', look=(1.0, 0.25), tilt=0.05)
        elif t < 1.95: otto_head(c, 150, 935, 98, 'oh', f, eyes='open', mouth='smile', look=(-1.0, -0.4), tilt=-0.05)
        else: otto_head(c, 150 + math.sin(g * 4) * 5, 935, 98, 'oh', f, eyes='closed', mouth='smile', tilt=math.sin(g * 4) * 0.06)
    up = (20, 985)
    if t < 0.5: lhand = lerp2((64, 1060), up, ease(seg(t, 0.05, 0.5)))
    elif t < 0.75: lhand = up
    elif t < 1.5: lhand = lerp2(up, (84, 1150), ease(seg(t, 0.75, 1.5)))
    else: lhand = None
    cabin(c, f, g, head, moving=1.0, lhand=lhand)
    pinned = t >= PIN
    collection2(c, f, g, n if pinned else n - 1)
    if not pinned:
        hs = cab(lhand if t < 0.6 else up); p = ease(seg(t, 0.6, PIN))
        x, y = lerp2((hs[0] - 4, hs[1] - 46), POS[n], p); y -= 190 * math.sin(p * math.pi)
        SOUV[n](c, x, y, 1.5, p * 6.28)
    else:
        q = t - PIN
        if q < 0.45: rays(c, POS[n][0], POS[n][1], 60 + 50 * q, 86 + 100 * q, 8, GOLD, 1 - q / 0.45, f, 'pin')
    pts = [(330, 742), (196, 560), (92, 790), (212, 800), PEGP] + [POS[k] for k in range(6, n + 1)]
    for i, (sx, sy) in enumerate(pts):
        ph = seg(t, 1.85 + i * 0.2, 2.5 + i * 0.2)
        if 0 < ph < 1: sparkle(c, sx + 36, sy - 40 - 14 * ph, 34 * math.sin(ph * math.pi), GOLD, 1)
    stop_lamp(c, LAMP[0], LAMP[1], False, f)
    if 1.95 <= t < PERK:
        for k in range(3):
            ph = (g * 0.6 + k / 3) % 1
            note(c, 596 + k * 46 + ph * 50, 1000 - ph * 150, 1.0, CREAMT, math.sin(ph * math.pi))
    mirror(c, f, 3 * math.sin(g * 2.2), 0)
    if perk: txt(c, "?", 640, 930, 96, CREAMT, SERIF)
    c.restore()
    cap2(c, t, 1.0, [line], y=250, size=80, gold=True)


def badge3(c):
    c.new_path(); c.arc(832, 1062, 25, 0, 2 * math.pi); fs(c, GOLD, 6); txt(c, "3", 832, 1076, 38, INK, SANS)


def fare_scene(c, t, f, g, P, item, line1, line2, ps=0.9, seat3=False, size1=80, pkw=None):
    S = 0.9; ox = 400; T0 = 2.1; q = t - T0
    c.save(); rcam(c, 1.0)
    rear_set(c, f, g)
    if seat3: badge3(c)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    if q < 0.3: rh = lerp2((98, 40), (176, -64), ease(seg(q, -0.3, 0.3)))
    elif q < 0.55: rh = (176, -64)
    else: rh = lerp2((176, -64), (60, -300), ease(seg(q, 0.55, 0.95)))
    sal = ease(seg(q, 1.1, 1.35))
    otto_full(c, ox, 1400, S, 'of', f, eyes='open', mouth='smile', look=(1, 0.0) if q < 0.55 else (0.5, -1), lh=lerp2((-98, 40), (-70, -150), sal), rh=rh, bob=math.sin(g * 3) * 2)
    hand = (ox + rh[0] * S, 1400 + (rh[1] - 175) * S)
    hop = 24 * abs(math.sin(seg(t, 0.3, 1.2) * math.pi * 2)) if 0.3 < t < 1.2 else (20 * abs(math.sin(seg(q, 0.6, 1.5) * math.pi * 2)) if q > 0.6 else 0)
    P(c, GX, GY_ - hop, ps, 'ps', f, g, mood='joy' if (0.3 < t < 1.2 or q > 0.6) else 'happy', look=(-1, 0), rot=0.04 * math.sin(g * 5), **(pkw or {}))
    gp = (GX - 150, GY_ - 150)
    ik = eback(seg(t, 1.5, 1.8))
    if ik > 0.01:
        took = q >= 0.42
        if not took: pp = lerp2(gp, (hand[0] + 16, hand[1] - 20), ease(seg(q, 0.3, 0.42))); pr = 0.0
        else: pp = (hand[0] + 16, hand[1] - 40); pr = 0.3 * ease(seg(q, 0.55, 0.95))
        item(c, pp[0], pp[1], 1.7 * ik, pr)
        if 0.9 < q < 1.5:
            qq = seg(q, 0.9, 1.5); rays(c, pp[0], pp[1], 56 + 30 * qq, 80 + 46 * qq, 8, GOLD, 1 - qq, f, 'fr')
    for i in range(2):
        hq = seg(q, 0.7 + i * 0.25, 1.7 + i * 0.25)
        if 0 < hq < 1: heart(c, GX - 10 + i * 70, GY_ - 300 - 80 * hq, 0.7 + 0.15 * i, CORAL, 1 - ein(hq))
    c.restore()
    cap2(c, t, 0.15, [line1], y=240, size=size1, t1=T0 - 0.2)
    cap2(c, t, T0 - 0.1, [line2], y=240, size=86, gold=True)


def card(c, x, y, k, f, pic, rot=0.0):
    if k <= 0.01: return
    c.save(); c.translate(x, y); c.scale(k, k); c.rotate(rot)
    rrect(c, -192, -142, 400, 300, 16); rgb(c, INK, 0.3); c.fill()
    rrect(c, -200, -150, 400, 300, 16); fs(c, PAPER, 8)
    c.save(); rrect(c, -182, -132, 364, 264, 10); c.clip(); pic(c); c.restore()
    c.new_path(); c.arc(0, -150, 12, 0, 2 * math.pi); fs(c, TEAL, 5)
    c.restore()


def road_base(c, t, f, g, P=None, ps=0.42, otto=('open', 'smile'), look=(-1, -0.3), lift=0.0, pkw=None, pdy=0):
    c.rectangle(0, 0, W, H); rgb(c, NAVY); c.fill()
    c.save(); c.translate(500, 1320); c.scale(1.18, 1.18); c.translate(-500, -1320); c.translate(0, 120)
    country(c, f, g, 1250)
    sp = 520; off = sp * (t + 3.0)
    for i, tk in enumerate((-0.35, 0.85, 1.9, 3.1)):
        bush(c, -160 + (t - tk) * sp, 1250, 1.5 - 0.3 * (i % 2))
    road2(c, 1300, off)
    by = 963 + math.sin(g * 11) * 3; bx = 150
    c.save(); c.translate(bx + 600, by + 380); c.rotate(lift); c.translate(-(bx + 600), -(by + 380))
    bus_ext(c, f, g, bx, by, 0.8, door=0.0, rot=-off / 34.0, otto=otto, look=look)
    if P:
        gxw = bx + 0.8 * 250
        c.save(); c.rectangle(bx + 0.8 * 194, by + 0.8 * 64, 0.8 * 112, 0.8 * 142); c.clip()
        P(c, gxw, by + 0.8 * 236 + pdy, ps, 'pw', f, g, mood='happy', look=(-1, -0.2), **(pkw or {})); c.restore()
    c.restore()
    reflect(c, g, bx + 20, bx + 640, 1396, n=4, depth=60)
    rain(c, g, 0.2)
    c.restore()
    return bx, by


def road_scene(c, t, f, g, P, pic, place, ps=0.42, size2=68, pkw=None, pdy=0):
    road_base(c, t, f, g, P, ps, pkw=pkw, pdy=pdy)
    card(c, 846, 720, eback(seg(t, 0.5, 0.8)) * 0.58, f, pic, rot=0.06 + 0.02 * math.sin(g * 2))
    cap2(c, t, 0.2, ["Stop requested:"], y=240, size=80)
    cap2(c, t, 0.8, [place], y=338, size=size2, gold=True)


def ext_begin(c, f, g, z=1.0, fx=540, fy=960):
    c.rectangle(0, 0, W, H); rgb(c, NAVY); c.fill()
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)
    country(c, f, g, 1450)
    c.save(); c.translate(530, 1450); c.scale(1.3, 1.3); c.translate(-530, -GY5)


def ext_end(c, g, ra=0.16):
    c.restore(); rain(c, g, ra); c.restore()


def scr(x, y): return 530 + 1.3 * (x - 530), 1450 + 1.3 * (y - GY5)


def otto_home(c, f, g, t, wave_t=3.1, eyes='open', mouth='smile', look=(1, -0.5), x=232):
    sal = ease(seg(t, wave_t, wave_t + 0.3))
    otto_full(c, x, 1396, 0.55, 'of', f, eyes=eyes, mouth=mouth, look=look, lh=lerp2((-98, 40), (-70, -150), sal), rh=(98, 40), bob=math.sin(g * 3) * 2)


def stopped_bus(c, f, g, otto=('wide', 'o'), door=0.0, look=(-1, 0.3), cone=True):
    """the bus stands on the right and faces left; its lights fall on the road"""
    road2(c, 1336, 0)
    if cone:
        c.new_path(); c.move_to(644, 1262); c.line_to(120, 1170); c.line_to(120, 1428); c.line_to(644, 1332); c.close_path(); rgb(c, hx('FFE9A8'), 0.17); c.fill()
    bus_ext(c, f, g, 640, 1010 + math.sin(g * 11) * 1.5, 0.8, door=door, otto=otto, look=look)


def field_scene(c, t, f, g, tease=True):
    FL = 1.9 if tease else 1.75
    if tease: z, fx, fy = 1.0, 540, 960
    else:
        k = ease(seg(t, 0.6, 1.3)); z = lerp(1.55, 1.0, k); sx, sy = scr(330, 1120)
        fx, fy = lerp(sx + 90, 540, k), lerp(sy - 40, 960, k)
    ext_begin(c, f, g, z, fx, fy)
    fl = t - FL
    flash = (1 - fl / 0.18) if 0 <= fl < 0.18 else ((1 - (fl - 0.3) / 0.25) * 0.7 if 0.3 <= fl < 0.55 else 0)
    c.save(); c.translate(330, 1300); c.scale(1, 0.3); c.new_path(); c.arc(0, 0, 330, math.pi, 2 * math.pi); c.restore(); rgb(c, hx('1D3A2E')); c.fill()
    scarep(c, 330, 1336, 0.8, 'fig', f, g, sil=True if (flash <= 0 and t < FL + 0.6) else 'eyes', rot=0.02 * math.sin(g * 2))
    for i in range(5):
        px = 130 + i * 112
        wline(c, [(px, 1340), (px, 1262)], ('fp', i), f, lw=12, col=hx('2B2F55'), amp=0.5)
    wline(c, [(110, 1290), (610, 1290)], 'fr', f, lw=9, col=hx('2B2F55'), amp=0.5)
    stopped_bus(c, f, g)
    if flash > 0:
        c.rectangle(-900, -900, 4000, 5000); rgb(c, WHITE, 0.45 * flash); c.fill()
        wline(c, [(560, 380), (500, 560), (570, 600), (490, 800)], 'bolt', f, lw=12, col=WHITE, amp=2, a=flash)
    ext_end(c, g, 0.3)
    if tease:
        band(c, ease(seg(t, 0.0, 0.9)), 560)
        cap2(c, t, 1.25, ["Who is standing in the field?"], y=250, size=76, gold=True)
        cap2(c, t, 2.0, ["Scarecrow, statue or wizard?"], y=362, size=70)
    else:
        band(c, 1 - ease(seg(t, 0.6, 1.3)))
        cap2(c, t, -1, ["Someone is standing in the field."], y=250, size=72, gold=True, t1=2.2)
        cap2(c, t, 2.3, ["It does not move."], y=250, size=86)


def melt_scene(c, t, f, g, tease=True):
    S = 0.9
    if tease: z, fx, fy = 1.0, 540, 960
    else:
        k = ease(seg(t, 0.6, 1.3)); z = lerp(1.5, 1.0, k); fx, fy = lerp(620, 540, k), lerp(1250, 960, k)
    c.save(); c.translate(W / 2, H / 2); c.scale(z, z); c.translate(-fx, -fy)
    c.rectangle(-400, -400, W + 800, H + 800); rgb(c, NAVY); c.fill()
    c.save(); rcam(c, 0.0, 46 * ease(seg(t, 0.2, 2.0)) if tease else 46)
    rear_set(c, f, g); badge3(c)
    strap(c, 470, 566, 0.03 * math.sin(g * 2), f)
    c.rectangle(-900, -900, 4000, 5000); rgb(c, DARK, 0.34); c.fill()
    c.rectangle(-900, -900, 4000, 5000); rgb(c, hx('6FB7FF'), 0.07); c.fill()
    pk = 0.5 + 0.5 * seg(t, 0.0, 4.0) if tease else 0.6 + 0.4 * seg(t, 0, 3.6)
    c.save(); c.translate(752, 1404); c.scale(1, 0.2); c.new_path(); c.arc(0, 0, 150 * pk, 0, 2 * math.pi); c.restore(); rgb(c, hx('BFE4FF'), 0.85); c.fill()
    for i in range(3):
        ph = (g * 1.1 + i / 3) % 1
        c.new_path(); c.arc(690 + i * 54, 1312 + 84 * ph * ph, 8 - 3 * ph, 0, 2 * math.pi); rgb(c, hx('BFE4FF'), 0.95); c.fill()
    rrect(c, 664, 1010, 150, 206, 30); rgb(c, hx('0A0F24'), 0.82); c.fill()
    bl = (g * 0.45) % 1
    if bl > 0.08:
        for sg in (-1, 1):
            c.new_path(); c.arc(740 + sg * 22, 1080, 8, 0, 2 * math.pi); rgb(c, WHITE, 0.9); c.fill()
    for i in range(3):
        ph = (g * 0.5 + i / 3) % 1
        wcirc(c, 640 - 70 * ph, 1100 - 40 * ph, 14 + 26 * ph, ('br', i), f, amp=2); rgb(c, WHITE, 0.35 * (1 - ph)); c.fill()
    ox = lerp(230, 372, ease(seg(t, 0.0, 0.9))) if tease else 372
    jit = math.sin(g * 46) * 2.5
    otto_full(c, ox + jit, 1400, S, 'of', f, eyes='wide', mouth='flat' if t < 1.6 else 'o', look=(1, 0.5), lh=(-60, -110), rh=(60, -110), bob=abs(math.sin(g * 9)) * 6 if (tease and t < 0.9) else 0)
    txt(c, "brrr", ox - 40, 1400 - 392 * S - 30, 54, CREAMT, SERIF)
    c.restore(); c.restore()
    if tease:
        band(c, ease(seg(t, 0.0, 0.9)), 560)
        cap2(c, t, 1.25, ["Who is melting in seat 3?"], y=250, size=80, gold=True)
        cap2(c, t, 2.0, ["Snowman, ice cream or icicle?"], y=362, size=68)
    else:
        band(c, 1 - ease(seg(t, 0.6, 1.3)))
        cap2(c, t, -1, ["Who is melting in seat 3?"], y=250, size=82, gold=True, t1=2.2)
        cap2(c, t, 2.3, ["It is freezing back here."], y=250, size=82)
