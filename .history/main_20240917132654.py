import PTZ
from threading import Thread
import time

def thread_function(ptz):
    print("Thread started")
    time.sleep(2)
    r,w,h = ptz.get_resolution()
    ptz.move(-91.22,-2.05)
    time.sleep(3)
    ptz.zoom(4552)
    time.sleep(3)
    ptz.move(-67.43,-1.33)
    time.sleep(1)
    # ptz.set_preset("bar")
    # ptz.remove_preset("bar")


ptz = PTZ.PTZ('192.168.0.90')
print("Start")
t = Thread(target=thread_function,args=(ptz,)).start()
ptz.display()