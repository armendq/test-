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
for b in range(48):                                   # sleigh bells ride the beat, very low
    add(bnoise(0.09,6000,12000,400+b)*np.exp(-tt(0.09)*40),b*beat,0.016 if b%2==0 else 0.010)
# scene 1 (0.0): the letter above the slot, on a snowy evening
blip(0.01,620,1250,0.16,0.10); add(bnoise(0.03,1500,8000,2)*np.exp(-tt(0.03)*90),0.01,0.16); cap(0.06); cap(0.13)        # a little gasp
for k in range(5): bell(0.02+0.12*k,0.07-0.008*k,k)
d=1.2; add(sweep(520,640,d)*(1+0.8*np.sin(2*np.pi*14*tt(d))),0.1,0.035)                                              # it trembles
swish(0.6,0.14,3)                                                                                                    # the camera pulls back
add(sweep(650,1450,0.45),1.35,0.075); add(sweep(1450,520,0.42),1.78,0.075)                                           # the letter flies
thunk(2.2,0.26); blip(2.3,330,170,0.12,0.14)                                                                         # the mailbox swallows it
for k,t0 in enumerate((2.42,2.77)): blip(t0,560+90*k,960+120*k,0.10,0.08)                                            # the child hops
for k,n in enumerate((88,91)): add(pluck(mtof(n),0.8,4),2.45+0.3*k,0.07)
add(bnoise(0.42,900,5000,13)*hann(int(SR*0.42)),2.75,0.07)                                                           # the snow cap slides off
poof(3.2,0.24,1); blip(3.27,480,900,0.09,0.08)
# scene 2 (3.6): Santa has a real address
swish(3.6,0.18,5); cap(3.85); cap(3.92)
rumble(3.6,4.5,0.05,3); tick(4.5,900,0.12); thunk(4.5,0.10)                                                          # the belt stops
t=4.55
while t<5.9:
    u=(t-4.55)/1.35; tick(t,1300+900*u,0.07); t+=0.085-0.045*u                                                       # the camera reads
blip(4.82,700,430,0.10,0.14)                                                                                         # ?
ding(5.95,0.14); cap(5.95); cap(6.02)                                                                                # found it
for k in range(3): blip(5.96+0.08*k,640+130*k,980+150*k,0.09,0.07)
blip(6.02,420,880,0.10,0.14)                                                                                         # the hero hops
add(pluck(mtof(100),0.5,7),6.12,0.06)
for k,n in enumerate((91,96)): add(pluck(mtof(n),0.7,5),6.72+0.1*k,0.08)                                             # the camera falls in love
swish(7.15,0.2,15); add(sweep(500,1500,0.5),7.15,0.07); rumble(7.15,7.9,0.05,4)                                      # off it goes
# scene 3 (8.0): before 1912, the Dead Letter Office
swish(8.0,0.18,6); cap(8.25); cap(8.32)
d=3.5; q=tt(d); add(bnoise(d,70,600,53)*np.minimum(1,q/0.3)*np.minimum(1,(d-q)/0.1)*(1+0.4*np.sin(2*np.pi*5*q)),8.05,0.06)    # the stove roars
rc=np.random.default_rng(77)
for k in range(46): tick(8.1+3.4*rc.random(),700+2600*rc.random(),0.035+0.04*rc.random())                           # crackle
for k,T in enumerate((8.45,8.95,9.45,9.95,10.45)):
    thwap(T-0.03,0.09,20+k); add(sweep(800,1300,0.3),T,0.04)                                                         # a letter flies
    fwoomp(T+0.5,0.17,k); blip(T+0.46,520,300,0.07,0.1)                                                              # and burns, the hero flinches
cap(10.3); cap(10.37)
creak(10.98,260,330,0.22,0.06)                                                                                       # the clerk lifts the last one
add(sweep(140,50,0.3,10),11.55,0.6); add(bnoise(0.06,300,5000,35)*np.exp(-tt(0.06)*50),11.55,0.34); clink(11.56,1500,0.14)     # the stove door slams
ding(11.62,0.16)                                                                                                     # the calendar: 1912
for k in range(3): add(bnoise(0.07,1200,7000,90+k)*hann(int(SR*0.07)),11.72+0.17*k,0.07)                             # the torn page flutters down
for k,n in enumerate((84,88,91)): add(pluck(mtof(n),1.0,3.4),11.75+0.1*k,0.08)
# scene 4 (12.4): 1912, postmasters may open it
swish(12.4,0.18,7); cap(12.65); cap(12.72)
add(bnoise(0.3,700,4000,17)*hann(int(SR*0.3)),12.45,0.08); thunk(13.0,0.10)                                          # the hero slides onto the desk
blip(13.15,500,760,0.07,0.07)                                                                                        # the opener
d=0.28; add(sweep(700,2600,d)*(1+0.5*np.sin(2*np.pi*60*tt(d))),13.42,0.07); add(bnoise(d,2500,9000,19)*hann(int(SR*d)),13.42,0.07)   # zip
blip(13.7,420,940,0.13,0.10); add(pluck(mtof(96),0.5,7),13.72,0.07)                                                  # the flap pops
for k in range(4): add(bnoise(0.08,1200,6500,110+k)*hann(int(SR*0.08)),13.85+0.17*k,0.07)                            # the letter unfolds
for k,n in enumerate((79,84,88,91)): add(pluck(mtof(n),0.7,5),13.9+0.16*k,0.06)
cap(14.75); cap(14.82); ding(14.86,0.14); blip(14.84,380,760,0.10,0.10)                                              # year 114
for k,t0 in enumerate((15.55,15.95)): blip(t0,640+90*k,1040+110*k,0.09,0.07)                                         # hearts
for k in range(5): tick(15.62+0.105*k,2300 if k%2 else 2000,0.06)                                                    # the teddy waves
blip(15.72,700,1150,0.08,0.08)
arp(15.5,(84,88,91),0.07,0.07,1.0,3.4)
# scene 5 (16.8): details removed, adopted online
swish(16.8,0.18,8); cap(17.05); cap(17.12)
for k,t0 in enumerate((17.35,17.75,18.15)): squeak(t0,0.34,0.075,820+70*k,1250+90*k); tick(t0+0.35,1100,0.07)        # three black bars
for k in range(3): step(18.75+0.24*k,0.10)                                                                           # the stranger arrives
add(bnoise(0.3,900,5000,23)*hann(int(SR*0.3)),18.85,0.08)
cap(19.1); cap(19.17); blip(19.17,460,880,0.10,0.10)                                                                 # the ADOPT button
for k in range(6): tick(19.42+0.11*k,1700,0.03)                                                                      # the cursor
tick(20.14,1200,0.16); tick(20.2,800,0.14)                                                                           # click
ding(20.22,0.15); arp(20.24)
for k,t0 in enumerate((20.3,20.42,20.56,20.72)): blip(t0,620+110*k,1000+130*k,0.08,0.07)
for k in range(4): bell(20.26+0.14*k,0.06,k)
# scene 6 (21.2): the gift arrives
swish(21.2,0.18,9); cap(21.45); cap(21.52)
for k in range(4): crunch(21.5+0.3*k,0.11,k)                                                                         # steps in the snow
creak(22.5,230,330,0.42,0.09); thunk(22.98,0.07)                                                                     # the door opens
blip(23.07,520,1040,0.11,0.10)                                                                                       # the child sees it
add(bnoise(0.22,900,5000,29)*hann(int(SR*0.22)),23.2,0.07)
add(bnoise(0.3,600,4000,31)*hann(int(SR*0.3)),23.55,0.08)                                                            # the camera pushes in
thunk(23.9,0.12); ding(23.93,0.13); arp(23.96,(84,88,91,96),0.11)                                                    # the hug
for k in range(5): bell(23.95+0.13*k,0.07,k)
for k,t0 in enumerate((24.0,24.3,24.6)): add(pluck(mtof(91+2*k),0.5,7),t0,0.06)                                      # hearts
tick(24.12,1500,0.05)
for k,t0 in enumerate((24.25,24.73,25.22)): blip(t0,560+60*k,980+80*k,0.09,0.08); crunch(t0+0.4,0.06,10+k)           # the child jumps
# scene 7 (25.6): adopted, and the deadline
swish(25.6,0.18,10); cap(25.75); cap(25.82)
blip(26.02,480,900,0.10,0.09); tick(26.06,1600,0.07)                                                                 # the calendar
blip(26.22,700,1000,0.07,0.07)                                                                                       # the stamp appears
squeak(26.45,0.3,0.06,1000,1500)                                                                                     # the red ring
add(sweep(900,300,0.17),26.68,0.09)                                                                                  # the stamp comes down
add(sweep(120,45,0.32,9),26.85,0.6); add(bnoise(0.07,200,3000,41)*np.exp(-tt(0.07)*45),26.85,0.3); add(pluck(430,0.18,24),26.85,0.22)   # stamp
ding(26.9,0.14); arp(26.96,(84,88,91,96),0.12)
for k in range(6): bell(26.95+0.12*k,0.065,k)
for k,t0 in enumerate((27.0,27.32,27.64,27.96)): add(pluck(mtof(93+(k%3)*2),0.4,8),t0,0.05)
for k,t0 in enumerate((27.15,27.6)): blip(t0,640+80*k,1000+90*k,0.07,0.07)                                           # the hero hops
cap(27.95); cap(28.02)
for k,t0 in enumerate((28.3,28.62)): blip(t0,700+150*k,1000+180*k,0.08,0.06)                                         # ? ?
for k,n in enumerate((79,84,88)): add(pluck(mtof(n),1.2,3.0),28.9+0.12*k,0.09)
for k in range(3): bell(28.92+0.12*k,0.05,k)
add(bnoise(0.6,400,6000,60)*np.minimum(1,tt(0.6)/0.55)**2*np.minimum(1,(0.6-tt(0.6))/0.03),29.4,0.2)
x=buf[:NS]
x[-int(0.02*SR):]*=np.linspace(1,0,int(0.02*SR)); x[:int(0.004*SR)]*=np.linspace(0,1,int(0.004*SR))
x=np.tanh(x*1.6); x=x/np.max(np.abs(x))*0.89
st=np.stack([x,x],1); pcm=(st*32767).astype('<i2')
w=wave.open('audio.wav','wb'); w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes()); w.close()
print('audio ok', len(x)/SR)
