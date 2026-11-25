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
# scene 1: check-in
add(sweep(520,880,0.09),0.02,0.12); cap(0.05); cap(0.12)
rumble(1.25,3.0,0.06,3); blip(1.28,300,520,0.10)
thwap(2.45); add(bnoise(0.45,400,6000,7)*np.minimum(1,tt(0.45)/0.4)**2,2.8,0.22)
# scene 2: tag scan
cap(3.45); cap(3.52); rumble(3.2,4.4,0.05,9); thunk(4.4,0.16)
for k in range(4): blip(4.42+0.2*k,1400,1400,0.07,0.05)
add(sweep(300,700,0.12),4.66,0.12)                                   # card pops
ding(5.25,0.15); blip(5.25,900,1500,0.10)
rumble(5.6,7.4,0.05,11); add(sweep(500,1300,0.3),6.4,0.10)
# scene 3: x-ray
swish(7.6,0.18,5); cap(7.85); cap(7.92); rumble(7.6,8.7,0.05,13); thwap(8.45,0.12,15)
d=1.2; q=tt(d); add(np.sin(2*np.pi*np.cumsum(180+220*q/d)/SR)*(1+0.5*np.sin(2*np.pi*30*q))*np.minimum(1,q/0.1)*np.minimum(1,(d-q)/0.1),8.8,0.07)   # scanner hum
for k in range(3): blip(9.05+0.3*k,1100+200*k,1100+200*k,0.06,0.05)
add(sweep(400,900,0.12),9.6,0.14); add(sweep(900,500,0.14),9.75,0.10)   # a duck?
ding(10.5,0.16)
thwap(10.75,0.12,17); rumble(10.7,12.3,0.05,19)
# scene 4: the ride
swish(12.4,0.2,6); cap(12.6); cap(12.67)
d=5.8; q=tt(d); wind=bnoise(d,500,5000,21)*(0.7+0.3*np.sin(2*np.pi*0.9*q))*np.minimum(1,q/0.3)*np.minimum(1,(d-q)/0.25); add(wind,12.4,0.085)
roll=bnoise(d,80,600,23)*(1+0.6*np.sin(2*np.pi*22*q))*np.minimum(1,q/0.2)*np.minimum(1,(d-q)/0.2); add(roll,12.4,0.06)
add(sweep(500,1700,0.45),12.95,0.16)                                  # wheee
cap(14.45)
for k in range(18): add(np.sin(2*np.pi*(1500+40*k)*tt(0.018))*hann(int(SR*0.018)),14.5+k*0.067,0.10)
ding(15.72,0.14)
cap(16.3); cap(16.37)
t=16.35
while t<17.38:
    u=(t-16.35)/1.03; add(np.sin(2*np.pi*(1500+900*u)*tt(0.018))*hann(int(SR*0.018)),t,0.10); t+=0.07-0.04*u
ding(17.4,0.16)
# scene 5: sorting
swish(18.2,0.18,7); cap(18.4); cap(18.47); rumble(18.2,23.0,0.035,25)
add(sweep(900,300,0.6),19.25,0.12); thunk(19.98,0.26); ding(20.0,0.13)
cap(20.5); cap(20.57)
add(pluck(mtof(76),0.3,9),20.95,0.10); add(pluck(mtof(73),0.4,8),21.15,0.10)     # uh-oh
blip(21.1,700,700,0.05,0.2)
add(sweep(900,260,0.7),21.88,0.13); thunk(22.6,0.28)
add(sweep(520,360,0.22),22.33,0.16); add(sweep(390,250,0.34),22.57,0.16)          # wrong chute
# scene 6: reunion
swish(23.0,0.18,8); cap(23.3); cap(23.37); thwap(23.4,0.12,27); rumble(23.0,25.2,0.03,29)
blip(23.95,600,1000,0.12,0.1); blip(24.1,800,1300,0.12,0.1)
add(bnoise(0.3,600,6000,31)*hann(int(SR*0.3)),25.25,0.16)                         # hop
add(sweep(220,120,0.12,10),25.75,0.22)
for k,n in enumerate((84,88,91,96)): add(pluck(mtof(n),1.6,2.6),25.76+0.055*k,0.13)
for k in range(3): add(pluck(mtof(91+k*2),0.4,8),25.9+0.3*k,0.07)
# scene 7: the lost one
swish(27.4,0.18,9); cap(27.55); cap(27.62)
add(sweep(330,300,0.3),27.95,0.13); add(sweep(294,262,0.3),28.3,0.13); add(sweep(262,196,0.55),28.65,0.14)   # sad trio
add(bnoise(0.6,400,6000,60)*np.minimum(1,tt(0.6)/0.55)**2*np.minimum(1,(0.6-tt(0.6))/0.03),29.4,0.24)
x=buf[:NS]
x[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR)); x[:int(0.004*SR)]*=np.linspace(0,1,int(0.004*SR))
x=np.tanh(x*1.6); x=x/np.max(np.abs(x))*0.89
st=np.stack([x,x],1); pcm=(st*32767).astype('<i2')
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x)/SR)
