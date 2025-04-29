from ssd1306  import SSD1306_I2C as screen
from time     import sleep
from machine  import Pin, ADC, I2C
lcd            =  screen(128, 64, I2C(1, scl=Pin(15), sda=Pin(14)))
adc            = ADC(26)


def calculate_hr():
    x=0
    values         = []
    min_           = 0
    max_           = 1
    count          = 0
    previous_value = 0
    current_pos    = 0
    haspeaked=False
    lastvalue=0
    lcd.fill(0)
    beats=0
    time=0
    while True:
        current=adc.read_u16()
        values.append(current)
        
        if len(values) >= 500:
            min_=min(values)
            max_=max(values)
            values.clear()
        if count==0:
            scaled_value =63-(current - min_) / (max_-min_)*63
            lcd.line(round(current_pos),round(scaled_value),round(current_pos-1),round(previous_value),1)
        
        
            if current-min_ > (max_-min_)*0.6 and haspeaked == False:
                if current-min_ > lastvalue:
                    lastvalue = current-min_
                elif current-min_ < lastvalue:
                    lcd.fill_rect(round(current_pos-4),round(previous_value),8,8,1)
                    haspeaked = True
                    beats+=1
            elif current-min_ < (max_-min_)*0.5 and haspeaked:
                lastvalue=0
                haspeaked = False
        
            previous_value=scaled_value
            current_pos+=2
            if current_pos >= 128:
                lcd.fill(0)
                current_pos = 0
            
            lcd.show()  
          
          
            count=4
        count-=1
        time+=1
        if time==7500:
            return beats*2
        if min_<=15000 or max_>=60000:
            beats=0
            time=0
            if x == 50:
                print("0")
                x=0
        else:
            if x == 50:
                print("1")
                x=0
        sleep(1/250)
        x+=1
        