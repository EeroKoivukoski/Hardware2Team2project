from oled import show_menu_screen, show_text_screen, show_result_screen
import encoder
from machine import Pin
import time
from test import calculate_hr

menu_items = [
    "1.Measure HR",
    "2.Basic HRV Analysis",
    "3.Kubios",
    "4.History"
]

current_index = 0
rot = encoder.Encoder(10, 11)
btn_select = Pin(12, Pin.IN, Pin.PULL_UP)

def debounce(pin):
    if not pin.value():
        time.sleep(0.15)
        if not pin.value():
            return True
    return False

def show_collecting_screen():
    hr=calculate_hr()
    return hr

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
    current_index=0
    last_scroll_time = time.ticks_ms()
    update=True
    while True:
        if update==True:
            show_menu_screen(menu_items, current_index)
            update=False

        while rot.fifo.has_data():
            now = time.ticks_ms()
            move = rot.fifo.get()
            current_index = (current_index + move) % 4
            last_scroll_time = now
            update=True

        if debounce(btn_select):
            selected = current_index

            if selected == 0:
                hr=show_collecting_screen()
                show_result_screen(hr)
                update=True

            elif selected == 1:
                hr=show_collecting_screen()
                show_result_screen(hr)
                update=True

            elif selected == 2:
                show_collecting_screen()
                show_sending_screen()
                if show_error_screen():
                    show_sending_screen()
                show_result_screen()
                update=True

            elif selected == 3:
                show_history_list()
                update=True
                
            time.sleep(1)