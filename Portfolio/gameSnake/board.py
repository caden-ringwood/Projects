from settings import *
import sys
import random
from PIL import Image, ImageTk
from tkinter import Tk, Frame, Canvas, ALL, NW

class Board(Canvas):
    def __init__(self):
        super(Board, self).__init__(width=BOARD_SIZE, height=BOARD_SIZE, background="black", highlightthickness=2)

        self.initGame()
        self.pack()

    def initGame(self):
        self.ingame = True
        self.parts = 3
        self.score = 0

        self.moveX = SIZE
        self.moveY = 0

        self.appleX = 100
        self.appleY = 200

        self.loadImages()
        self.createObjs()
        self.locateApple()
        self.bind_all("<Key>", self.onKeyPressed)
        self.after(DELAY, self.onTimer)

    def loadImages(self):
        try:
            self.img_apple = Image.open("imgs/apple.png")
            self.img_head = Image.open("imgs/snakeHead.png")
            self.img_body = Image.open("imgs/snakeBody.png")
            self.apple = ImageTk.PhotoImage(self.img_apple)
            self.head = ImageTk.PhotoImage(self.img_head)
            self.body = ImageTk.PhotoImage(self.img_body)

        except IOError as e:
            print(e)
            sys.exit(1)

    def createObjs(self):
        self.create_text(32, 12, text="Score: {0}".format(self.score), tag="score_text", fill="green", font=30)
        self.create_image(self.appleX, self.appleY, image=self.apple, tag="apple", anchor=NW)
        self.create_image(50, 50, image=self.head, tag="head")
        self.create_image(60, 50, image=self.body, tag="body")
        self.create_image(70, 50, image=self.body, tag="body")

    def locateApple(self):
        apple =self.find_withtag("apple")
        self.delete(apple[0])
        self.appleX = random.randint(0, MAX_RAND_POS)*SIZE
        self.appleX = random.randint(0, MAX_RAND_POS) * SIZE
        self.create_image(self.appleX, self.appleY, image=self.apple, tag="apple", anchor=NW)

    def onKeyPressed(self, e):
        key = e.keysym

        if key == LEFT_CURSOR_KEY and self.moveX < 0:
            self.moveX = -SIZE
            self.moveY = 0
        if key == RIGHT_CURSOR_KEY and self.moveX >= 0:
            self.moveX = SIZE
            self.moveY = 0
        if key == UP_CURSOR_KEY and self.moveY <= 0:
            self.moveX = 0
            self.moveY = SIZE
        if key == DOWN_CURSOR_KEY and self.moveY >= 0:
            self.moveX = 0
            self.moveY = -SIZE

    def onTimer(self):
        self.drawScore()
        self.checkCollision()
        if self.ingame:
            self.checkAppleCollision()
            self.moveSnake()
            self.after(DELAY, self.onTimer())
        else:
            self.gameOver()

    def drawScore(self):
        score = self.find_withtag("score_text")
        self.itemconfigure(score, text="Score: {0}".format(self.score))

    def checkCollision(self):
        body_parts = self.find_withtag("body")
        head = self.find_withtag("head")

        x1, y1, x2, y2 = self.bbox(head)
        overlapping = self.find_overlapping(x1, y1, x2, y2)
        for part in body_parts:
            for lap in overlapping:
                if lap == part:
                    self.ingame = False

        if x1 < 0 or x1 > BOARD_SIZE-SIZE:
            self.ingame = False

        if y1 < 0 or y1 > BOARD_SIZE-SIZE:
            self.ingame = False

    def checkAppleCollision(self):
        head = self.find_withtag("head")
        apple = self.find_withtag("apple")

        x1, y1, x2, y2 = self.bbox(head)
        overlapping = self.find_overlapping(x1, y1, x2, y2)
        for lap in overlapping:
            if apple[0] == lap:
                self.score += 1
                x, y = self.coords(apple)
                self.create_image(x, y, image=self.body, tag="body")
                self.locateApple()

    def moveSnake(self):
        bodyParts = self.find_withtag("body")
        head = self.find_withtag("head")
        list = bodyParts + head
        z = 0
        while z < len(list) - 1:
            c1 = self.coords(list[z])
            c2 = self.coords(list[z+1])
            self.move(list[z], c2[0] - c1[0], c2[1] - c1[1])
            z += 1
        self.move(head, self.moveX, self.moveY)

    def gameOver(self):
        self.delete(ALL)
        self.create_text(self.winfo_width()/2, self.winfo_height()/2, text="Game Over with score {0}".format(self.score))
