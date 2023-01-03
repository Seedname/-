import mido
import math
import random
mid = mido.MidiFile('bigshot.mid', clip=True)

f = open('b.txt', 'w')
f.write(str(mid.tracks))
f.close()

f = open('b.txt', 'r')
lines = f.readlines()
f.close()

f = open('c.txt', 'w')

xs = [0] * len(mid.tracks)
n = []
for i in range(len(mid.tracks)): n.append([])

tempo = 0
tpb = mid.ticks_per_beat

for i in range(len(lines)):
    if 'tempo=' in lines[i]:
        k = lines[i].index("tempo=")+6
        s = lines[i][k:]
        s = s[:s.index(",")]
        num = int(s)
        tempo = 10**6*60/num

scale = 6000/(tempo*tpb)

for i in range(len(lines)):
    go = True
    if 'note_off' in lines[i]:
        go = False

    try:
        k = lines[i].index("time=")+5
        time = lines[i][k:]
        num2 = int(time.replace(")", "").replace(",",""))

        l = lines[i].index('channel=')+8
        c = lines[i][l:l+2]
        channel = int(c.replace(',',''))

        if not 'set_tempo' in lines[i]:
            xs[channel] += num2

        j = lines[i].index("note=")+5
        note = lines[i][j:(j+3)]
        num = int(note.replace(",", ""))


        if go:
            # if(num <= 128 and num >= 41):
            if(num <= 128 and num >= 41):
                # if 89-num-8 < 35:
                # print(num2)
                n[channel].append([math.floor(scale*xs[channel]/4), 89-num-8])
    except:
        continue

numChannels = 0

f.write('notes = [')
for i in range(len(n)):
    if(len(n[i]) > 0):
        f.write(str(n[i]) + ',')
        numChannels += 1
f.write('];\n')
f.write('speed = ' + str(math.floor(tempo)) + ';\n')
f.write('trackColors = [')
for i in range(numChannels):
    f.write(str(i))
    if(i < numChannels-1):f.write(",")
f.write("];\n")
a = [0] * numChannels
f.write('trackInstruments = ' + str(a) + ';')
if numChannels > 6:
    f.write('\ncolors.push(')
    for i in range(6, numChannels):
        f.write('color(' + str(random.randint(0, 255)) + ',' + str(random.randint(0, 255)) + ',' + str(random.randint(0,255)) + ')')
        if(i < numChannels-1): f.write(', ')
    f.write(');')