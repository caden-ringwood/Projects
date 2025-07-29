from tkinter import *
from tkinter.ttk import *
from settings import *
from tkinter import colorchooser as cc
from tkinter import messagebox


class Application(Frame):
    title = "New GUI"
    def __init__(self):
        super(Application, self).__init__()
        self.initUI()

    def initUI(self):
        self.master.title(Application.title)
        self.style = Style()
        self.style.theme_use(theme)
        self.money = 0
        self.moneyVar = StringVar()
        self.moneyVar.set(self.money)

        self.price1 = 10
        self.price1Var = StringVar()
        self.price1Var.set(self.price1)

        self.price2 = 15
        self.price2Var = StringVar()
        self.price2Var.set(self.price2)

        self.priceColor = 100
        self.priceColorVar = StringVar()
        self.priceColorVar.set(self.priceColor)

        self.clickPower = 1
        self.autoPower = 0

        self.times1Uped = 0
        self.times2Uped = 0

        self.LABLE_FONT = ("Arial", 20)

        self.creatWidgets()
        self.onTimer(100000000000000000000000000000000000000000000000000000)


    def centerWindow(self):
        w = WIDTH
        h = HEIGHT
        sw = self.master.winfo_screenwidth()
        sh = self.master.winfo_screenheight()
        pecW = (w / sw)
        ajustedWidth = sw * pecW
        pecH = (h / sh)
        ajustedHeight = sh * pecH

        x = (sw - ajustedWidth) / 2
        y = (sh - ajustedHeight) / 2

        self.master.geometry("%dx%d+%d+%d" % (ajustedWidth, ajustedHeight, x, y))

    def __change_Title__(title):
        Application.title = title

    def creatWidgets(self):
        Label(self, text="$$$", foreground="green").grid(column=2, row=1, sticky=N)
        self.amountMoney = Label(self, textvariable=self.moneyVar)
        self.amountMoney.grid(column=2, row=2, sticky=N)

        self.mainButton = Button(self, text="Click", command=lambda: self.click("main"))\
            .grid(column=2, row=3, sticky=N)

        Label(self, text="+ Power").grid(column=1, row=4, sticky=S)
        self.upgrade1 = Button(self, textvariable=self.price1Var, command=lambda: self.click("1"))\
            .grid(column=1, row=5, sticky=S)

        Label(self, text="+ Auto").grid(column=2, row=4, sticky=S)
        self.upgrade2 = Button(self, textvariable=self.price2Var, command=lambda: self.click("2"))\
            .grid(column=2, row=5, sticky=S)

        Label(self, text="Change Color").grid(column=3, row=4, sticky=S)
        self.upgrade3 = Button(self, textvariable=self.priceColorVar, command=lambda: self.click("color"))\
            .grid(column=3, row=5, sticky=S)

        Label(self, text="WIN", foreground="orange", font=self.LABLE_FONT).grid(column=2, row=6, sticky=S)
        self.upgrade3 = Button(self, text="1,000", command=lambda: self.click("win")) \
            .grid(column=2, row=7, sticky=S)


        self.pack(fill=BOTH, expand=1)
        self.centerWindow()

    def click(self, clicked):
        if clicked == "main":
            self.money = self.money + self.clickPower
            self.moneyVar.set(self.money)

        elif clicked == "1":
            if self.money >= self.price1:
                self.times1Uped += 1
                self.money = self.money - self.price1
                self.moneyVar.set(self.money)
                self.clickPower = self.clickPower + 1
                self.price1 = int((self.price1 + 8) + (self.price1 * .5))
                self.price1Var.set(self.price1)

        elif clicked == "2":
            if self.money >= self.price2:
                self.times2Uped += 1
                self.money = self.money - self.price2
                self.moneyVar.set(self.money)
                self.autoPower = 1 + self.autoPower
                self.price2 = (self.price2 * 2) + 5
                self.price2Var.set(self.price2)

        elif clicked == "color":
            if self.money >= self.priceColor:
                self.money = self.money - self.priceColor
                self.moneyVar.set(self.money)
                self.changeColor()

        elif clicked == "win":
            if self.money >= 10:
                self.money = self.money - 10
                self.moneyVar.set(self.money)
                awnser = messagebox.askyesno("Winner", "You Beat the Button Game!\nDo you want to play again")
                if awnser == False:
                    self.quit()
                if awnser == True:
                    self.initUI()


    def onTimer(self, number):
        if number > 0:
            self.money = self.money + self.autoPower
            self.moneyVar.set((self.money))
            self.after(1000, self.onTimer, number - 1)

    def changeColor(self):
        rgb, hx = cc.askcolor()
        self.style.configure("TLabel", background=hx)
        self.style.configure("TFrame", background=hx)


