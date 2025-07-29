from settings import *
from board import *

class Snake(Frame):
    def __init__(self):
        super(Snake, self).__init__()
        self.master.title(title)
        self.board = Board()
        self.pack()

def main():
    root =Tk()
    x = Snake()
    root.mainloop()

main()