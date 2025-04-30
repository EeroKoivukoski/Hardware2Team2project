#imports
import time
from ssd1306  import SSD1306_I2C as screen
from machine  import Pin, ADC, I2C
import framebuf,smiley_bitmap,x_bitmap
lcd                = screen(128, 64, I2C(1, scl=Pin(15), sda=Pin(14)))
adc                = ADC(26)

def calculate_hr():
    #bitmaps
    imagey = framebuf.FrameBuffer(smiley_bitmap.img, 128, 64, framebuf.MONO_VLSB)
    imagen = framebuf.FrameBuffer(x_bitmap.img, 128, 64, framebuf.MONO_VLSB)
    
    #settings
    accuracy       = 1 #The less accuracy the faster it calibrates, but the peak to peak diff suffers. (1=highest accuracy)
    
    #variables
    values         = []    #List to get the last two seconds of values. This is done to get max and min values for scaling.
    peaks          = []    #Collects the time of a peak to calculate diff later.
    min_           = 0     #Minimum value in the last two seconds.
    max_           = 1     #Maximum value in the last two seconds.
    count          = 0     #When looped "accuracy" times, it will visualize the hbm.
    previous_value = 0     #Last loops scaled value to show the peak block(visualization) correctly.
    lastvalue      = 0     #Is the last loops unscaled value
    current_pos    = 0     #Current position on the lcd
    haspeaked      = False #If a peak happened, it will be true
    update         = False #If lcd is updated
    
    #reset lcd just to be sure
    lcd.fill(0)
    lcd.show()
    
    #True loop
    while True:
        
        #calibration
        if min_ <= 15000 or max_ >= 60000:
            peaks.clear()
            lcd.blit(imagen,0,0)
        elif update == True:
            lcd.blit(imagey,0,0)
            
        #lcd update
        if update==True:
            lcd.show()
            update=False 
            
        #Get sensor value
        current = adc.read_u16()
        
        #Put it in a list
        values.append(current)
        
        #every 500 values, get min and max values
        if len(values) >= 250:
            min_ = min(values)
            max_ = max(values)
            values.clear()
            
        #Only visualize every "accuracy"value   
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
                    peaks.append(newtime)
                    
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
             
        #End when you have 30 peaks
        if len(peaks)==31:
            #Make a list of peak to peak diff.
            calpeaks=[]
            for i in range(1,31):
                calpeaks.append(time.ticks_diff(peaks[i],peaks[i-1]))
            return calpeaks
        
print(calculate_hr())