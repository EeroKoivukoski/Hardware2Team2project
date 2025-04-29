from PPM_Heart_mod.menu import run_menu
from PPM_Heart_mod.oled import show_menu_screen, show_text_screen

def main():
    while True:
        rot = Encoder(10, 11)
        btn_select = Pin(12, Pin.IN, Pin.PULL_UP)
        current_index = 0
        menu_items = [
        "1.Measure HR",
        "2.Basic HRV Analysis",
        "3.Kubios",
        "4.History"]
        current_index =run_menu(current_index,menu_items)

if __name__ == "__main__":
    main()

