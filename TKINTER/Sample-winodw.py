#!user/bin/python3.7
from tkinter import *

if __name__=="__main__":
    window=Tk()
    window.title("LED Control")
    window.geometry("300x200")
    Button(window,text="Press").pack(expand=YES, fill=BOTH, padx=5, pady=20)
    window.mainloop()


