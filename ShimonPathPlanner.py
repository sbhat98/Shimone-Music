import sched, time
import numpy as np
import argparse
from pythonosc import osc_message_builder
from pythonosc import udp_client

SECONDS_TO_CROSS_KEYBOARD = 1.0

def main():
    melody = [ 20, 0,32, 0,31,29,27, 0,
               24,25,22,24,27, 0,25, 0,
               24, 0, 0, 0, 0, 0,22, 0,
               19, 0,22, 0,20, 0, 0, 0,

               20, 0,32, 0,31,29,27, 0,
               24,25,22,24,27, 0,25, 0,
               24, 0, 0, 0, 0, 0,22, 0,
               19, 0,22, 0,20, 0, 0, 0,

               24, 0,24,25,22, 0,24, 0,
               27, 0, 0, 0,24, 0,27, 0,
               29,31,32, 0,29, 0,30, 0,
               29, 0,27,29,27,25,24, 0,

                0, 0,24,25, 0,22, 0,24,
               27, 0, 0, 0,24, 0,27, 0,
               29,31,32,31,29,30,29,27,
               24,25,22,24,27,25,24,22]
    period = 100
    keyboardSize = 48
    playMelody(period, keyboardSize, melody)

def playMelody(period, keyboardSize, melody):
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip", default="127.0.0.1",
        help="The ip of the OSC server")
    parser.add_argument("--port", type=int, default=5005,
        help="The port the OSC server is listening on")
    args = parser.parse_args()
    client = udp_client.SimpleUDPClient(args.ip, args.port)

    period /= 1000
    maxDist = np.floor(period * keyboardSize / SECONDS_TO_CROSS_KEYBOARD)
    defaultPositions = [keyboardSize * 1 // 8, keyboardSize  * 3 // 8, keyboardSize  * 5 // 8, keyboardSize * 7 // 8]
    malletPositions = defaultPositions
    totalMissed = [0];

    scheduler = sched.scheduler(time.time, time.sleep)
    for i in range(len(melody)):
        nextNote = melody[i]
        scheduler.enter(period, 1, playNote, argument=(maxDist, nextNote, malletPositions, defaultPositions, totalMissed, client))
        scheduler.run()
        i += 1

    print(f'Missed {totalMissed[0]} of {len(melody)} notes')

def playNote(maxDist, targetNote, malletPositions, defaultPositions, totalMissed, client):
    closestMallet = np.argmin([abs(pos - targetNote) for pos in malletPositions])
    for i in range(4):
        if i != closestMallet:
            malletPositions[i] = defaultPositions[i]
    if abs(malletPositions[closestMallet] - targetNote) <= maxDist:
        malletPositions[closestMallet] = targetNote
        client.send_message('/positions', malletPositions)
        client.send_message('/mididata', targetNote)
    else:
        totalMissed[0] += 1

if __name__ == '__main__':
    main()
