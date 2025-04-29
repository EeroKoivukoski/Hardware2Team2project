from oled import show_menu_screen, show_text_screen
from encoder import Encoder
from machine import Pin
import time

menu_items = [
    "1.Measure HR",
    "2.Basic HRV Analysis",
    "3.Kubios",
    "4.History"
]

current_index = 0
rot = Encoder(10, 11)
btn_select = Pin(12, Pin.IN, Pin.PULL_UP)

def debounce(pin):
    if not pin.value():
        time.sleep(0.15)
        if not pin.value():
            return True
    return False

def show_collecting_screen():
    show_text_screen("Collecting Data...")
    time.sleep(2)

def show_sending_screen():
    show_text_screen("Sending Data...")
    time.sleep(2)

def show_error_screen():
    show_text_screen("ERROR SENDING DATA", "Press the button to retry or wait 3 seconds to return to main mnu")
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < 3000:
        if not btn_select.value():
            return True
    return False

def show_result_screen():
    oled.fill(0)
    oled.text("MEAN HR:", 0, 0)
    oled.text("MEAN PPI:", 0, 10)
    oled.text("RMSSD:", 0, 20)
    oled.text("SDNN:", 0, 30)
    oled.text("SNS:", 0, 40)
    oled.text("PNS:", 0, 50)
    oled.show()
    time.sleep(2)

def show_history_list():
    history_items = ["Measuremnt 1", "Measurement 2", "Measurement 3", "Measurement4", "Mesurement5"]
    selected = 0
    while True:
        show_menu_screen(history_items, selected)
        if rot.fifo.has_data():
            move = rot.fifo.get()
            selected = (selected + move) % 5
        if debounce(btn_select):
            show_result_screen()
            break

def run_menu():
    current_index
    last_scroll_time = time.ticks_ms()

    while True:
        show_menu_screen(menu_items, current_index)

        if rot.fifo.has_data():
            now = time.ticks_ms()
            if time.ticks_diff(now, last_scroll_time) > 100:
                move = rot.fifo.get()
                current_index = (current_index + move) % 4
                last_scroll_time = now

        if debounce(btn_select):
            selected = current_index

            if selected == 0:
                show_collecting_screen()
                show_result_screen()

            elif selected == 1:
                show_collecting_screen()
                show_result_screen()

            elif selected == 2:
                show_collecting_screen()
                show_sending_screen()
                if show_error_screen():
                    show_sending_screen()
                show_result_screen()

            elif selected == 3:
                show_history_list()
                
            time.sleep(1)

