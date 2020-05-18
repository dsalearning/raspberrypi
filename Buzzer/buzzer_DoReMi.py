#!/usr/local/bin/python
from tkinter import *
import time
import RPi.GPIO as GPIO
#from gpiozero import Button

class App:
    def __init__(self,w):
        self.window = w
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(16, GPIO.OUT)
        self.p = GPIO.PWM(16, 50)
        self.createGUI()

    def createGUI(self):
        print("開始建立視窗外觀")
        btnOn = Button(self.window,
                       text = "Play",
                       padx = 50,
                       pady = 20,
                       font = ("Helvetica",20,"bold italic"),
                       background = "#00ff00",
                       command = self.doReMi
                       )
        btnOn.pack()

    def doReMi(self):
        self.p.start(50)
        print("Do")
        self.p.ChangeFrequency(523)
        time.sleep(1)

        print("Re")
        self.p.ChangeFrequency(587)
        time.sleep(1)
       
        print("Mi")
        self.p.ChangeFrequency(659)
        time.sleep(1)
        self.p.stop()


def on_closing():
    print("視窗關閉被偵測到")
    #self.p.stop()
    GPIO.cleanup()
    sys.exit(0)

if __name__ == '__main__':
    root = Tk()
    root.title("DoReMi")
    root.geometry("700x400")
    root.protocol("WM_DELETE_WINDOW",on_closing)
    display = App(root)
    root.mainloop()