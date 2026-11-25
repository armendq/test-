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
# scene 1: the drop
add(sweep(520,880,0.09),0.02,0.12); cap(0.05); cap(0.12)
add(sweep(400,1100,0.5),1.35,0.12)                                   # the throw
thunk(2.25,0.22); add(pluck(900,0.25,12),2.26,0.10)                    # clunk in the box
add(bnoise(0.4,400,6000,7)*np.minimum(1,tt(0.4)/0.36)**2,2.8,0.22)
# scene 2: flip and postmark
cap(3.45); cap(3.52); rumble(3.2,7.8,0.04,9)
for k in range(9): add(np.sin(2*np.pi*1900*tt(0.012))*hann(int(SR*0.012)),3.3+k*0.36,0.035)   # letters zipping
thunk(4.1,0.12); add(sweep(380,980,0.5),4.2,0.13)                      # the flip
add(sweep(120,45,0.25,10),5.22,0.5); add(bnoise(0.06,300,3000,31)*np.exp(-tt(0.06)*50),5.22,0.25); ding(5.26,0.13)   # stamp
add(sweep(700,400,0.25),5.5,0.07)                                     # dizzy
cap(5.85); cap(5.92)
t=5.95
while t<7.25:
    u=(t-5.95)/1.3; add(np.sin(2*np.pi*(1500+900*u)*tt(0.018))*hann(int(SR*0.018)),t,0.09); t+=0.075-0.045*u
ding(7.28,0.14)
# scene 3: the camera
swish(7.8,0.18,5); cap(8.05); cap(8.12); rumble(7.8,12.6,0.035,13)
blip(8.55,1200,1200,0.07,0.05); blip(8.7,1500,1500,0.07,0.05); ding(8.95,0.14)
thunk(10.45,0.10)
for k in range(3): blip(10.55+0.12*k,1200,1200,0.06,0.05)
cap(10.3); cap(10.37)
for dt in (0,0.18):
    d=0.14; q=tt(d); add(np.sign(np.sin(2*np.pi*150*q))*hann(len(q)),10.78+dt,0.07)          # cannot read
add(sweep(500,350,0.2),11.1,0.07)
# scene 4: the room in Utah
swish(12.6,0.18,6); cap(12.85); cap(12.92)
add(bnoise(0.45,800,7000,41)*hann(int(SR*0.45)),13.2,0.10); blip(13.7,700,1000,0.10)
cap(15.2); cap(15.27)
t=14.5
k=0
while t<16.5:
    add(np.sin(2*np.pi*(2300 if k%3 else 1800)*tt(0.012))*hann(int(SR*0.012)),t,0.07); t+=0.075+0.02*((k*7)%3); k+=1
ding(16.55,0.17); blip(16.56,900,1500,0.10)
# scene 5: barcode and sorting
swish(18.2,0.18,7); cap(18.45); cap(18.52); rumble(18.2,21.4,0.04,25)
add(bnoise(0.6,3000,11000,43)*hann(int(SR*0.6)),18.9,0.11)             # spray
d=1.7; q=tt(d); add(bnoise(d,500,5000,45)*np.minimum(1,q/0.3)*np.minimum(1,(d-q)/0.25),19.7,0.08)   # speed
add(sweep(500,1500,0.4),19.75,0.10)
cap(20.3); cap(20.37)
add(bnoise(0.4,700,6000,47)*hann(int(SR*0.4)),21.2,0.14); thunk(22.02,0.24); ding(22.06,0.13)
# scene 6: the door
swish(22.8,0.18,8); cap(23.1); cap(23.17)
for k in range(4): add(sweep(170,70,0.09,18),23.1+0.31*k,0.12)
add(sweep(240,330,0.35)*(1+0.4*np.sin(2*np.pi*30*tt(0.35))),24.1,0.07)   # the door
blip(24.9,600,1000,0.11,0.1)
for k,n in enumerate((84,88,91,96)): add(pluck(mtof(n),1.6,2.6),25.2+0.055*k,0.13)
for k in range(3): add(pluck(mtof(91+k*2),0.4,8),25.6+0.3*k,0.07)
# scene 7: the fridge
swish(27.4,0.18,9); cap(27.55); cap(27.62)
add(np.sin(2*np.pi*1700*tt(0.02))*hann(int(SR*0.02)),27.75,0.12)
for k,n in enumerate((79,84,88)): add(pluck(mtof(n),1.2,3.0),28.0+0.12*k,0.09)
add(bnoise(0.6,400,6000,60)*np.minimum(1,tt(0.6)/0.55)**2*np.minimum(1,(0.6-tt(0.6))/0.03),29.4,0.24)
x=buf[:NS]
x[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR)); x[:int(0.004*SR)]*=np.linspace(0,1,int(0.004*SR))
x=np.tanh(x*1.6); x=x/np.max(np.abs(x))*0.89
st=np.stack([x,x],1); pcm=(st*32767).astype('<i2')
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x)/SR)
