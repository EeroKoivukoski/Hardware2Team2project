from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from calculations import calculate
import encoder
import time
from history import save_result
rot = encoder.Encoder(10, 11)


i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

def debounce(pin):
    if not pin.value():
        time.sleep(0.15)
        if not pin.value():
            return True
    return False

def show_menu_screen(items, selected_index):
    oled.fill(0)
    oled.text("Main Menu:", 0, 0)
    i = 0
    for item in items:
        if rot.fifo.has_data():
            rot.fifo.get()
        if i == selected_index:
            prefix = ">"
        else:
            prefix = " "
        oled.text(prefix + item, 0, 10 + i * 10)
        i = i + 1
    oled.show()
    if rot.fifo.has_data():
            rot.fifo.get()

def show_text_screen(title, line2):
    oled.fill(0)
    oled.text(title, 0, 0)
    oled.text(line2, 0, 20)
    oled.show()
    if rot.fifo.has_data():
            rot.fifo.get()
    
def show_result_screen(hr):
    help_btn = Pin(12, Pin.IN, Pin.PULL_UP)
    result = calculate(hr)
    save_result(result)

    oled.fill(0)
    oled.text("MEAN HR: " + str(int(result[0])), 0, 0)
    oled.text("MEAN PPI:" + str(int(result[1])), 0, 10)
    oled.text("RMSSD:  " + str(int(result[2])), 0, 20)
    oled.text("SDNN:   " + str(int(result[3])), 0, 30)
    oled.show()
    if rot.fifo.has_data():
            rot.fifo.get()
    
def show_result_screen_kubios(result):
    help_btn = Pin(12, Pin.IN, Pin.PULL_UP)
    #Mean hr, rr/ppi, rmssd, sdnn, sns, pns, age
    save_result(result)
    oled.fill(0)
    oled.text(f"MEAN HR:   {result[0]}", 0, 0)
    oled.text(f"MEAN PPI:  {result[1]}", 0, 9)
    oled.text(f"RMSSD:     {result[2]:.2f}", 0, 18)
    oled.text(f"SDNN:      {result[3]:.2f}", 0, 27)
    oled.text(f"SNS:       {result[4]:.2f}", 0, 36)
    oled.text(f"PNS:       {result[5]:.2f}", 0, 45)
    oled.text(f"Phys. Age: {result[6]:.2f}", 0, 54)
    print(f"MEAN HR:  {result[0]}")
    print(f"MEAN PPI: {result[1]}")
    print(f"RMSSD:    {result[2]:.2f}")
    print(f"SDNN:     {result[3]:.2f}")
    print(f"SNS:      {result[4]:.2f}")
    print(f"PNS:      {result[5]:.2f}")
    print(f"Phys.Age: {result[6]:.2f}")
    
    oled.show()
    while help_btn.value():
        if rot.fifo.has_data():
            rot.fifo.get()
        time.sleep(0.01)