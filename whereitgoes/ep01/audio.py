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
def blip(t,f0=500,f1=900,g=0.13): add(sweep(f0,f1,0.07),t,g)
# scene 1
add(bnoise(0.5,400,5000,3)*hann(int(SR*0.5)),0.0,0.28)                       # toss whoosh
add(bnoise(0.7,300,7000,4)*np.exp(-tt(0.7)*9),2.3,0.42)                      # splash
add(sweep(140,60,0.3,6),2.3,0.35)
# scene 2
for i,t in enumerate([2.75,2.95,3.2,3.5,3.75,4.0]): blip(t,420+40*i,820+60*i,0.10)
cap(2.9); cap(2.97)
add(pluck(1760,0.5,9)+0.6*pluck(2637,0.5,10),4.3,0.22)                        # landing tink
for k in range(7): add((bnoise(0.03,1500,6000,20+k)*np.exp(-tt(0.03)*120))+0.5*sweep(900,700,0.03),4.78+k*0.185,0.2)  # dentures
cap(4.85)
# scene 3
swish(6.5,0.18,5); cap(6.7); cap(6.77)
for k,t in enumerate([7.05,7.6,8.15]): add(bnoise(0.5,800,6000,30+k)*hann(int(SR*0.5)),t,0.22)
add(bnoise(0.4,200,1500,39)*hann(int(SR*0.4)),8.85,0.2)                       # hose arrives
for k in range(10): add(sweep(300+k*45,1100+k*90,0.07),9.42+0.17*k,0.2)       # suction pops
add(sweep(500,1900,0.3),10.95,0.2)                                           # hero wheee
# scene 4
swish(11.5,0.18,6); cap(11.7); cap(11.77)
t=12.4
while t<15.35:
    u=(t-12.4)/3.0; add(np.sin(2*np.pi*(1500+900*u)*tt(0.018))*hann(int(SR*0.018)),t,0.11); t+=0.11-0.07*min(1,u*1.2)+0.02*u*u
add(sum(pluck(f,1.4,3.2) for f in (1318.5,1975.5,2637.0)),15.4,0.16)          # ding
for k in range(31):
    if k%3==0: add(pluck(2093+ (k%5)*120,0.12,30),12.42+0.115*k,0.045)
add(sum(pluck(mtof(n),0.6,6) for n in (84,88,91)),15.87,0.12)                 # hero lands on the pile
# scene 5
swish(16.5,0.18,7); cap(16.65); cap(16.72); cap(19.7); cap(19.77)
for k,t in enumerate([17.8,19.0,20.2]):
    add(sweep(520,260,0.1),t-0.25,0.16); add(pluck(mtof(79+2*k),0.5,7)+0.5*pluck(mtof(84+2*k),0.5,7),t,0.13)
# scene 6
swish(22.5,0.18,8); cap(22.6)
for k,n in enumerate((84,88,91,96,100)): add(pluck(mtof(n),1.6,2.6),23.65+0.055*k,0.14)   # coin becomes dinner
add(bnoise(0.9,2000,12000,50)*np.exp(-tt(0.9)*4)*np.minimum(1,tt(0.9)/0.05),23.65,0.07)
cap(23.9); cap(23.97)
for k in range(3): add(pluck(mtof(91+k*2),0.4,8),24.4+0.5*k,0.07)
# scene 7
swish(27.5,0.18,9); cap(27.62); cap(27.69)
add(bnoise(0.6,400,6000,60)*np.minimum(1,tt(0.6)/0.55)**2*np.minimum(1,(0.6-tt(0.6))/0.03),29.4,0.26)   # wind-up into the loop
x=buf[:NS]
x[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR)); x[:int(0.004*SR)]*=np.linspace(0,1,int(0.004*SR))
x=np.tanh(x*1.6); x=x/np.max(np.abs(x))*0.89
st=np.stack([x,x],1); pcm=(st*32767).astype('<i2')
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x)/SR)
