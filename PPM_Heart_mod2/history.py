from machine import Pin
import time

def save_result(result):
    try:
        with open("history.txt", "a") as f:
            f.write("HR:{} PPI:{} RMSSD:{} SDNN:{}\n".format(
                int(result[0]), int(result[1]), int(result[2]), int(result[3])
            ))
    except:
        pass

def show_history(oled):
    btn = Pin(12, Pin.IN, Pin.PULL_UP)

    while btn.value() == 0:
        time.sleep(0.05)

    try:
        with open("history.txt", "r") as f:
            entries = f.readlines()
    except:
        entries = []

    count = min(len(entries), 4)

    oled.fill(0)
    oled.text("Last measurements", 0, 0)

    line_y = 10
    for i in range(count):
        parts = entries[-count + i].strip().split()
        if len(parts) == 4:
            line1 = "{} {}".format(parts[0], parts[1])
            line2 = "{} {}".format(parts[2], parts[3])
            oled.text("{}. {}".format(i + 1, line1), 0, line_y)
            oled.text("   {}".format(line2), 0, line_y + 10)
            line_y += 20

    oled.show()

    while btn.value():
        time.sleep(0.01)
    while btn.value() == 0:
        time.sleep(0.01)
