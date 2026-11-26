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

for s in (3.0, 6.8, 10.4, 13.6, 17.8, 21.4): swish(s - 0.04, 0.15, int(s * 10))
for k in range(9): tick(0.05 + k * 0.12, 1700 + 60 * (k % 3), 0.05)
for t0 in (0.15, 0.62, 1.08): add(sweep(74, 38, 0.14, 12), t0, 0.32); add(sweep(74, 38, 0.14, 12), t0 + 0.18, 0.2)
cap(0.02); squeak(1.2, 0.5, 0.05)
thwap(1.9, 0.2); blip(1.95, 300, 160, 0.12, 0.16); cap(2.3)
cap(3.2)
for i in range(3): step(3.2 + i * 0.2, 0.1); blip(4.3 + i * 0.6, 420, 260, 0.1, 0.1); thwap(4.35 + i * 0.6, 0.09, 10 + i)
for k in range(10): blip(4.2 + k * 0.25, 500 + 40 * (k % 4), 300, 0.04, 0.06)
cap(7.0)
for k in range(16): crunch(7.25 + k * 0.08, 0.06, k)
cap(8.8)
for i in range(5): blip(8.85 + i * 0.22, 600 + 90 * i, 1000 + 110 * i, 0.11); thwap(8.85 + i * 0.22, 0.06, 20 + i)
cap(10.6); creak(10.7, 220, 380, 0.9, 0.05)
for k in range(14): tick(10.7 + k * 0.1, 1500 + 70 * k, 0.04)
ding(11.95, 0.12); ding(12.25, 0.1)
cap(13.8)
for k in range(10): add(bnoise(0.18, 2000, 9000, 300 + k) * hann(int(SR * 0.18)), 13.9 + k * 0.13, 0.07)
swish(14.6, 0.14, 33); thunk(15.2, 0.28)
for k in range(30): tick(15.2 + k * 0.06, 1600 + 25 * k, 0.04)
ding(17.0, 0.15)
cap(18.0)
for k in range(14): blip(18.3 + k * 0.18, 500 + 50 * (k % 5), 260, 0.05, 0.07); thwap(18.32 + k * 0.18, 0.05, 40 + k)
cap(21.55); arp(21.8, (84, 88, 91, 96), 0.1)
for i in range(3): blip(22.2 + i * 0.25, 700 + 150 * i, 1000 + 180 * i, 0.08, 0.06)
n0 = int((DUR - 0.7) * SR); buf[n0:NS] *= np.linspace(1, 0.2, NS - n0)
x=buf[:NS]
x[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR)); x[:int(0.004*SR)]*=np.linspace(0,1,int(0.004*SR))
x=np.tanh(x*1.6); x=x/np.max(np.abs(x))*0.89
st=np.stack([x,x],1); pcm=(st*32767).astype('<i2')
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x)/SR)

