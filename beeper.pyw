import winsound, keyboard, random, threading, time, json
import librosa, os, soundfile
from playsound import playsound
MODE = 0
#0 = Random
#1 = Linair
QUIT = False
RANGE = (500, 2037)
LINAIR_STAIR = 50
SOUND_FILE = ""
Affected = "1234567890\bqwertyuiopasdfghjklzxcvbnm \n"
CONFIG_NAME = 'BeepConfig.json'
BACKOUT_KEY = '='
TEMPLATE = {"MODE":0,"RANGE":RANGE,"STAIR":50,"SOUNDFILE":"","BACKOUT":"=","Note":"Mode 0: Random beep with every key, Mode 1: Linair beep. Range: the range of the frequency. Mode 3: Using the soundfile (linear mode).Stair: The amount of frequency added in a linair mode. Backout: key to end the program"}

#json configFIle
try:
    file = open("BeepConfig.json", 'r')
    temp = json.load(file)
    file.close()
    RANGE = temp["RANGE"]
    MODE = temp["MODE"]
    LINAIR_STAIR = temp["STAIR"]
    BACKOUT_KEY = temp['BACKOUT']
    SOUND_FILE = temp['SOUNDFILE']
    print("Loaded file")
except(Exception) as e:
    print(e)
    file = open("BeepConfig.json", 'w')
    json.dump(TEMPLATE, file, indent=4)
    file.close()
    print("Used default template")


class track:
    global QUIT, RANGE
    def __init__(self, key="", freq=RANGE[0], SoundFile="") -> None:
        self.freq = freq
        self.key = key
        self.SoundFile = SoundFile
    def start(self):
        if self.SoundFile == "":
            while not QUIT:
                if keyboard.is_pressed(self.key):
                    winsound.Beep(self.freq, 50)
                    time.sleep(0.1)
        else:
            #if soundfile is used
            while not QUIT:
                if keyboard.is_pressed(self.key):
                    playsound(self.SoundFile)
                    time.sleep(0.1)
def BREAKOUT():
    global QUIT, BACKOUT_KEY
    while not QUIT:
        if keyboard.is_pressed(BACKOUT_KEY):
            QUIT = True
            break

#Asigns every key a frequency
pos = 0
created_soundfiles = False
files = []
for char in Affected:
    
    #Random mode
    if MODE == 0:
        x = track(char, random.randint(RANGE[0], RANGE[1]))
        threading.Thread(target=x.start).start()
    #Linair mode
    elif MODE == 1:
        curr_freq = (pos * LINAIR_STAIR)+RANGE[0]
        if curr_freq > RANGE[1]:
            pos = 0
            curr_freq =(pos * LINAIR_STAIR)+RANGE[0]
        x = track(char, curr_freq)
        threading.Thread(target=x.start).start()
    #Soundfile mode
    elif MODE == 2:
        if not created_soundfiles:
            try: os.mkdir("sounds")
            except: pass
            for x in range(12):
                filename = SOUND_FILE
                y, sr = librosa.load(filename)
                steps = float(x*0.5)
                new_y = librosa.effects.pitch_shift(y, sr, steps)
                outputName = f"sounds/{SOUND_FILE.split('.')[0]}{x}.wav"
                soundfile.write(outputName, new_y, sr,)
                files.append(outputName)
            created_soundfiles = True
        try:
            file = files[pos]
            print(file)
        except(IndexError):
            pos = 0
            file = files[pos]
        x = track(SoundFile=file, key=char)
        threading.Thread(target=x.start).start()
            
        


    pos+=1

print(f"Active threads: {threading.active_count()}")
BREAKOUT() #Breakout on the mainthread