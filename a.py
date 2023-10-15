import mido
import math
import random

mid = mido.MidiFile('mond_3.mid', clip=True)

f = open('b.txt', 'w')
f.write(str(mid.tracks))
f.close()

f = open('b.txt', 'r')
lines = f.readlines()
f.close()

f = open('c.txt', 'w')

# def parse_line(line):
#     line = line.strip()
#     if line[:7] == "Message" or line[:11] == "MetaMessage":

#         line = line[line.index("Message") + 8:-2]
#         line = line.split(",")
#         line = list(map(str.strip, line))
#         message = line.pop(0).strip("'")
#         if message == "sequencer_specific" or message == "end_of_track":
#             return False
#         line = [line[i].split("=") for i in range(len(line))]
#         data = {}
#         data["message"] = message
#         data |= {line[i][0]:eval(line[i][1]) for i in range(len(line))}
        
#         return data
#     return False

# tempo = 500000
# ticks_per_beat = mid.ticks_per_beat
# times = [0] * 16

# # output = [[] for _ in range(16)]
# output = []

# for line in lines:
#     command = parse_line(line)

#     if not command: continue

#     message = command["message"]
#     if message == "set_tempo":
#         tempo = command["tempo"]    

#     if message == "note_on" or message == "note_off":
#         channel = command["channel"]
#         millis = int((tempo * command["time"] / ticks_per_beat) / (10 ** 3))
#         volume = int(100 * command["velocity"] / 127)
       
#         if message == "note_on":
#             # print(volume)
#             output.append(["start", times[channel], 89-command['note']-8, volume])
#             # f.write(f"startNote({89-command['note']-8}, {times[channel]}, {channel}, {volume})\n")
#         else:
#             output.append(["stop", times[channel], 89-command['note']-8])
#             # f.write(f"playNote({89-command['note']-8}, {times[channel]-prev[channel]}, {channel}, {volume});\n")
#             # prev[channel] = times[channel]
#             # f.write(f"stopNote({89-command['note']-8}, {times[channel]}, {channel})\n")
#         times[channel] += millis

# output.sort(key=lambda x : x[1])
# f.write("var output = " + str(output) + ";")

xs = [0] * 16
n = []
volumes = [0] * 16
volumeCounts = [0] * 16
for i in range(16): 
    n.append([])

tempo = 120
tpb = mid.ticks_per_beat

for i in range(len(lines)):
    if 'tempo=' in lines[i]:
        k = lines[i].index("tempo=")+6
        s = lines[i][k:]
        s = s[:s.index(",")]
        num = int(s)
        tempo = 10**6*60/num

scale = 6000/(tempo*tpb)
end_of_track = 0

for i in range(len(lines)):
    go = True
    if 'note_off' in lines[i]:
        go = False

    if "end_of_track" in lines[i]:
        xs = [5469] * 16
        end_of_track += 1
        
    try:
        k = lines[i].index("time=")+5
        time = lines[i][k:]
        num2 = int(time.replace(")", "").replace(",",""))

        l = lines[i].index('channel=')+8
        c = lines[i][l:l+2]
        channel = int(c.strip().replace(',','')) + end_of_track

        if not 'set_tempo' in lines[i]:
            xs[channel] += num2

        j = lines[i].index("note=")+5
        note = lines[i][j:(j+3)]
        num = int(note.replace(",", ""))

        if go:
            if 'velocity=' in lines[i]:
                m = lines[i].index("velocity=")+9
                v = lines[i][m:m+3].strip().replace(",","")
                velocity = int(v)
                volumes[channel] += velocity
                volumeCounts[channel] += 1

            # if(num <= 128 and num >= 41):
            n[channel].append([math.floor(scale*xs[channel]/4), 89-num-8])
    except:
        continue

numChannels = 0
tVolumes = []

def map(value, istart, istop, ostart, ostop):
      return ostart + (ostop - ostart) * ((value - istart) / (istop - istart))

f.write('notes = [')
for i in range(len(n)):
    if len(n[i]) > 0:
        f.write(str(n[i]) + ',')
        tVolumes.append(
            math.floor(map(volumes[i]/(volumeCounts[i]), 0, 127, 0, 100))/100)
        numChannels += 1
f.write('];\n')
f.write('speed = ' + str(math.floor(tempo)) + ';\n')
f.write('trackColors = [')
for i in range(numChannels):
    f.write(str(i))
    if(i < numChannels-1):f.write(",")
f.write("];\n")
a = [0] * numChannels
f.write('trackInstruments = ' + str(a) + ';\n')
f.write("trackVolumes = " + str(tVolumes) + ";")
if numChannels > 6:
    f.write('\ncolors.push(')
    for i in range(6, numChannels):
        f.write('color(' + str(random.randint(0, 255)) + ',' + str(random.randint(0, 255)) + ',' + str(random.randint(0,255)) + ')')
        if(i < numChannels-1): f.write(', ')
    f.write(');')