import json
from selenium import webdriver
from playsound import playsound
import time, threading
import ctypes
from pynput.keyboard import Key,Controller
data = {}

template={"Active":False,"WebLink":"","Current_Option":0,"CountDown":5, "WebDriver":"chromedriver.exe","PlaySoundWhileBrowser":False,"SoundFileName":"sound.wav","Options":{"1.":"Open WebLink; WebLink has to be filled in; if you want sound while browser is open, set PlaySoundWhileBrowsing to true", "2.":"lock screen and play sound; SoundFileName has to be filled in."}}

def pts(): playsound(data["SoundFileName"])
def startPlaySound(): threading.Thread(target=pts).start()

try:
    #Does stuff when the file has been opened.
    with open("conf.json", 'r') as file:
        data = json.load(file)
    #Only activates when conf 'Active' is true
    if data["Active"]:
        print(f"Entered Countdown ({data['CountDown']} minutes)")
        time.sleep(data["CountDown"]*60)
        #If the current option has been filled in
        if not data["Current_Option"] > len(data["Options"]) and data["Current_Option"] >= 1:
            if data["Current_Option"] == 1:
                #----------------------------------------------------------------------------------First option
                driver = webdriver.Chrome(data["WebDriver"])
                driver.maximize_window()
                driver.get(data["WebLink"])
                if data["PlaySoundWhileBrowser"]:
                    print("Playing sound")
                    keyboard = Controller()
                    for x in range(100):
                        keyboard.press(Key.media_volume_up)
                        keyboard.release(Key.media_volume_up)
                    startPlaySound()

            
            elif data["Current_Option"] == 2:
                #----------------------------------------------------------------------------------Second option
                
                keyboard = Controller()
                for x in range(100):
                    keyboard.press(Key.media_volume_up)
                    keyboard.release(Key.media_volume_up)
                ctypes.windll.user32.LockWorkStation()
                startPlaySound()



except(FileNotFoundError):
    with open("conf.json", 'w') as file:
        json.dump(template, file, indent=4)
        file.close()
