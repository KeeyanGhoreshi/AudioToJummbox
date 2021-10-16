
import codecs
import json

import math
import matplotlib.pyplot as plt
import numpy as np
import librosa
from scipy.signal import find_peaks
from scipy.fft import fftshift
from scipy.fft import rfft, rfftfreq
from scipy import signal
from scipy.fftpack import fft


def loadFile(filepath):
    try:
        data, fs = librosa.load(filepath)
        return data, fs
    except Exception:
        raise RuntimeError("Failed to load file " + filepath)

# get a chunk of the data, duration in milliseconds
def chunkData(data, fs, duration):
    # get chunk size in samples
    rate = fs/1000 # samples per millisecond
    n = int(duration * rate)
    # chunk data into chunks of size [n]
    # using list comprehension
    final = [data[i * n:(i + 1) * n] for i in range((len(data) + n - 1) // n )] 
    return final

def getPitch(frequency):
       return math.log((frequency/440),2) * 12 + 69.0

def myround(x, prec=2, base=.04):
    return round(base * round(float(x)/base),prec)

def calcFft(data, dur, fs): 
    N = int(fs * dur)
    yf = rfft(data)
    xf = rfftfreq(N, 1 / fs)

    return (xf, abs(yf))

def processChunk(chunk, windowSize, fs):
    hann = signal.windows.hann(len(chunk))
    windowed = hann * chunk
    for i in range(len(windowed)*9):
        windowed = np.append(windowed,0)
    xf, yf = calcFft(windowed,windowSize/100, fs)
    return (xf, yf)

def getBinSize(amps):
    an_array = np.array(amps)
    median = np.median(an_array)
    standard_deviation = np.std(an_array)
    distance_from_median = abs(an_array - median)
    max_deviations = 5
    not_outlier = distance_from_median < max_deviations * standard_deviation
    no_outliers = an_array[not_outlier]
    nBins = 50
    at = plt.hist(no_outliers, nBins)
    bins = at[1]
    binSize = at[1][1] - at[1][0]
    return binSize

def getNote(freq, amp, floor, binSize):
    note = {}
    pitch = 0
    ampBin = round((amp - floor)/binSize)
    if ampBin > 50:
        ampBin = 50
#     ampBin = getVolume(amp/max(amps))
    if(freq > 4186.009):
        # higher than C8
        adjusted_freq = freq/6  # divide by 6, max freq 24k, adjusted to max 4k
        pitch = myround(getPitch(adjusted_freq))
        note["freqMult"] = 6
    else:
        pitch = myround(getPitch(freq))
        note["freqMult"] = 1
    note["pitch"] = int(pitch) - 12
    detune = (pitch - int(pitch))/0.04
    note["detune"] = round(detune)
    note["volume"] = ampBin
    return note

def makeNote(note, tick, mod):
    volume = 100
    return {
        "pitches": [
            note["pitch"]
        ],
        "points": [
            {
                "tick": tick,
                "pitchBend": 0,
                "volume": volume,
                "forMod": mod
            },
            {
                "tick": tick+1,
                "pitchBend": 0,
                "volume": volume,
                "forMod": mod
            }
        ]
    }
def makeModNote(volume, tick, pitch):
        return {
        "pitches": [
            pitch
        ],
        "points": [
            {
                "tick": tick,
                "pitchBend": 0,
                "volume": volume,
                "forMod": True
            },
            {
                "tick": tick+1,
                "pitchBend": 0,
                "volume": volume,
                "forMod": True
            }
        ]
    }
def convert(filepath, tempo, base, output, smooth):
    data, fs = loadFile(filepath)
    windowSize = 60/(tempo*24) * 1000 # in ms
    normalized_tone = np.int32((data / max(data)) * 2147483647)
    DURATION = len(normalized_tone)/fs
    pointsPerTick = []
    freqs = []
    amps = []
    chunked = chunkData(normalized_tone, fs, windowSize)
    for chunk in chunked:
        points = []
        xf, yf = processChunk(chunk, windowSize, fs)
        peaks, _ = find_peaks(yf, prominence=max(yf)*.02)      # BEST!
        for peak in peaks:
            pair = (xf[peak], yf[peak])
            freqs.append(xf[peak])
            amps.append(yf[peak])
            points.append(pair)
        pointsPerTick.append(points)
    binSize = getBinSize(amps)
    converted = []
    # turn the freq/amp into a note/volume
    for points in pointsPerTick:
        convertedPoints = []
        for point in points:
            convertedPoints.append(getNote(point[0], point[1], min(amps), binSize))
        converted.append(convertedPoints)
    song = {}
    with codecs.open(base, encoding='utf-8') as f:
        song = json.load(f)

    channelSix = song["channels"][18:24]
    channelOne = song["channels"][0:18]
    modChannels = song["channels"][24:32]
    for i, notes in enumerate(converted):
        tick = (i)%192
        pattern = int((i)/192)
        highFreq = [ele for ele in notes if ele["freqMult"]==6]
        lowFreq = [ele for ele in notes if ele["freqMult"]==1]

        while len(lowFreq) > 18:
            minVol = min(lowFreq, key=lambda x:x['volume'])
            lowFreq.remove(minVol)
        while len(highFreq) > 6:
            minVol = min(highFreq, key=lambda x:x['volume'])
            highFreq.remove(minVol)

        for k, note in enumerate(lowFreq):
            channelOne[k]["patterns"][pattern]["notes"].append(makeNote(note, tick, False))
            modChannel = int(k/6)
            modPitch = k%6
            modChannels[modChannel]["patterns"][pattern]["notes"].append(makeModNote(note["volume"], tick, modPitch))
            modChannels[modChannel+4]["patterns"][pattern]["notes"].append(makeModNote(note["detune"]+50, tick, modPitch))
        for j, note2 in enumerate(highFreq):
            modPitch = j%6
            modChannel = 3
            channelSix[j]["patterns"][pattern]["notes"].append(makeNote(note2, tick, False))
            modChannels[modChannel]["patterns"][pattern]["notes"].append(makeModNote(note2["volume"], tick, modPitch))
            modChannels[modChannel+4]["patterns"][pattern]["notes"].append(makeModNote(note2["detune"]+50, tick, modPitch))

    with open(output, 'w', encoding='utf-8') as f:
        json.dump(song, f, ensure_ascii=False, indent=4)

def smoothMod():
    smooth = {}
    points = {
        0: [],
        1: [],
        2: [],
        3: [],
        4: [],
        5: []
    }
    with codecs.open('data.json', encoding='utf-8') as f:
        smooth = json.load(f)
        modChannels = smooth["channels"][24:28]
        pitchChannels = smooth["channels"][0:24]
    #     for pitchChannel in pitchChannels:
    #         for pattern in pitchChannel["patterns"]:
    #             for thing in pattern["notes"]:
    #                 aa = thing["points"]
    #                 if len(aa) == 2:
    #                     aa[1]["volume"]=0
        for modChannel in modChannels: 
            for pattern in modChannel["patterns"]:
                for thing in pattern["notes"]:
                    points[thing["pitches"][0]].append(thing["points"][0])
                i = 1
                gaps = {
                    0: [],
                    1: [],
                    2: [],
                    3: [],
                    4: [],
                    5: []
                }
                for j in range(6):
                    pointIter = iter(points[j])
                    point2 = next(pointIter, 'end')
                    for i in range(96):
                        if point2 == 'end':
                            pass
                        else:
                            if point2['tick'] == i*3:
                                gaps[j].append({'tick': point2['tick'], 'pitchBend': 0, 'volume': point2['volume'], 'forMod':True})
                                gaps[j].append({'tick': point2['tick']+1, 'pitchBend': 0, 'volume': point2['volume'], 'forMod':True})
                                gaps[j].append({'tick': point2['tick']+2, 'pitchBend': 0, 'volume': point2['volume'], 'forMod':True})
                                point2 = next(pointIter, 'end')
                            else:
                                gaps[j].append({'tick': i*3, 'pitchBend': 0, 'volume': 0, 'forMod': True})
                pattern["notes"] = [
                    {'pitches': [0], 'points': gaps[0]},
                    {'pitches': [1], 'points': gaps[1]},
                    {'pitches': [2], 'points': gaps[2]},
                    {'pitches': [3], 'points': gaps[3]},
                    {'pitches': [4], 'points': gaps[4]},
                    {'pitches': [5], 'points': gaps[5]},
                ]
                points = {
                    0: [],
                    1: [],
                    2: [],
                    3: [],
                    4: [],
                    5: []
                }
    with open('data.json', 'w', encoding='utf-8') as f:
        json.dump(smooth, f, ensure_ascii=False, indent=4)