from tkinter import *
from tkinter.ttk import *
from settings import *
from tkinter import messagebox
from tkinter import filedialog as fd


class Application(Frame):
    title = "New GUI"
    def __init__(self):
        super(Application, self).__init__()
        self.initUI()

    def initUI(self):
        self.master.title(Application.title)
        self.style = Style()
        self.style.theme_use(theme)
        self.creatWidgets()
        self.input = 0

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

        self.screentxt = Text(self, width=20, height=1)
        self.screentxt.grid(column=1, row=1, columnspan=4, sticky=N)

        self.one = Button(self, text="1", command=lambda: self.entry("1")).grid(column=1, row=2, sticky=W)
        self.two = Button(self, text="2", command=lambda: self.entry("2")).grid(column=2, row=2, sticky=W)
        self.three = Button(self, text="3", command=lambda: self.entry("3")).grid(column=3, row=2, sticky=W)
        self.times = Button(self, text="X", command=lambda: self.entry("X")).grid(column=4, row=2, sticky=W)
        self.four = Button(self, text="4", command=lambda: self.entry("4")).grid(column=1, row=3, sticky=W)
        self.five = Button(self, text="5", command=lambda: self.entry("5")).grid(column=2, row=3, sticky=W)
        self.six = Button(self, text="6", command=lambda: self.entry("6")).grid(column=3, row=3, sticky=W)
        self.divide = Button(self, text="/", command=lambda: self.entry("/")).grid(column=4, row=3, sticky=W)
        self.seven = Button(self, text="7", command=lambda: self.entry("7")).grid(column=1, row=4, sticky=W)
        self.eight = Button(self, text="8", command=lambda: self.entry("8")).grid(column=2, row=4, sticky=W)
        self.nine = Button(self, text="9", command=lambda: self.entry("9")).grid(column=3, row=4, sticky=W)
        self.add = Button(self, text="+", command=lambda: self.entry("+")).grid(column=4, row=4, sticky=W)
        self.color = Button(self, text="Clear", command=lambda: self.entry("C")).grid(column=1, row=5, sticky=N)
        self.zero = Button(self, text="0", command=lambda: self.entry("0")).grid(column=2, row=5, sticky=N)
        self.equals = Button(self, text="=", command=lambda: self.entry("=")).grid(column=3, row=5, sticky=N)
        self.minus = Button(self, text="-", command=lambda: self.entry("-")).grid(column=4, row=5, sticky=N)

        self.pack(fill=BOTH, expand=1)
        self.centerWindow()

    def entry(self, data):
        if self.input == 0:
            if data == "1":
                print(1)
                self.screentxt.insert(END, "1")

            elif data == "2":
                print(2)
                self.screentxt.insert(END, "2")

            elif data == "3":
                print(3)
                self.screentxt.insert(END, "3")

            elif data == "X":
                print("X")
                self.input += 1
                self.number1 = self.screentxt.get(0.0, END)
                self.symbol = "X"
                self.screentxt.delete(0.0, END)

            elif data == "4":
                print(4)
                self.screentxt.insert(END, "4")

            elif data == "5":
                print(5)
                self.screentxt.insert(END, "5")

            elif data == "6":
                print(6)
                self.screentxt.insert(END, "6")

            elif data == "/":
                print("/")
                self.input += 1
                self.number1 = self.screentxt.get(0.0, END)
                self.symbol = "/"
                self.screentxt.delete(0.0, END)

            elif data == "7":
                print(7)
                self.screentxt.insert(END, "7")

            elif data == "8":
                print(8)
                self.screentxt.insert(END, "8")

            elif data == "9":
                print(9)
                self.screentxt.insert(END, "9")

            elif data == "+":
                print(self.input)
                self.input += 1
                self.number1 = self.screentxt.get(0.0, END)
                self.symbol = "+"
                self.screentxt.delete(0.0, END)

            elif data == "C":
                self.screentxt.delete(0.0, END)
                self.input = 0

            elif data == "0":
                print(0)
                self.screentxt.insert(END, "0")

            elif data == "-":
                print("-")
                self.input += 1
                self.number1 = self.screentxt.get(0.0, END)
                self.symbol = "-"
                self.screentxt.delete(0.0, END)

            elif data == "=":
                print("=")
                equation = self.screentxt.get(0.0, END)
                self.screentxt.delete(0.0, END)
                print(equation)


        elif self.input == 1:
            if data == "1":
                print(1)
                self.screentxt.insert(END, "1")

            elif data == "2":
                print(2)
                self.screentxt.insert(END, "2")

            elif data == "3":
                print(3)
                self.screentxt.insert(END, "3")

            elif data == "X":
                print("X")
                self.input = 0
                self.screentxt.delete(0.0, END)

            elif data == "4":
                print(4)
                self.screentxt.insert(END, "4")

            elif data == "5":
                print(5)
                self.screentxt.insert(END, "5")

            elif data == "6":
                print(6)
                self.screentxt.insert(END, "6")

            elif data == "/":
                print("/")
                self.screentxt.insert(END, "/")
                self.input = 0
                self.screentxt.delete(0.0, END)

            elif data == "7":
                print(7)
                self.screentxt.insert(END, "7")

            elif data == "8":
                print(8)
                self.screentxt.insert(END, "8")

            elif data == "9":
                print(9)
                self.screentxt.insert(END, "9")

            elif data == "+":
                print("+")
                self.input += 1
                self.screentxt.delete(0.0, END)

            elif data == "C":
                self.screentxt.delete(0.0, END)
                self.input = 0

            elif data == "0":
                print(0)
                self.screentxt.insert(END, "0")

            elif data == "-":
                print("-")
                self.screentxt.insert(END, "-")
                self.screentxt.delete(0.0, END)
                self.input = 0

            elif data == "=":
                print(self.input)
                self.number2 = self.screentxt.get(0.0, END)
                self.screentxt.delete(0.0, END)
                self.calculate(self.symbol, self.number1, self.number2)


    def calculate(self, symbol, number1, number2):
        if symbol == "+":
            awnser = int(number1) + int(number2)
            self.screentxt.insert(END, awnser)

        elif symbol == "-":
            awnser = int(number1) - int(number2)
            self.screentxt.insert(END, awnser)

        elif symbol == "X":
            awnser = int(number1) * int(number2)
            self.screentxt.insert(END, awnser)

        elif symbol == "/":
            try:
                awnser = int(number1) / int(number2)
                self.screentxt.insert(END, awnser)

            except:
                messagebox.showerror("Error", "Error: Can't devide by zero")




