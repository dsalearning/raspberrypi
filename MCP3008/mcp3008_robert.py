#!/usr/bin/python3.7
from tkinter import *
from threading import Timer
from gpiozero import MCP3008
import math
from master.lcd_display import lcd

class App:
    def __init__(self,w):
        self.window = w
        self.channel0 = MCP3008(0)
        self.my_lcd = lcd()
        self.autoUpdate()


    def autoUpdate(self):
        value = self.channel0.value
        print(value)
        self.my_lcd.display_string(str(math.floor(value*100)),1)
        Timer(1, self.autoUpdate).start()

if __name__ == '__main__':
    window = Tk()
    window.title('MCP3008_可變電阻')
    window.option_add("*font",('verdana', 18, 'bold'))
    window.option_add("*background", '#333333')
    window.option_add("*foreground",'#ffffff')
    app = App(window)
    window.mainloop()