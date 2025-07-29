#Caden RIngwood
#Clock
#9/2021


#imports
from Alarm import *
from tkinter import *
from tkinter import font
from tkinter import ttk
import calendar
import time
import datetime

#time zones
ECT=1
EET=2
ART=2
EAT=3
MET=3
NET=4
PLT=5
BST=6
VST=7
CTT=8
JST=9
ACT=9
AET=10
SST=-11
NST=-12
MIT=-11
HST=-10
AST=-9
PST=-8
PNT=-7
MST=-7
CST=-6
EST=-5
IET=-5
PRT=-4
CNT=-3
AGT=-3
BET=-3
CAT=-1

dls=1

#calculating currrent time firm unix epoch
def getTimeNow(timeZone, dls = 0):
    seconds = calendar.timegm(time.gmtime())
    current_second = seconds % 60
    minutes = seconds // 60
    current_minute = minutes % 60
    hours = minutes // 60
    current_hour = hours % 24
    
    #adjusting time for time zone and day light savings
    current_hour = current_hour + timeZone + dls
    
    
    #convert to standerd time
    tag = " AM"
    if current_hour <= 11:
        tag = " AM"
    elif current_hour <= 12:
        tag = " PM"
    elif current_hour >= 13:
        current_hour = current_hour - 12
        tag = " PM"

#alarm
    ahour,aminute,asecond = set_alarm()
    if current_hour == ahour and current_minute == aminute and current_second == asecond:
        alarm()
    
    #format
    if current_hour < 10:
        current_hour = "0"+str(current_hour)
    if current_minute < 10:
        current_minute = "0"+str(current_minute)
    if current_second < 10:
        current_second = "0"+str(current_second)

    current_time = (str(current_hour)+":"+str(current_minute)+":"+str(current_second)+tag)
    
    return current_time

def show_time():
    c_time = getTimeNow(MST,dls)
    txt.set(c_time)
    root.after(1,show_time)

def quit(*args):
    root.destroy()

def set_alarm():
    ahour = 11
    aminute = 47
    asecond = 0
    return ahour, aminute, asecond

#root
root = Tk()
root.attributes("-fullscreen",False)
root.title("Alarm Clock")
root.geometry("800x400")
root.bind("x",quit)
root.bind("a",set_alarm)
root.configure(background = "black")
root.after(1,show_time)
txt = StringVar()
fnt = font.Font(family="Century Gothic",size=60, weight="bold")
lbl = ttk.Label(root,textvariable=txt,foreground="white",background="black",font=fnt)
lbl.place(relx=0.5,rely=0.5,anchor=CENTER)
root.mainloop()










