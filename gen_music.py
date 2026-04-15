#!/usr/bin/env python3
"""Generate proper 8-bit chiptune music for arcade game using Python synthesis"""
import struct, math, wave, os, array

SAMPLE_RATE = 44100

def sine_tone(freq, dur, vol=0.3):
    samples = int(SAMPLE_RATE * dur)
    buf = array.array('h')
    for i in range(samples):
        t = i / SAMPLE_RATE
        env = min(1.0, i / (SAMPLE_RATE * 0.005))
        rel = max(0, 1 - (i / (SAMPLE_RATE * dur)) * 1.2)
        val = int(32767 * vol * env * rel * math.sin(2 * math.pi * freq * t))
        buf.append(val)
    return buf

def square_tone(freq, dur, vol=0.25):
    samples = int(SAMPLE_RATE * dur)
    buf = array.array('h')
    for i in range(samples):
        t = i / SAMPLE_RATE
        env = min(1.0, i / (SAMPLE_RATE * 0.008))
        rel = max(0, 1 - (i / (SAMPLE_RATE * dur)) * 0.8)
        val = int(32767 * vol * env * rel * (1 if math.sin(2 * math.pi * freq * t) >= 0 else -1))
        buf.append(val)
    return buf

def triangle_tone(freq, dur, vol=0.3):
    samples = int(SAMPLE_RATE * dur)
    buf = array.array('h')
    for i in range(samples):
        t = i / SAMPLE_RATE
        env = min(1.0, i / (SAMPLE_RATE * 0.01))
        rel = max(0, 1 - (i / (SAMPLE_RATE * dur)) * 1.0)
        phase = (freq * t) % 1.0
        val = int(32767 * vol * env * rel * (2 * phase - 1))
        buf.append(val)
    return buf

def kick_tone(dur=0.15, vol=0.5):
    samples = int(SAMPLE_RATE * dur)
    buf = array.array('h')
    for i in range(samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 30)
        freq = 150 * math.exp(-t * 20)
        val = int(32767 * vol * env * math.sin(2 * math.pi * freq * t))
        buf.append(val)
    return buf

def snare_tone(dur=0.1, vol=0.3):
    samples = int(SAMPLE_RATE * dur)
    buf = array.array('h')
    for i in range(samples):
        t = i / SAMPLE_RATE
        env = math.exp(-t * 40)
        val = int(32767 * vol * env * (2 * (os.urandom(1)[0] / 255.0) - 1))
        buf.append(val)
    return buf

def hihat_tone(dur=0.04, vol=0.12):
    samples = int(SAMPLE_RATE * dur)
    buf = array.array('h')
    for i in range(samples):
        env = math.exp(-i / (SAMPLE_RATE * 0.015))
        val = int(32767 * vol * env * (2 * (os.urandom(1)[0] / 255.0) - 1))
        buf.append(val)
    return buf

def write_wav(path, bufs, total_beats, bpm):
    beat_dur = 60.0 / bpm
    total_sec = total_beats * beat_dur + 2.0
    total_samples = int(total_sec * SAMPLE_RATE)
    
    out = array.array('h', [0] * total_samples)
    
    for buf in bufs:
        for i, s in enumerate(buf):
            if i < total_samples:
                out[i] = max(-32768, min(32767, out[i] + s))
    
    with wave.open(path, 'wb') as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SAMPLE_RATE)
        w.writeframes(out.tobytes())
    sz = os.path.getsize(path)
    print(f"  → {path} ({sz/1024:.0f} KB)")


def note(name, oct, beats, vol=0.25):
    freq_map = {
        'C':261.63,'D':293.66,'E':329.63,'F':349.23,
        'G':392.00,'A':440.00,'B':493.88,
        'C#':277.18,'D#':311.13,'F#':369.99,'G#':415.30,'A#':466.16,
        'Db':277.18,'Eb':311.13,'Gb':369.99,'Ab':415.30,'Bb':466.16,
    }
    freq = freq_map.get(name, 440) * (2 ** (oct - 4))
    beat_dur = 60.0 / 142
    dur = beats * beat_dur
    return square_tone(freq, dur, vol)


def make_race_song():
    print("Generating race track...")
    beat_dur = 60.0 / 142
    bufs = []
    total_beats = 36

    # Melody: E minor driving race tune
    melody = [
        # Phrase 1
        (0,   'E',5,0.5,0.22), (0.5,'E',5,0.5,0.18),
        (1,   'G',5,0.5,0.22), (1.5,'E',5,0.5,0.18),
        (2,   'D',5,0.5,0.22), (2.5,'C',5,0.5,0.18),
        (3,   'B',4,1.0,0.28),
        # Phrase 2
        (4,   'E',5,0.5,0.22), (4.5,'E',5,0.5,0.18),
        (5,   'G',5,0.5,0.22), (5.5,'E',5,0.5,0.18),
        (6,   'D',5,0.5,0.22), (6.5,'C',5,0.5,0.18),
        (7,   'B',4,1.5,0.32),
        # Phrase 3 - higher
        (9,   'G',5,0.5,0.22), (9.5,'A',5,0.5,0.18),
        (10,  'B',5,1.0,0.28), (11, 'D',5,0.5,0.22),
        (11.5,'C',5,0.5,0.18),
        (12,  'B',5,1.0,0.28), (13, 'A',5,0.5,0.22),
        (13.5,'G',5,0.5,0.18),
        (14,  'E',5,1.0,0.28),
        (15,  'E',5,0.5,0.18), (15.5,'E',5,0.5,0.18),
        # Phrase 4 - fastest
        (16,  'E',5,0.25,0.22), (16.25,'G',5,0.25,0.18),
        (16.5,'E',5,0.25,0.22), (16.75,'G',5,0.25,0.18),
        (17,  'E',5,0.5,0.22),  (17.5,'D',5,0.5,0.18),
        (18,  'C',5,0.5,0.22),  (18.5,'D',5,0.5,0.18),
        (19,  'B',4,0.5,0.28),  (19.5,'C',5,0.5,0.22),
        (20,  'D',5,1.0,0.28),
        (21,  'G',5,0.5,0.22),  (21.5,'A',5,0.5,0.18),
        (22,  'B',5,1.0,0.32),
        (23,  'E',5,0.5,0.22),  (23.5,'G',5,0.5,0.18),
        (24,  'E',5,0.5,0.22),  (24.5,'D',5,0.5,0.18),
        (25,  'C',5,1.0,0.28),
        (26,  'B',4,0.5,0.22),  (26.5,'C',5,0.5,0.18),
        (27,  'B',4,2.0,0.35),
    ]

    for beat, name, oct, beats, vol in melody:
        bufs.append(note(name, oct, beats, vol))

    # Bass line
    bass = [
        (0,'E',3,2,0.2),(2,'E',3,2,0.2),
        (4,'E',3,2,0.2),(6,'E',3,2,0.2),
        (8,'G',3,2,0.2),(10,'F',3,2,0.2),
        (12,'A',3,2,0.2),(14,'E',3,2,0.2),
        (16,'E',3,2,0.2),(18,'E',3,2,0.2),
        (20,'D',3,2,0.2),(22,'C',3,2,0.2),
        (24,'B',3,2,0.22),(26,'A',3,2,0.22),
        (28,'E',3,2,0.2),(30,'E',3,2,0.2),
        (32,'E',3,2,0.2),(34,'E',3,2,0.2),
    ]
    for beat, name, oct, beats, vol in bass:
        bufs.append(triangle_tone(
            {'C':130.81,'D':146.83,'E':164.81,'F':174.61,'G':196.00,'A':220.00,'B':246.88}[name]
            * (2**(oct-4)), beats * beat_dur, vol))

    # Drums: kick on 1 and 3, snare on 2 and 4, hh on 8ths
    for beat in [0,2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,34]:
        start = int(beat * beat_dur * SAMPLE_RATE)
        k = kick_tone()
        for i, s in enumerate(k):
            idx = start + i
            if idx < 88200 * 40:
                pass

    for b in range(0, 36, 1):
        bufs.append(kick_tone())
        bufs.append(hihat_tone())
        bufs.append(hihat_tone(vol=0.08))
        bufs.append(hihat_tone(vol=0.08))
        bufs.append(snare_tone())

    write_wav('/home/aipi/.openclaw/workspace/games/race_song.wav', bufs, 36, 142)


def make_park_song():
    print("Generating parking track...")
    beat_dur = 60.0 / 95
    bufs = []
    total_beats = 32

    # Chill melody in A minor - dreamy
    melody = [
        (0,  'A',4,1.5,0.22),
        (1.5,'C',5,1.0,0.18),
        (2.5,'E',5,1.5,0.22),
        (4,  'G',5,1.0,0.18),
        (5,  'E',5,1.5,0.22),
        (6.5,'C',5,1.0,0.18),
        (7.5,'A',4,2.0,0.28),

        (9.5,'F',4,1.5,0.22),
        (11, 'A',4,1.0,0.18),
        (12, 'C',5,1.5,0.22),
        (13.5,'E',5,1.0,0.18),
        (14.5,'D',5,1.0,0.22),
        (15.5,'C',5,1.0,0.18),
        (16.5,'A',4,2.0,0.28),

        (18.5,'E',4,1.5,0.22),
        (20, 'G',4,1.0,0.18),
        (21, 'A',4,1.5,0.22),
        (22.5,'C',5,1.0,0.18),
        (23.5,'B',4,1.0,0.22),
        (24.5,'A',4,1.0,0.18),
        (25.5,'G',4,2.0,0.28),

        (27.5,'C',5,1.5,0.22),
        (29, 'E',5,1.0,0.18),
        (30, 'F',5,1.5,0.22),
        (31.5,'G',5,1.0,0.18),
    ]

    for beat, name, oct, beats, vol in melody:
        freq_map = {
            'C':261.63,'D':293.66,'E':329.63,'F':349.23,
            'G':392.00,'A':440.00,'B':493.88
        }
        freq = freq_map.get(name, 440) * (2 ** (oct - 4))
        dur = beats * beat_dur
        # Alternating triangle + sine for warmth
        bufs.append(triangle_tone(freq, dur * 0.8, vol))
        bufs.append(sine_tone(freq * 2, dur * 0.3, vol * 0.12))

    # Simple soft kick on downbeats
    for b in range(0, 32, 2):
        k = kick_tone(dur=0.2, vol=0.2)
        bufs.append(k)

    # Gentle hi-hats
    for b in range(0, 32, 1):
        bufs.append(hihat_tone(dur=0.03, vol=0.06))

    write_wav('/home/aipi/.openclaw/workspace/games/park_song.wav', bufs, 32, 95)


make_race_song()
make_park_song()
print("Done!")