import numpy as np, wave
SR=44100; DUR=24.0; NS=int(SR*DUR)
buf=np.zeros(NS+SR)
def add(x,t0,g=1.0):
    i=int(t0*SR)
    if i<0: x=x[-i:]; i=0
    j=min(len(buf),i+len(x))
    if j>i: buf[i:j]+=g*x[:j-i]
def tt(d): return np.arange(int(SR*d))/SR
def hann(n): return np.hanning(n)
def bnoise(d,lo,hi,seed):
    n=int(SR*d); r=np.random.default_rng(seed).standard_normal(n); F=np.fft.rfft(r); fr=np.fft.rfftfreq(n,1/SR)
    F[(fr<lo)|(fr>hi)]=0; x=np.fft.irfft(F,n); return x/(np.max(np.abs(x))+1e-9)
def pluck(freq,d=0.6,dec=6.0,bright=1.0):
    t=tt(d); s=np.sin(2*np.pi*freq*t)+0.5*bright*np.sin(2*np.pi*2*freq*t)*np.exp(-t*8)+0.25*bright*np.sin(2*np.pi*3*freq*t)*np.exp(-t*14)
    return s*np.exp(-t*dec)*np.minimum(1,t/0.004)
def sweep(f0,f1,d,dec=0):
    t=tt(d); f=f0+(f1-f0)*t/d; ph=2*np.pi*np.cumsum(f)/SR; s=np.sin(ph)*hann(len(t))
    return s*np.exp(-t*dec) if dec else s
def mtof(m): return 440.0*2**((m-69)/12)
# ---------------- music: 96 bpm, 12 bars, C Am F G
beat=0.625; chords=[(60,64,67),(57,60,64),(53,57,60),(55,59,62)]
pat=[0,1,2,1,2,1,0,1]
for bar in range(12):
    ch=chords[bar%4]; t0=bar*4*beat
    lift = 1.0 if bar<6 else 1.25
    for e in range(8):
        n=ch[pat[e]]+12+(12 if e==6 else 0)
        add(pluck(mtof(n),0.7,5.5),t0+e*beat/2,0.085*lift*(1.15 if e%2==0 else 0.8))
    for b in (0,2):
        add(pluck(mtof(ch[0]-12),1.1,3.0,0.2),t0+b*beat,0.17)
    for e in range(8):
        if e%2==1: add(bnoise(0.05,5000,11000,bar*8+e)*np.exp(-tt(0.05)*60),t0+e*beat/2,0.035)
    if bar>=6 and bar<11:   # warm pad under the turn and payoff
        d=4*beat; t=tt(d); env=np.minimum(1,t/0.5)*np.minimum(1,(d-t)/0.5)
        pad=sum(np.sin(2*np.pi*mtof(n)*t)+0.3*np.sin(2*np.pi*mtof(n+12)*t) for n in ch)
        add(pad*env,t0,0.03)
# ---------------- sfx
def swish(t,g=0.16,seed=1): add(bnoise(0.26,1200,9000,seed)*hann(int(SR*0.26)),t,g)
def cap(t): add(sweep(620,930,0.05),t,0.10)
def blip(t,f0=500,f1=900,g=0.13,d=0.07): add(sweep(f0,f1,d),t,g)
def ding(t,g=0.16): add(sum(pluck(f,1.2,3.4) for f in (1318.5,1975.5,2637.0)),t,g)
def thunk(t,g=0.3): add(sweep(140,55,0.16,14),t,g); add(bnoise(0.04,200,1800,int(t*100))*np.exp(-tt(0.04)*80),t,g*0.4)
def rumble(t0,t1,g=0.05,seed=3):
    d=t1-t0; x=bnoise(d,60,420,seed)*(1+0.5*np.sin(2*np.pi*13*tt(d))); e=np.minimum(1,tt(d)/0.15)*np.minimum(1,(d-tt(d))/0.15)
    add(x*e,t0,g)
def thwap(t,g=0.14,seed=5):
    for k in range(3): add(bnoise(0.05,300,3000,seed+k)*np.exp(-tt(0.05)*60),t+k*0.06,g)
def creak(t,f0=300,f1=220,d=0.28,g=0.07): add(sweep(f0,f1,d)*(1+0.6*np.sin(2*np.pi*31*tt(d))),t,g)
def tick(t,f=1900,g=0.05): add(np.sin(2*np.pi*f*tt(0.014))*hann(int(SR*0.014)),t,g)
def clink(t,f=2400,g=0.08): add(pluck(f,0.35,11),t,g); add(pluck(f*1.5,0.25,14),t,g*0.5)
def step(t,g=0.12): add(sweep(170,70,0.09,18),t,g)
def splash(t,g=0.2,seed=71):
    d=0.45; add(bnoise(d,700,6500,seed)*np.exp(-tt(d)*7)*np.minimum(1,tt(d)/0.01),t,g); add(sweep(420,160,0.14),t,g*0.6)
def bell(t,g=0.05,seed=0):      # a small sleigh bell
    d=0.22; add(bnoise(d,5200,12000,900+seed)*np.exp(-tt(d)*22),t,g); add(pluck(3300+70*(seed%4),0.2,20),t,g*0.5)
def squeak(t,d=0.34,g=0.06,f0=900,f1=1350): add(sweep(f0,f1,d)*(1+0.7*np.sin(2*np.pi*46*tt(d))),t,g); add(bnoise(d,2500,7000,int(t*50))*hann(int(SR*d)),t,g*0.35)
def crunch(t,g=0.10,seed=0): add(bnoise(0.11,500,4200,700+seed)*np.exp(-tt(0.11)*26)*np.minimum(1,tt(0.11)/0.01),t,g); add(sweep(150,80,0.08,18),t,g*0.6)
def poof(t,g=0.2,seed=0): d=0.4; add(bnoise(d,150,1600,800+seed)*np.exp(-tt(d)*9)*np.minimum(1,tt(d)/0.012),t,g); add(sweep(130,60,0.2,10),t,g*0.8)
def fwoomp(t,g=0.16,seed=0): d=0.42; add(bnoise(d,120,2200,600+seed)*np.exp(-tt(d)*8)*np.minimum(1,tt(d)/0.03),t,g); add(sweep(210,90,0.3,7),t,g*0.9)
def arp(t,notes=(84,88,91,96),g=0.11,gap=0.055,d=1.4,dec=2.8):
    for k,n in enumerate(notes): add(pluck(mtof(n),d,dec),t+gap*k,g)

def splosh(t, g=0.16, seed=0, d=0.5):
    add(bnoise(d, 150, 2500, 700 + seed) * np.exp(-tt(d) * 7) * np.minimum(1, tt(d) / 0.01), t, g); add(sweep(400, 120, 0.12, 9), t, g * 0.5)
def plip(t, g=0.07, seed=0): add(sweep(900, 1500, 0.06, 20), t, g); add(bnoise(0.08, 800, 4000, 900 + seed) * np.exp(-tt(0.08) * 40), t, g * 0.5)
def surf(t, d=1.4, g=0.06, seed=3): q = tt(d); add(bnoise(d, 300, 3000, 800 + seed) * np.sin(np.pi * q / d) ** 2, t, g)
for s in (3.0, 6.8, 10.4, 13.6, 17.8, 21.4): swish(s - 0.04, 0.15, int(s * 10))
for k in range(9): tick(0.05 + k * 0.12, 1700 + 60 * (k % 3), 0.05)
for t0 in (0.15, 0.62, 1.08): add(sweep(74, 38, 0.14, 12), t0, 0.32); add(sweep(74, 38, 0.14, 12), t0 + 0.18, 0.2)
cap(0.02); squeak(1.2, 0.5, 0.05); surf(0.0, 3.0, 0.04, 1)
splosh(1.9, 0.2); cap(2.3)
cap(3.2); surf(3.0, 3.8, 0.04, 2)
for k in range(22): plip(3.55 + k * 0.12, 0.05, k)
for k in range(20): tick(3.5 + k * 0.13, 1500 + 40 * k, 0.04)
cap(7.0)
q = tt(3.4); add(bnoise(3.4, 60, 400, 77) * np.minimum(1, q / 0.3) * np.minimum(1, (3.4 - q) / 0.3), 6.9, 0.1)
for k in range(12): blip(7.1 + k * 0.27, 700 + 90 * (k % 4), 1100 + 90 * (k % 4), 0.05, 0.05)
cap(10.6); creak(10.6, 200, 340, 1.1, 0.05); surf(10.4, 3.2, 0.04, 4)
for k in range(6): thwap(10.8 + k * 0.15, 0.04, 30 + k)
blip(11.75, 400, 800, 0.1, 0.12); ding(12.35, 0.13)
cap(13.8); surf(13.6, 4.2, 0.04, 5)
for k in range(40): tick(14.6 + k * 0.065, 1500 + 20 * k, 0.04)
ding(17.25, 0.14)
cap(18.0); surf(17.8, 1.6, 0.08, 6); splosh(18.3, 0.08, 3, 0.4)
swish(19.1, 0.12, 44); blip(19.9, 500, 900, 0.08, 0.08); ding(20.05, 0.15)
cap(21.55); arp(21.8, (84, 88, 91, 96), 0.1)
for i in range(3): blip(22.2 + i * 0.25, 700 + 150 * i, 1000 + 180 * i, 0.08, 0.06)
n0 = int((DUR - 0.7) * SR); buf[n0:NS] *= np.linspace(1, 0.2, NS - n0)
x=buf[:NS]
x[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR)); x[:int(0.004*SR)]*=np.linspace(0,1,int(0.004*SR))
x=np.tanh(x*1.6); x=x/np.max(np.abs(x))*0.89
st=np.stack([x,x],1); pcm=(st*32767).astype('<i2')
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x)/SR)

