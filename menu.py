from oled import show_menu_screen, show_text_screen, show_result_screen,show_result_screen_kubios, oled
from history import show_history
import encoder
from machine import Pin
import time
from test import calculate_hr
from hr_test import calculate_hr as measure_hr
from kubios import kubiosconnecton,callbackfunction,send_data


menu_items = [
    "Measure HR",
    "HRV Analysis",
    "Kubios Analysis",
    "HRV History"
]

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

def show_error_screen():
    show_text_screen("Press button to retry",
                     "or wait 3s for menu")
    start = time.ticks_ms()
    while time.ticks_diff(time.ticks_ms(), start) < 3000:
        if not btn_select.value():
            return True
    return False

def run_menu():
    current_index=0
    update=True
    
    while True:
        if update:
            show_menu_screen(menu_items, current_index)
            update=False

        while rot.fifo.has_data():
            move = rot.fifo.get()
            current_index = (current_index + move) % 4
            update=True

        if debounce(btn_select):
            selected = current_index

            if selected == 0:
                measure_hr()
                update=True

            elif selected == 1:
                hr=calculate_hr()
                show_result_screen(hr)
                update=True

            elif selected == 2:
                check=True
                while check:
                    hr=kubiosconnecton(calculate_hr())
                    if hr:
                        show_result_screen_kubios(hr)
                        send_data(hr)
                        check=False
                    else:
                        check=show_error_screen()
                update=True
                

            elif selected == 3:
                show_history(oled, rot)
                update=True