#!user/bin/python3.7
from tkinter import *
from threading import Timer
from gpiozero import MCP3008
from gpiozero import LED
import math
from master.lcd_display import lcd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


class App:
    def __init__(self,w):
        self.window = w
        self.channel0 = MCP3008(0)
        self.lightness = MCP3008(7)
        self.led = LED(18)
        self.my_lcd = lcd()
        
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('/home/pi/Documents/certificate/raspberrypi-f3174-firebase-adminsdk-bbufq-63a19debda.json')
        
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://raspberrypi-f3174.firebaseio.com/'
        })
        self.vr_value_ref = db.reference('iot20200425/vr_value')
        self.lightness_ref = db.reference('iot20200425/lightness')
        
        self.autoUpdate()
        

    def autoUpdate(self):
        channel0value = self.channel0.value
        lightnessValue = self.lightness.value * 1000
        
        if lightnessValue<20:
            self.led.on()
        else:
            self.led.off()
            
        print(lightnessValue)
        self.vr_value_ref.set(math.floor(channel0value*100))
        self.lightness_ref.set(math.floor(lightnessValue))
        self.my_lcd.display_string("VR  = "+str(math.floor(channel0value*100)),1)
        self.my_lcd.display_string("CDS = "+str(math.floor(lightnessValue)),2)
        Timer(0.5, self.autoUpdate).start()


if __name__ == "__main__":
    window=Tk()
    window.title("MCP3008_可變電阻")
    window.option_add("*font",("verdana",18,"bold"))
    window.option_add("background","#333333")
    window.option_add("foreground","#ffffff")
    app = App(window)
    window.mainloop()
