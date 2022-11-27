import socket, os
PORT = 7777
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
conn = {}
conn["IP"] = s.getsockname()[0]
conn["PORT"] = PORT
try: os.mkdir("out")
except: pass
s.close()
repeat = False
#Put here what you want to happen when activated
def Detonate():
    print('Detonated')

template = """import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
IP="$"
PORT=*
s.connect((IP,PORT))
s.close()
"""
template = template.replace('$', conn["IP"])
template = template.replace('*', str(conn["PORT"]))
file = open('out/remote.py', 'w')
file.writelines(template)
file.close()
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((conn["IP"], conn["PORT"]))

while True:
    s.listen()
    print('loop')
    if s.accept():
        Detonate()
        if not repeat:
            break