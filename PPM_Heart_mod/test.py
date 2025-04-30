#imports
import time
from ssd1306  import SSD1306_I2C as screen
from machine  import Pin, ADC, I2C
lcd                = screen(128, 64, I2C(1, scl=Pin(15), sda=Pin(14)))
adc                = ADC(26)

#start timer
start              = time.ticks_ms()

def calculate_hr():
    
    #settings
    accuracy       = 2
    #variables
    values         = []
    min_           = 0
    max_           = 1
    lastpeak       = 0
    count          = 0
    previous_value = 0
    current_pos    = 0
    haspeaked      = False
    lastvalue      = 0
    peaks          = []
    update         = False
    
    #reset lcd
    lcd.fill(0)
    
    #True loop
    while True:
        
        #Get sensor value
        current = adc.read_u16()
        
        #Put it in a list
        values.append(current)
        
        #every 500 values, get min and max values
        if len(values) >= 500:
            min_ = min(values)
            max_ = max(values)
            values.clear()
            
        #Only visualize every (accuracy) value   
        if count==0:
            scaled_value = 63 - ( current - min_ ) / ( max_ - min_ ) * 63
            lcd.line ( round ( current_pos ) , round ( scaled_value ) , round ( current_pos ) , round ( previous_value ) , 1 )
            if current-min_ > ( max_ - min_ ) * 0.6 and haspeaked == False:
                if current - min_ > lastvalue:
                    lastvalue = current - min_
                elif current - min_ < lastvalue:
                    newtime = time.ticks_ms()
                    lcd.fill_rect ( round (current_pos - 4 ) , round ( previous_value ) , 8 , 8 , 1 )
                    haspeaked = True
                    if lastpeak == 0:
                        peaks.append(newtime-start-lastpeak)
                    peaks.append(newtime-lastpeak)
                    lastpeak= newtime - start -lastpeak
                    
            elif current-min_ < (max_- min_) * 0.5 and haspeaked:
                lastvalue=0
                haspeaked = False
            previous_value=scaled_value
            current_pos+=2
            if current_pos >= 128:
                lcd.fill(0)
                current_pos = 0
            update=True  
            count=accuracy
        count-=1
        
        #calibration
        if min_ <= 15000 or max_ >= 60000:
            peaks.clear()
            lcd.rect(0,0,4,4,0)
        elif update == True:
            lcd.rect(0,0,4,4,1)

           
        #lcd update
        if update==True:
            lcd.show()
            update=False
            
        #End
        if len(peaks)==30:
            end = time.ticks_ms()-start
            time_taken = end - start
            return peaks
print(calculate_hr())