from machine import Pin, I2C
from ssd1306 import SSD1306_I2C

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

def show_menu_screen(items, selected_index):
    oled.fill(0)
    oled.text("Main Menu:", 0, 0)
    i = 0
    for item in items:
        if i == selected_index:
            prefix = ">"
        else:
            prefix + " "
        oled.text(prefix + item, 0, 10 + i * 10)
        i += 1
    oled.show()

def show_text_screen(title, line2=""):
    oled.fill(0)
    oled.text(title, 0, 0)
    oled.text(line2, 0, 20)
    oled.show()

