#imports
import time,framebuf,encoder
import animations.smiley_bitmap as smile_heart
import animations.x_bitmap as x_heart
import animations.smileyer_bitmap as smilest_heart
from ssd1306  import SSD1306_I2C as screen
from machine  import Pin, ADC, I2C
rot = encoder.Encoder(10, 11)
lcd                = screen(128, 64, I2C(1, scl=Pin(15), sda=Pin(14)))
adc                = ADC(26)
btn                =Pin(12, Pin.IN, Pin.PULL_UP)

def calculate_hr():
    lcd.fill(0)
    lcd.text("Loading...",0,0,1)
    lcd.show()

    #variables
    values         = []    #List to get the last two seconds of values. This is done to get max and min values for scaling.
    peaks          = []    #Collects the time of a peak to calculate diff later.
    min_           = 0     #Minimum value in the last two seconds.
    max_           = 1     #Maximum value in the last two seconds.
    previous_value = 0     #Last loops scaled value to show the peak block(visualization) correctly.
    lastvalue      = 0     #Is the last loops unscaled value
    haspeaked      = False #If a peak happened, it will be true
    update         = False #If lcd is updated
    calib          = 3     #If calibrated 1 or 2
    check          = False
    btn_check      = False
    meanppi        = 0
    meanhrv        = 0
    hearts = framebuf.FrameBuffer(smile_heart.img, 128, 64, framebuf.MONO_VLSB)
    heartx = framebuf.FrameBuffer(x_heart.img, 128, 64, framebuf.MONO_VLSB)
    hearte = framebuf.FrameBuffer(smilest_heart.img, 128, 64, framebuf.MONO_VLSB)
    
    #True loop
    while True:
        if rot.fifo.has_data():
            rot.fifo.get()
        if btn.value():
            btn_check=True        
        #Get sensor value
        current = adc.read_u16()
        
        #Put it in a list
        values.append(current)
        
        #every 500 values, get min and max values
        if len(values) >= 500:
            min_ = min(values)
            max_ = max(values)
            values.clear()
            
        #Only vis
            #get peaks
        if current-min_ > ( max_ - min_ ) * 0.6 and haspeaked == False:
            if current - min_ > lastvalue:
                lastvalue = current - min_
            elif current - min_ < lastvalue:
                newtime = time.ticks_ms()
                haspeaked = True
                peaks.append(newtime)
                check=True
        #when new peak is about to come       
        elif current-min_ < (max_- min_) * 0.5 and haspeaked:
            lastvalue=0
            haspeaked = False
               
            #animation
            
        if calib==1:
            lcd.blit(hearts,0, 0)
        elif calib==2:
            lcd.blit(hearte,0,0)
        else:
            lcd.blit(heartx,0,0)
        lcd.text(f"Mean PPI: "+str(meanppi),0,45,1)
        lcd.text(f"BPM: "+str(meanhrv),0,55,1)
        update=True  

        
        #calibration :)
        if len(peaks) % 5==0 and check:
            calpeaks=[]
            for i in range(len(peaks)-len(peaks),len(peaks)):
                calpeaks.append(time.ticks_diff(peaks[i],peaks[i-1]))
                
            for i in range(len(calpeaks)-4,len(calpeaks)):
                if not check:
                    pass
                elif calpeaks[i] >= 2000 or calpeaks[i] <= 250:
                    peaks.clear()
                    lcd.rect(0,0,4,4,0)
                    calib=3
                    check=False
                    lcd.fill(0)
                else:
                    calib=1
                    lcd.fill(0)
                    update=False
            #Measure when you have 10 peaks
            if calib==1:
                calib=2
                del calpeaks[0]
                sum = 0
                for i in calpeaks:
                    sum += i
                meanppi=sum/len(calpeaks)
                meanhrv=60/(meanppi/1000)
                peaks.clear()
                check=False
                lcd.fill(0)
                update=False
                
        #lcd update
        if update==True:
            lcd.show()
            update=False
        if not btn.value() and btn_check:
            time.sleep(0.15)
            if not btn.value():
                return "counted"
#print(calculate_hr()) #Testline, add comment if not already added
            