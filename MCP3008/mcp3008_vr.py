#!user/bin/python3.7
from tkinter import *
from threading import Timer
from gpiozero import MCP3008

class App:
    def __init__(self,w):
        self.window = w
        self.vr0=MCP3008(0)
        self.autoUpdate()


    def autoUpdate(self):
        #print("autoUpdtea")
        print(round(self.vr0.value*1023))
        Timer(0.2,self.autoUpdate).start()


if __name__ == "__main__":
    window=Tk()
    window.title("MCP3008_可變電阻")
    window.option_add("*font",("verdana",18,"bold"))
    window.option_add("background","#333333")
    window.option_add("foreground","#ffffff")
    app = App(window)
    window.mainloop()