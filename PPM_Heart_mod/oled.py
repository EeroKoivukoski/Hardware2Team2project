from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from calculations import calculate
import encoder
import time

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
        if i == selected_index:
            prefix = ">"
        else:
            prefix = " "
        oled.text(prefix + item, 0, 10 + i * 10)
        i += 1
    oled.show()

def show_text_screen(title, line2=""):
    oled.fill(0)
    oled.text(title, 0, 0)
    oled.text(line2, 0, 20)
    oled.show()
    
def show_result_screen(hr):
    help=Pin(12, Pin.IN, Pin.PULL_UP)
    list=calculate(hr)
    oled.fill(0)
    oled.text("MEAN HR: "  + str(list[0]), 0, 0 )
    oled.text("MEAN PPI: " + str(list[1]), 0, 10)
    oled.text("RMSSD: "    + str(list[2]), 0, 20)
    oled.text("SDNN: "     + str(list[3]), 0, 30)
    oled.show()
    while not debounce(help):
        pass