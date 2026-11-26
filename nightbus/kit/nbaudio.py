import sys
L = open('/home/claude/studio/nightbus/ep05/audio.py').read().split('\n')
ib = [k for k, l in enumerate(L) if l.startswith('# ') and 'beds' in l][0]
ih = [k for k, l in enumerate(L) if l.startswith('# ') and 'sfx helpers' in l][0]
ia = [k for k, l in enumerate(L) if l.startswith('# ') and 'scene A' in l][0]
it = [k for k, l in enumerate(L) if l.startswith('x = buf[:NS]')][0]
HEAD = '\n'.join(L[:ib]); HELP = '\n'.join(L[ih:ia]); TAIL = '\n'.join(L[it:])
BODY = r'''
ts = np.arange(NS) / SR
def spans_env(spans, r=0.12):
    pts = [(0, 0)]
    for a, b in spans: pts += [(max(a - r, 0.001), 0), (a + r, 1), (b - r, 1), (min(b + r, 29.999), 0)]
    pts.append((30, 0)); return env_seg(pts)
e_in = spans_env(IN); e_out = 1 - e_in
rain_out = bnoise(DUR, 1800, 9500, 1) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.23 * ts))
rain_in = bnoise(DUR, 250, 2600, 2) * (0.8 + 0.2 * np.sin(2 * np.pi * 0.31 * ts + 1))
buf[:NS] += rain_out * e_out * 0.045 + rain_in * e_in * 0.06
g_eng = env_seg(ENG)
f_eng = 42 + 300 * g_eng
ph = 2 * np.pi * np.cumsum(f_eng) / SR
eng = (np.sin(ph) + 0.5 * np.sin(2 * ph) + 0.3 * np.sin(3 * ph) + 0.15 * np.sin(5 * ph)) * (1 + 0.25 * np.sin(2 * np.pi * 11 * ts))
buf[:NS] += eng * g_eng
beat = 0.75
CH = [(53, 57, 60, 64), (50, 53, 57, 60), (46, 50, 53, 57), (48, 52, 55, 58)]
MEL = [(0, 81), (1.5, 77), (2, 79), (3, 77), (4.5, 74), (5, 76), (6, 74), (7, 77), (7.5, 81), (8, 82), (9, 79), (10.5, 76), (11, 72)]
m_gain = env_seg([(0, 0), (M0 - 0.01, 0), (M0 + 0.25, 0.8), (16.7, 0.8), (17.0, 0.95), (19.0, 1.1), (MEND - 0.5, 1.0), (MEND - 0.02, 0.6), (MEND, 0.0), (30, 0)])
mus = np.zeros(NS + 2 * SR)
def madd(x, t0, g):
    i = int(t0 * SR); j = min(len(mus), i + len(x))
    if i >= 0 and j > i: mus[i:j] += g * x[:j - i]
for bar in range(8):
    ch = CH[bar % 4]; t0 = M0 + bar * 4 * beat
    madd(bass(mtof(ch[0] - 12)), t0, 0.20); madd(bass(mtof(ch[0] - 12), 0.9), t0 + 2.5 * beat, 0.11)
    for e, k in enumerate([0, 2, 1, 3, 2, 1, 3, 2]):
        madd(vibe(mtof(ch[k] + 12), 1.6, 3.2), t0 + e * beat / 2, 0.05 * (1.2 if e % 4 == 0 else 0.85))
    d = 4 * beat; t = tt(d); env = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.6)
    pad = sum(np.sin(2 * np.pi * mtof(n) * t) + 0.25 * np.sin(2 * np.pi * mtof(n + 12) * t) for n in ch)
    madd(pad * env, t0, 0.022)
for rep in range(3):
    for (b, n) in MEL:
        tm = M0 + rep * 12 * beat + b * beat
        if tm < MEND: madd(vibe(mtof(n), 2.4, 2.0), tm, 0.085)
buf[:NS] += mus[:NS] * m_gain
'''
EXTRA = r'''
def heartbeat(t, g=0.42):
    for dt, k in ((0, 1.0), (0.2, 0.7)):
        add(sweep(74, 38, 0.14, 12), t + dt, g * k); add(sweep(170, 95, 0.10, 16), t + dt, g * k * 0.45)
def creep(t0, d, g=0.09):
    q = tt(d)
    x = (np.sin(2 * np.pi * 61.7 * q) + 0.8 * np.sin(2 * np.pi * 65.4 * q) + 0.4 * np.sin(2 * np.pi * 185 * q)) * np.minimum(1, q / 0.4) * np.minimum(1, (d - q) / 0.08)
    add(x, t0, g)
def thunder(t, g=0.22):
    d = 1.6; add(bnoise(d, 40, 400, 91) * np.exp(-tt(d) * 2.2) * np.minimum(1, tt(d) / 0.02), t, g); add(bnoise(0.12, 1500, 9000, 92) * np.exp(-tt(0.12) * 30), t, g * 0.5)
def riser(t=29.45): add(bnoise(0.5, 400, 6000, 60) * np.minimum(1, tt(0.5) / 0.45) ** 2 * np.minimum(1, (0.5 - tt(0.5)) / 0.03), t, 0.16)
def steps(t0, n, gap=0.19, g=0.1):
    for k in range(n): step(t0 + k * gap, g, k)
def door(t): hiss(t, 0.5, 0.09, 8)
'''
def build(cfg, events, out='audio.py'):
    open(out, 'w').write(HEAD + '\n' + cfg + BODY + HELP + EXTRA + events + '\n' + TAIL + '\n')
