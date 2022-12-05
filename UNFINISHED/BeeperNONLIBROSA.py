import winsound, keyboard, random, threading, time, json
#import librosa, os, soundfile
from playsound import playsound
MODE = 0
#0 = Random
#1 = Linair
#2 = sound file (kinda broken)

#todo
#fix replay option




QUIT = False
RANGE = (500, 2037)
LINAIR_STAIR = 50
SOUND_FILE = ""
Affected = "1234567890\bqwertyuiopasdfghjklzxcvbnm \n"
CONFIG_NAME = 'BeepConfig.json'
BACKOUT_KEY = '='
REPLAY_BTN = '-'
SCRIPT_FILE = '' #File to program 'song'
TEMPLATE = {"MODE":0,"RANGE":RANGE,"STAIR":50,"SCRIPT_FILE":"","USES_SCRIPT":False,"SOUNDFILE":"","SCRIPT_REPLAY":'',"BACKOUT":"=","Note":"Mode 0: Random beep with every key, Mode 1: Linair beep. Range: the range of the frequency. Mode 3: Using the soundfile (linear mode).Stair: The amount of frequency added in a linair mode. Backout: key to end the program"}

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
    SCRIPT_FILE = temp['SCRIPT_FILE']
    REPLAY_BTN = temp['SCRIPT_REPLAY']
    if not temp["USES_SCRIPT"]:
        SCRIPT_FILE = ''
    print("Loaded file")
except(Exception) as e:
    print(e)
    file = open("BeepConfig.json", 'w')
    json.dump(TEMPLATE, file, indent=4)
    file.close()
    print("Used default template")


class track:
    global QUIT, RANGE
    def __init__(self, key="", freq=RANGE[0], SoundFile="", REPLAY_MODE=False) -> None:
        self.freq = freq
        self.key = key
        self.SoundFile = SoundFile
        self.REPLAY_MODE = REPLAY_MODE
    def start(self):
        if self.REPLAY_MODE:
            print(f'{self.key} is in REPLAYMODE')
            while not QUIT:
                if keyboard.is_pressed(self.key):
                    runScriptfile()
                    
        elif self.SoundFile == "":
            while not QUIT:
                if keyboard.is_pressed(self.key):
                    winsound.Beep(self.freq, 50)
                    time.sleep(0.1)
        
        else:
            #if soundfile is used
            while not QUIT:
                if keyboard.is_pressed(self.key):
                    playsound(self.SoundFile)
                    time.sleep(0.2)
def BREAKOUT():
    global QUIT, BACKOUT_KEY
    while not QUIT:
        if keyboard.is_pressed(BACKOUT_KEY):
            QUIT = True
            break
def PLAY_THREAD_SOUND():
    global SOUND_FILE
    playsound(SOUND_FILE)
def PLAY_THREAD_FREQ(freq):
    winsound.Beep(freq,50)
def runScriptfile():
    global SCRIPT_FILE
    """
    # means 0.1 sec
    $ means 0.5 sec
    * means 1 sec
    """
    
    items = ""
    file = open(SCRIPT_FILE, 'r')
    for line in file:
        items+=line.strip('\n')
    file.close()
    if Bind["USES"] == 'freq':
        for char in items:
            if char == '#':
                print("0.1 sec wait")
                time.sleep(0.1)
            elif char == '$':
                print("0.5 sec wait")
                time.sleep(0.5)
            elif char == '*':
                print("1 sec wait")
                time.sleep(1)
            else:
                threading.Thread(target=PLAY_THREAD_FREQ, args=(Bind[char],)).start()
    elif Bind["USES"] == 'sound':
        for char in items:
            if char == '#':
                time.sleep(0.1)
            elif char == '$':
                time.sleep(0.5)
            elif char == '*':
                time.sleep(1)
            else:
                threading.Thread(target=PLAY_THREAD_SOUND).start()
                time.sleep(0.1)
    

#Asigns every key a frequency
pos = 0
created_soundfiles = False
files = []
Bind = {}
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
        if SCRIPT_FILE == '':
            x = track(char, curr_freq)
            threading.Thread(target=x.start).start()
        else:
            Bind['USES'] = "freq"
            Bind[char] = curr_freq
    #Soundfile mode
    elif MODE == 2:
        if SCRIPT_FILE == '':
            x = track(SoundFile=SOUND_FILE, key=char)
            threading.Thread(target=x.start).start()
        else:
            Bind['USES'] = "sound"
            Bind[char] = SOUND_FILE
        


    pos+=1

#for replay
if REPLAY_BTN != '':
    x = track(key=REPLAY_BTN, REPLAY_MODE=True)
    threading.Thread(target=x.start).start()

print(f"Active threads: {threading.active_count()}")
print(f"Bound: {Bind}")
if SCRIPT_FILE != '':
    runScriptfile()
else:
    BREAKOUT() #Breakout on the mainthread
