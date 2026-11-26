import numpy as np, wave
SR=44100; DUR=30.0; NS=int(SR*DUR)
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
for s in (3.6, 8.0, 12.4, 16.8, 21.2, 25.6): swish(s - 0.04, 0.15, int(s * 10))
for k in range(11): tick(0.05 + k * 0.12, 1700 + 60 * (k % 3), 0.05)
for t0 in (0.15, 0.62, 1.08): add(sweep(74, 38, 0.14, 12), t0, 0.32); add(sweep(74, 38, 0.14, 12), t0 + 0.18, 0.2)
cap(0.02)
add(bnoise(0.6, 400, 6000, 60) * np.minimum(1, tt(0.6) / 0.55) ** 2 * np.minimum(1, (0.6 - tt(0.6)) / 0.03), 29.4, 0.2)

rumble(0.0, 3.5, 0.045, 4); thunk(1.55, 0.3); thunk(1.95, 0.22); blip(2.6, 420, 260, 0.1, 0.2)
cap(3.85)
for i in range(3): blip(3.9 + i * 0.3, 560 + 70 * i, 900 + 80 * i, 0.1)
arp(4.9, (84, 88, 91), 0.07); blip(5.3, 480, 240, 0.12, 0.22); thwap(5.92, 0.12)
cap(8.2)
for k in range(31): tick(8.5 + k * 0.09, 1900 + 12 * k, 0.05)
ding(11.35, 0.15); creak(10.2, 260, 200, 0.4, 0.05)
cap(12.6); rumble(12.6, 16.7, 0.06, 7)
blip(13.5, 440, 440, 0.09, 0.14); blip(13.72, 440, 440, 0.09, 0.14); swish(13.9, 0.12, 31); thunk(15.0, 0.22); ding(15.05, 0.1)
cap(17.0); creak(17.05, 320, 420, 0.3, 0.08)
for i in range(4):
    swish(16.8 + 0.7 + i * 0.3, 0.1, 40 + i); splash(16.8 + 1.45 + i * 0.3, 0.13, 71 + i)
rumble(18.4, 21.1, 0.05, 9)
for k in range(9): blip(18.6 + k * 0.28, 300, 380, 0.04, 0.1)
blip(21.3, 600, 900, 0.1); blip(21.55, 700, 1000, 0.09); cap(21.4)
for k in range(5): tick(21.6 + k * 0.12, 2200, 0.05)
for k in range(6): step(22.0 + k * 0.19, 0.09)
for k in range(6): step(22.9 + k * 0.19, 0.09)
ding(24.2, 0.12)
cap(25.72); cap(25.8); arp(26.1, (84, 88, 91, 96), 0.1); thunk(26.1, 0.18)
cap(27.55); cap(27.62)
for i in range(3): blip(27.8 + i * 0.25, 700 + 150 * i, 1000 + 180 * i, 0.08, 0.06)
arp(28.6, (79, 84, 88), 0.09)
x=buf[:NS]
from scenes import EDIT
from edit import edited_audio
x = edited_audio(x, SR, EDIT)
x[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR)); x[:int(0.004*SR)]*=np.linspace(0,1,int(0.004*SR))
x=np.tanh(x*1.6); x=x/np.max(np.abs(x))*0.89
st=np.stack([x,x],1); pcm=(st*32767).astype('<i2')
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x)/SR)

