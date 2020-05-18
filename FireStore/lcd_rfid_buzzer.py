#!/usr/bin/env python3.7

import RPi.GPIO as GPIO
import mfrc522.MFRC522 as MFRC522
from tkinter import *
import threading
import time
import datetime
from master.lcd_display import lcd
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

class App():
    BUZZER= 16
    
    def __init__(self,window):
        self.window = window
        #init buzzer
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.BUZZER, GPIO.OUT)
        self.buzzer = GPIO.PWM(self.BUZZER,50)
        self.buzzer.start(50)
        
        #init LCD
        self.message_lcd = lcd()
        
        #init RFID
        self.previousUid = []
        self.MIFAREReader = MFRC522()
        self.rfidStatusHandler()
        
        #init firebase
        cred = credentials.Certificate('/home/pi/Documents/certificate/raspberrypi-f3174-firebase-adminsdk-bbufq-63a19debda.json')
        firebase_admin.initialize_app(cred)
        self.firestore = firestore.client()
        
    def rfidStatusHandler(self):
        #self.MIFAREReader.MFRC522_Request(self.MIFAREReader.PICC_REQIDL)
        self.buzzer.stop()
        (status, TagType) = self.MIFAREReader.MFRC522_Request(MFRC522.PICC_REQIDL)
        if status == MFRC522.MI_OK:
            print("status success")
            self.message_lcd.display_string("Status Success",1)
            self.message_lcd.display_string("... Welcome ...",2)
            self.buzzer.start(50)
            self.buzzer.ChangeFrequency(523)
            #time.sleep(0.3)
            self.cardRunning()
            self.buzzer.ChangeFrequency(659)
            time.sleep(0.3)
            self.buzzer.stop()
            
        else:
            self.message_lcd.display_string("Put Your Card",1)
            self.message_lcd.display_string(".............",2)
            
            
        threading.Timer(1,self.rfidStatusHandler).start()
        
    def cardRunning(self):
        (status, currentUid) = self.MIFAREReader.MFRC522_Anticoll()
        if status == self.MIFAREReader.MI_OK and set(currentUid) != set(self.previousUid):
            self.previousUid = currentUid;
            cardCode = ""
            for singleId in currentUid:
                cardCode += "{:x}.".format(singleId)
                
            self.message_lcd.display_string("Card ID:",1)
            self.message_lcd.display_string(cardCode.upper(),2)
            self.saveToFireStore(cardCode)
            

    def saveToFireStore(self,cardCode):
        doc_ref = self.firestore.collection('Doors').document()
        currentTime = time.time()
        timestamp = datetime.datetime.utcfromtimestamp(currentTime)
        print(timestamp)
        date = datetime.datetime.fromtimestamp(currentTime).strftime("%Y-%m-%d %H:%M:%S")
        doc_ref.set({
            'timestamp':timestamp,
            'cardId':cardCode,
            '日期':date
        })
        

def on_closing():
    print("視窗關閉被偵測到")
    GPIO.cleanup()
    sys.exit(0)

if __name__ == "__main__":
    GPIO.setwarnings(False)
    root = Tk()
    root.title("RFID_LCD")
    root.protocol("WM_DELETE_WINDOW",on_closing)
    app = App(root)
    root.mainloop()
