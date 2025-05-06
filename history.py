from machine import Pin
import time
import encoder

def save_result(result):
    try:
        t = time.localtime()
        hour = str(t[3])
        minute = str(t[4])
        if t[3] < 10:
            hour = "0" + hour
        if t[4] < 10:
            minute = "0" + minute
        time_string = str(t[2]) + "." + str(t[1]) + "." + str(t[0]) + " " + hour + ":" + minute

        f = open("history.txt", "a")
        if len(result)==4:
            f.write(time_string + " " +
                    "HR:" + str(int(result[0])) + " " +
                    "PPI:" + str(int(result[1])) + " " +
                    "RMSSD:" + str(int(result[2])) + " " +
                    "SDNN:" + str(int(result[3])) + "\n")
        else:
            f.write(time_string + " " +
                    "HR:" + str(int(result[0])) + " " +
                    "PPI:" + str(int(result[1])) + " " +
                    "RMSSD:" + str(int(result[2])) + " " +
                    "SDNN:" + str(int(result[3])) + " " +
                    "SNS:" + str(result[4]) + " " +
                    "PNS:" + str(result[5]) + " " +
                    "Phys.Age:" + str(result[6]) + "\n")
        f.close()
    except:
        pass

def show_history(oled, rot):
    btn = Pin(12, Pin.IN, Pin.PULL_UP)

    while btn.value() == 0:
        time.sleep(0.05)

    try:
        f = open("history.txt", "r")
        entries = f.readlines()
        f.close()
    except:
        entries = []

    count = 0
    for _ in entries:
        count = count + 1

    if count == 0:
        oled.fill(0)
        oled.text("No measurements", 0, 20)
        oled.show()
        time.sleep(2)
        return

    selected = 0

    while True:
        oled.fill(0)
        oled.text("Measurements", 0, 0)

        start = 0
        if selected >= 4:
            start = selected - 3

        i = 0
        while i < 4:
            entry_index = start + i
            if entry_index < count:
                entry_num = entry_index + 1
                if entry_index == selected:
                    line = "> MEASUREMENT " + str(entry_num)
                else:
                    line = " MEASUREMENT " + str(entry_num)
                oled.text(line, 0, 10 + i * 10)
            i += 1

        oled.show()

        while rot.fifo.has_data():
            move = rot.fifo.get()
            selected = selected + move
            if selected < 0:
                selected = 0
            elif selected >= count:
                selected = count - 1

        if btn.value() == 0:
            while btn.value() == 0:
                pass
            show_entry_detail(oled, entries[selected])
            return

def show_entry_detail(oled, line):
    btn = Pin(12, Pin.IN, Pin.PULL_UP)

    value1 = ""  # date
    value2 = ""  # time
    value3 = ""  # HR
    value4 = ""  # PPI
    value5 = ""  # RMSSD
    value6 = ""  # SDNN
    value7 = ""  # SNS
    value8 = ""  # PNS
    value9 = ""  # phys age

    index = 0
    current = ""
    i = 0
    while i < len(line):
        c = line[i]
        if c == " " or c == "\n":
            if index == 0:
                value1 = current
            elif index == 1:
                value2 = current
            elif index == 2:
                value3 = current
            elif index == 3:
                value4 = current
            elif index == 4:
                value5 = current
            elif index == 5:
                value6 = current
            elif index == 6:
                value7 = current
            elif index == 7:
                value8 = current
            elif index == 8:
                value9 = current
            current = ""
            index += 1
        else:
            current = current + c
        i = i + 1

    oled.fill(0)
    oled.text(value1 + " " + value2, 0, 0)
    oled.text(value3, 0, 9)
    oled.text(value4, 54, 9)
    oled.text(value5, 0, 18)
    oled.text(value6, 0, 27)
    if value7 != "":
        oled.text(value7, 0, 36)
    if value8 != "":
        oled.text(value8, 0, 45)
    if value9 != "":
        oled.text(value9, 0, 54)
    oled.show()

    while btn.value():
        time.sleep(0.01)
    while btn.value() == 0:
        time.sleep(0.01)

