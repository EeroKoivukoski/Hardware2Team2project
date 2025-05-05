import menu
global msg
from kubios import connect_wlan
connect_wlan()
def main():
    menu.run_menu()

if __name__ == "__main__":
    main()

