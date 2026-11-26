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
# scene 1 (0.0): you lock it, you throw the key
add(pluck(1700,0.12,30),0.01,0.2); add(bnoise(0.03,1500,8000,2)*np.exp(-tt(0.03)*90),0.01,0.2); cap(0.06); cap(0.13)      # click
add(sweep(700,1500,0.7),0.08,0.07); add(sweep(1500,520,0.95),0.82,0.07)                                                # the key flies
swish(0.6,0.14,3)                                                                                                      # camera pulls back
splash(1.8,0.22)
for k,n in enumerate((84,88)): add(pluck(mtof(n),0.9,4),1.95+0.45*k,0.08)
creak(2.33,200,95,0.34,0.16); thunk(2.36,0.2); clink(2.46,2500,0.07); clink(2.58,3000,0.06)                           # the rail cracks
add(sweep(600,420,0.2),2.75,0.06)
# scene 2 (3.6): one million locks, 45 tonnes
swish(3.6,0.18,5); cap(3.85); cap(3.92)
t=4.0
while t<5.33:
    u=(t-4.0)/1.33; tick(t,1500+900*u,0.085); t+=0.075-0.045*u
ding(5.37,0.14)
for k in range(5): add(pluck(mtof(96+(k*5)%9),0.4,9),4.3+0.62*k,0.03)
blip(5.7,300,620,0.12,0.12); cap(5.95); cap(6.02)
add(sweep(950,280,0.28),5.96,0.10)
add(sweep(110,40,0.4,8),6.24,0.6); add(bnoise(0.09,150,2500,33)*np.exp(-tt(0.09)*40),6.24,0.3); ding(6.3,0.10)          # 45 tonnes land
creak(6.34,150,85,0.6,0.14); creak(7.1,170,120,0.35,0.07)
# scene 3 (8.0): the railing falls
swish(8.0,0.18,6); cap(8.25); cap(8.32)
for k in range(4): step(8.08+0.3*k)
creak(8.4,320,240,0.26,0.09); creak(8.7,300,210,0.26,0.11); creak(8.97,280,180,0.3,0.14)
blip(9.25,500,950,0.10,0.09); add(sweep(620,140,0.55),9.2,0.12)
add(sweep(120,42,0.35,9),9.78,0.6); add(bnoise(0.4,250,6500,35)*np.exp(-tt(0.4)*9),9.78,0.34)                           # crash
for k in range(12): clink(9.8+0.045*k+0.01*((k*7)%5),1500+((k*577)%1700),0.05)
cap(10.3); cap(10.37); ding(10.5,0.10)
creak(11.53,210,100,0.3,0.14); thunk(11.56,0.16); clink(11.66,2500,0.07); clink(11.78,3000,0.06)
# scene 4 (12.4): Paris cuts them all off
swish(12.4,0.18,7); cap(12.65); cap(12.72)
for k in range(3): step(12.48+0.3*k)
add(sweep(800,1700,0.2),13.7,0.07)
add(bnoise(0.05,2000,10000,37)*np.exp(-tt(0.05)*70),13.9,0.4); clink(13.9,2700,0.16); thunk(13.9,0.14)                  # snip
add(sweep(950,300,0.46),13.93,0.10)
thunk(14.4,0.3)
for k in range(4): clink(14.41+0.05*k,1600+k*420,0.06)
cap(14.8); cap(14.87)
for k,n in enumerate((96,100,103)): add(pluck(mtof(n),0.5,7),14.95+0.1*k,0.05)
add(sweep(520,1050,0.4),15.42,0.08)
clink(15.85,3100,0.17); add(pluck(4650,0.5,8),15.85,0.07)                                                               # tink on the panel
d=0.7; add(sweep(1900,900,d)*(1+0.5*np.sin(2*np.pi*24*tt(d))),15.9,0.045); thunk(16.6,0.08)
# scene 5 (16.8): the auction
swish(16.8,0.18,8); cap(17.05); cap(17.12)
for k,t0 in enumerate((17.85,18.2,18.55,18.9)): blip(t0,520+90*k,900+120*k,0.12,0.09)
cap(19.25); cap(19.32)
add(bnoise(0.14,900,6000,39)*hann(int(SR*0.14)),19.5,0.10)
add(sweep(150,55,0.2,12),19.65,0.55); add(pluck(430,0.18,24),19.65,0.3); add(bnoise(0.04,300,3000,41)*np.exp(-tt(0.04)*70),19.65,0.25)   # gavel
for k,n in enumerate((84,88,91,96)): add(pluck(mtof(n),1.4,2.8),19.72+0.055*k,0.12)
blip(20.06,700,1000,0.07,0.07)
# scene 6 (21.2): the money
swish(21.2,0.18,9); cap(21.45); cap(21.52)
t=21.65
while t<23.2:
    u=(t-21.65)/1.55; tick(t,1400+800*u,0.05); t+=0.08-0.04*u
for i in range(9):
    ta=21.65+i*0.22+0.75; add(pluck(mtof(88+(0,4,7)[i%3]),0.5,7),ta,0.09); tick(ta,3200,0.05)
ding(23.22,0.13); cap(23.65); cap(23.72)
for k,t0 in enumerate((24.1,24.2,24.35)): blip(t0,600+80*k,1000+90*k,0.10,0.08)
for k,n in enumerate((84,88,91,96)): add(pluck(mtof(n),1.6,2.6),24.5+0.055*k,0.11)
for k in range(3): add(pluck(mtof(91+k*2),0.4,8),24.9+0.25*k,0.06)
# scene 7 (25.6): and the key?
add(bnoise(0.3,300,3000,10)*hann(int(SR*0.3)),25.6,0.2); cap(25.75); cap(25.82)
d=4.4; q=tt(d); add(bnoise(d,60,500,51)*np.minimum(1,q/0.4)*np.minimum(1,(d-q)/0.3)*(1+0.3*np.sin(2*np.pi*0.7*q)),25.6,0.045)   # under water
for k,t0 in enumerate((26.0,26.45,26.8,27.9,28.75,29.2)): blip(t0,300+40*(k%3),720+60*(k%3),0.05,0.07)                    # bubbles
blip(27.25,380,820,0.13,0.12); clink(27.27,2000,0.09)                                                                    # the fish nudges the key
cap(27.7); cap(27.77)
for k,t0 in enumerate((28.1,28.18,28.3)): blip(t0,700+150*k,1000+180*k,0.08,0.06)
ding(28.52,0.11)
for k,n in enumerate((79,84,88)): add(pluck(mtof(n),1.2,3.0),28.9+0.12*k,0.09)
add(bnoise(0.6,400,6000,60)*np.minimum(1,tt(0.6)/0.55)**2*np.minimum(1,(0.6-tt(0.6))/0.03),29.4,0.24)
x=buf[:NS]
x[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR)); x[:int(0.004*SR)]*=np.linspace(0,1,int(0.004*SR))
x=np.tanh(x*1.6); x=x/np.max(np.abs(x))*0.89
st=np.stack([x,x],1); pcm=(st*32767).astype('<i2')
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x)/SR)
