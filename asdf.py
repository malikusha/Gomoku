import time
import threading

def hello():
    print "hello, world"
    time.sleep(2)

t = threading.Timer(3.0, hello)
t.start()
while(1):
    print("doing nothing")
    time.sleep(1)
var = 'something'
