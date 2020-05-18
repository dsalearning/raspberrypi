#!user/bin/python3.7

from tkinter import *
from gpiozero import LED
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

class App:
    # 初始化的方法
    def __init__(self, w):
        print("init 被執行")
        self.led = LED(25)
        
        # Fetch the service account key JSON file contents
        cred = credentials.Certificate('/home/pi/Documents/certificate/raspberrypi-f3174-firebase-adminsdk-bbufq-63a19debda.json')
        
        # Initialize the app with a service account, granting admin privileges
        firebase_admin.initialize_app(cred, {
            'databaseURL': 'https://raspberrypi-f3174.firebaseio.com/'
        })
        
        # As an admin, the app has access to read and write all data, regradless of Security Rules
        self.ledRef = db.reference('iot20200425/ledControl')
        self.ledRef.listen(self.firebaseChangeData)

        self.window = w
        print("在class 內部呼叫",type(self.window))
        print("在class 內部呼叫",id(self.window))
        print(self.window.title())
        self.createGUI()


    # 沒有寫sel, 所以是private
    # https://effbot.org/tkinterbook/button.htm
    def createGUI(self):
        print("開始建立視窗外觀")
        btnOn = Button(self.window,
                       text = "LED",
                       padx = 50,
                       pady = 20,
                       font = ("Helvetica",20,"bold italic"),
                       background = "#00ff00",
                       command = self.LED_Click
                       )
        btnOn.pack()
        
    
    def LED_Click(self):
        print("user Click")
        print(self.ledRef.get())
        currentState = self.ledRef.get()
        self.ledRef.set(not currentState)
        #self.led.toggle()
     
    def firebaseChangeData(self,event):
        print('firebaseChangeData')
        #print(type(event))
        if event.data:
            self.led.on()
        else:
            self.led.off()
        

if __name__ == "__main__":
    root = Tk()
    root.title("LED Control")
    app = App(root)
    print("由實體變數取得",type(app.window))
    print("由實體變數取得",id(app.window))
    root.mainloop()
    
    