from machine import Pin
from fifo import Fifo

class Encoder:
    def __init__(self, rot_a, rot_b):
        self.a = Pin(rot_a, mode=Pin.IN)
        self.b = Pin(rot_b, mode=Pin.IN)
        self.fifo = Fifo(30, typecode='i')
        self.a.irq(handler=self.handler, trigger=Pin.IRQ_RISING, hard=True)

    def handler(self, pin):
        try:
            if self.b():
                self.fifo.put(-1)
            else:
                self.fifo.put(1)
        except:
            pass 

