#!usr/bin/python3.7
'''
這是要控制button和RGBLed
'''

from tkinter import *
from gpiozero import RGBLED, Button
from random import randint
import threading;

class App:
    def __init__(self,window):
        self.button = Button(18)
        self.rgbLed = RGBLED(17,27,22)
        self.rgbLed.color = (1,0,1)
        self.bolbtn = bool('false')
        self.autoUpdate()
        
    def autoUpdate(self):
        if self.button.is_pressed:
            self.bolbtn = not self.bolbtn
            print(self.bolbtn)
            r = randint(0,100) / 100;
            g = randint(0,100) / 100;
            b = randint(0,100) / 100;
            self.rgbLed.color = (r,g,b)

            
        threading.Timer(0.2,self.autoUpdate).start();

if __name__ == '__main__':
    root = Tk()
    root.title("RGBLED")
    root.geometry("700x400")
    root.option_add("*Font",("Helvetica", 18, "bold"))
    root.option_add("*background", "#bbbbbb")
    display = App(root);
    root.mainloop()
