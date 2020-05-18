#!user/bin/python3.7
from tkinter import *
from threading import Timer
from gpiozero import MCP3008
import math
from master.lcd_display import lcd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class App:
    def __init__(self,w):
        self.window = w
        self.vr0 = MCP3008(0)
        self.my_lcd = lcd()
        
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('/home/pi/Documents/certificate/raspberrypi-f3174-firebase-adminsdk-bbufq-63a19debda.json')
        
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://raspberrypi-f3174.firebaseio.com/'
        })
        
        self.autoUpdate()
        

    def autoUpdate(self):
        #print("autoUpdtea")
        value = round(self.vr0.value*1023)
        print(value)
        self.my_lcd.display_string(str(value),1)
        Timer(1, self.autoUpdate).start()


if __name__ == "__main__":
    window=Tk()
    window.title("MCP3008_可變電阻")
    window.option_add("*font",("verdana",18,"bold"))
    window.option_add("background","#333333")
    window.option_add("foreground","#ffffff")
    app = App(window)
    window.mainloop()
