import menu, animations.PU_bitmap as pu , animations.SE_bitmap as se, animations.Lightning_bitmap as light, time, framebuf
global msg
from kubios import connect_wlan
from oled import oled
def main():
    intro()
    connect_wlan()
    menu.run_menu()
def intro():
    PU=framebuf.FrameBuffer(pu.img, 42, 64, framebuf.MONO_VLSB)
    SE=framebuf.FrameBuffer(se.img, 42, 64, framebuf.MONO_VLSB)
    L=framebuf.FrameBuffer(light.img, 42, 64, framebuf.MONO_VLSB)
    oled.fill(0)
    oled.blit(PU,0 ,0)
    oled.blit(SE,84,0)
    
    x=0
    while x != 64:
        oled.blit(L,42,x-64)
        oled.show()
        x+=1
    for _ in range(4):
        oled.invert(1)
        oled.show()
        time.sleep(0.1)
        oled.invert(0)
        oled.show()
        time.sleep(0.1)

    
        
if __name__ == "__main__":
    main()

