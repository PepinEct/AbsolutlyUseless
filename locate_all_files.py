import os, threading, time

ONLY_FOLDERS = True
MAX_CACHED = 20000
total = 0
OUTPUT_FILE = "Out.txt"
TEMP_STORED = []
DEBUG = False


pre =time.perf_counter()
open(OUTPUT_FILE, 'w').close()
def store(item):
    global TEMP_STORED, MAX_CACHED, OUTPUT_FILE, total
    total+=1
    TEMP_STORED.append(item)
    if len(TEMP_STORED) > MAX_CACHED:
        #print('triggerd')
        temp = TEMP_STORED
        TEMP_STORED = []
        with open(OUTPUT_FILE, 'a') as file:
            for x in temp:
                file.writelines('\n'+str(x))
            file.close()
def debug(msg):
    global DEBUG
    if DEBUG:
        print(msg)
def active():
    global TEMP_STORED, pre
    while True:
        time.sleep(1)
        print(f"Active Threads: {threading.active_count()}")
        if threading.active_count() == 2:
            with open(OUTPUT_FILE, 'a') as file:
                for x in TEMP_STORED:
                    file.writelines('\n'+str(x))
                file.close()
            print(f"Took {time.perf_counter()-pre} seconds and scanned {total} files")
            break


def find_files(dir):
    debug(dir)
    global TEMP_STORED, whitelisted, ONLY_FOLDERS
    try:
        for file in os.listdir(dir):
            
            if file.strip() != 'Windows':

                    if os.path.isdir(dir+'/'+file):
                        try:
                            if ONLY_FOLDERS:
                                store(f"{dir}/{file}")
                            threading.Thread(target=find_files, args=(f"{dir}/{file}",)).start()
                            pass
                        except(Exception):
                            #print(f"{file}: Access denied.")
                            pass
                    else:
                        if not ONLY_FOLDERS:
                            store(f"{file}: ------- {dir}/{file}")
    except(Exception):
        #print(e)
        pass


dir = "C:/"
find_files(dir)
    #print(x)
threading.Thread(target=active).start()
input()